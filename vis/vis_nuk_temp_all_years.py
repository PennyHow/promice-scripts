#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 08:34:09 2022

@author: pho
"""
import math,datetime,random
import pandas as pd
import matplotlib.pyplot as plt

# Define station files
# infile = [
#     ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/CEN1/CEN1_hour.csv',
#     'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/CEN2/CEN2_hour.csv'],
#     ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/HUM/HUM_hour.csv'],
#     ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/NEM/NEM_hour.csv'],
#     ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_L/THU_L_hour.csv',
#     'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_L2/THU_L2_hour.csv'],
#     ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_U/THU_U_hour.csv',
#     'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_U2/THU_U2_hour.csv']
#     ]

infile = [
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/NUK_U/NUK_U_hour.csv',
     'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/NUK_Uv3/NUK_Uv3_hour.csv'],
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/NUK_L/NUK_L_hour.csv']]

# Iterate through files
for inf in infile: 
    
    # If one location is represented by two stations
    if len(inf)>1:
        all_df = []
        names = []
        for f in range(len(inf)):
            all_df.append(pd.read_csv(inf[f], comment='#', index_col=0,
                                      na_values=['','nan'], parse_dates=True,
                                      sep=',', 
                                      skip_blank_lines=True))    
            names.append(inf[f].split('/')[-1].split('_hour')[0])
        name = names[0]+' / '+names[1]
        df_hour = all_df[1].combine_first(all_df[0])
    
    # If one location is represented by one station
    else:        
        name = inf[0].split('/')[-1].split('_hour')[0]
        df_hour = pd.read_csv(inf[0], comment='#', index_col=0,
                             na_values=['','nan'], parse_dates=True,
                             sep=',', 
                             skip_blank_lines=True)   

    # Start plot
    print('Plotting '+name)        
    fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3,1]},
                           figsize=(10,5), sharex=True)

    # Define font sizes
    fsize1 = 12
    fsize2 = 10
    fsize3 = 9
    lw=1.

    # Get plotting years
    years = list(range(df_hour.index[0].year, df_hour.index[-1].year))
    y_min=df_hour['t_u'].min()
    y_max=df_hour['t_u'].max()    
    max_pdd=0
    
    # Define color ramp
    colors=['#7e4794','#36b700','#ff73b6','#c701ff','#4ecb8d','#ff9d3a',
            '#f9e858','#d83034','#c8c8c8','#f0c571','#59a89c','#0b81a2',
            '#e25759','#9d2c00']    
    if len(colors)==len(years):
        pass
    elif len(colors)>len(years):
        colors = colors[0:len(years)]
    else:
        while len(years)>len(colors):
            r = lambda: random.randint(0,255)
            colors.append('#%02X%02X%02X' % (r(),r(),r()))
    

    # Plot iteratively over years
    for y in range(len(years)):
        
        # Subset dataframe to years
        date_range = [datetime.date(years[y],1,1), datetime.date(years[y],12,31)]
        doy_range = [d.timetuple()[7] for d in date_range]
        df_subset = df_hour[str(years[y])+'-01-01':str(years[y])+'-12-31']
        
        # Resample daily mean and max
        df_max = df_subset.resample('1D').max()
        df_max['doy'] = df_max.index.dayofyear
        df_max = df_max.set_index('doy')
        df = df_subset.resample('1D').mean()
        df['doy'] = df.index.dayofyear
        df = df.set_index('doy')
        
        # Plot temperature from upper and lower boom values
        if 't_l' in df:
            # df['t'] = pd.concat([df['t_u'], df['t_l']])
            df['t_u'] = df['t_u'].combine_first(df['t_l'])
            
            # df['t'].plot(ax=ax[0], c=colors[y],  linewidth=lw, linestyle='-', 
            #              x_compat=True, label=str(years[y]))
            # df['t_u_std_pos'] = df['t']+df['t'].std()
            # df['t_u_std_neg'] = df['t']-df['t'].std()
            # df['t_zero'] = df['t']
    
        # # Plot temperature from upper boom only
        # else:
        if df['t_u'].isna().sum() < 150:  
            df['t_u'].plot(ax=ax[0], c=colors[y], linestyle='-', linewidth=lw, 
                            x_compat=True, label=str(years[y]))
            df['t_u_std_pos'] = df['t_u']+df['t_u'].std()
            df['t_u_std_neg'] = df['t_u']-df['t_u'].std()
            df['t_zero'] = df['t_u']
        
            # Calculate and plot standard deviation
            ax[0].fill_between(df.index, df['t_u_std_pos'], df['t_u_std_neg'], 
                               color=colors[y], alpha=0.15, label=None)#, label=str(years[y])+' std. dev.')  
            
            # Calculate and plot cumulative PDD
            df["t_zero"].loc[df["t_zero"] <= 0] = 0 
            df["t_zero"].loc[df["t_zero"] > 0] = 1 
            df['t_cum'] = df['t_zero'].cumsum()
            ax[1].plot(list(df.index) , list(df['t_cum']),c=colors[y], linewidth=lw, 
                       linestyle='-')#, label=str(years[y])+' PDD')
            if max_pdd < df['t_cum'].max():
                max_pdd = df['t_cum'].max()
        
 
    df_aver = df_hour.resample('1D').mean()
    df_aver['doy'] = df_aver.index.dayofyear
    df_aver['year'] = df_aver.index.year
    if 't_l' in df_aver:
        df_aver['t_u'] = df_aver['t_u'].combine_first(df_aver['t_l'])    
    
    df_aver = df_aver.loc[(df_aver['doy']>=df.index[0]) & (df_aver['doy']<=df.index[-1])]
    df_aver = df_aver.loc[(df_aver['year']<=years[-1])]
    
    average=[]
    for i in list(range(df.index[0], df.index[-1])):
        d = df_aver[['t_u','doy']].loc[df_aver['doy']==i].mean()
        average.append(d['t_u'])
    
    df_aver2 = pd.DataFrame({'doy':list(range(df.index[0], df.index[-1])),'t_u':average})
    ax[0].plot(list(df_aver2['doy']) , list(df_aver2['t_u']),c='k', linewidth=lw, 
               linestyle='--', label='Average')
        
    # df_aver2 = df_aver[['t_u','doy']].groupby('doy').mean()
    df_aver2['t_zero'] = df_aver2['t_u']
    df_aver2["t_zero"].loc[df_aver2["t_zero"] <= 0] = 0 
    df_aver2["t_zero"].loc[df_aver2["t_zero"] > 0] = 1 
    df_aver2['t_cum'] = df_aver2['t_zero'].cumsum()

    ax[1].plot(list(df_aver2['doy']) , list(df_aver2['t_cum']),c='k', linewidth=lw, 
               linestyle='--')

    
    # Add station as title
    props = dict(boxstyle='round', facecolor='#86BECC', alpha=0.3)
    ax[0].text(0.5, 1.1, name, fontsize=fsize1, horizontalalignment='center', 
                bbox=props, transform=ax[0].transAxes)

    # Format axs
    m0 = math.ceil(y_min / 10.0) * 10   
    m1 = math.ceil(y_max / 10.0) * 10 
    ax[0].set_ylim([m0, m1])
    ax[0].set_ylabel('Daily average air temperature $^\circ$C', fontsize=fsize2, labelpad=10) 

    ax[1].set_ylim([0, max_pdd + 1])
    ax[1].set_ylabel('Cumulative PDD', fontsize=fsize2, labelpad=10)   

    plt.setp(ax[1].get_yticklabels()[-1], visible=False)    
    ax[1].set_xlabel('', fontsize=0)  
    ax[1].set_xticklabels(['01-Jan','01-Feb','01-Mar','01-Apr','01-May', 
                           '01-Jun','01-Jul','01-Aug', '01-Sep', '01-Oct',
                           '01-Nov','01-Dec'], fontsize=fsize2) 

    ticks = [
             datetime.date(years[y], 1, 1).timetuple()[7],
             datetime.date(years[y], 2, 1).timetuple()[7],
             datetime.date(years[y], 3, 1).timetuple()[7],
             datetime.date(years[y], 4, 1).timetuple()[7], 
             datetime.date(years[y], 5, 1).timetuple()[7],
             datetime.date(years[y], 6, 1).timetuple()[7], 
             datetime.date(years[y], 7, 1).timetuple()[7],
             datetime.date(years[y], 8, 1).timetuple()[7], 
             datetime.date(years[y], 9, 1).timetuple()[7],
             datetime.date(years[y], 10, 1).timetuple()[7],
             datetime.date(years[y], 11, 1).timetuple()[7],             
             datetime.date(years[y], 12, 1).timetuple()[7]
             ]  
    
    for a in range(len(ax)):
        ax[a].yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
        ax[a].xaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
        ax[a].set_xticks(ticks)
        ax[a].tick_params(axis='x', which='minor', bottom=False)
        ax[a].tick_params(axis='x', which='major', bottom=False)
        ax[a].set_xlim([date_range[0].timetuple().tm_yday,
                        date_range[1].timetuple().tm_yday])
        # ax[a].yaxis.set_label_coords(-0.07, 0.5)
            
    # Format legend and spacing
    if len(years) > 20:
        fig.legend(fontsize=fsize3, bbox_to_anchor=(0.98, 0.9),ncol=2)
        plt.subplots_adjust(wspace=1, hspace=0, left=0.1, right=0.75)
    else:
        fig.legend(fontsize=fsize3, bbox_to_anchor=(0.98, 0.9))
        plt.subplots_adjust(wspace=1, hspace=0, left=0.1, right=0.85)
    
    # Show and save
    fig.align_ylabels(ax)
    plt.show()
    plt.savefig(name.split('/')[0]+'_all_years_temperature.jpg', dpi=300)