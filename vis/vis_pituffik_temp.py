#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 08:34:09 2022

@author: pho
"""
import math,datetime
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

infile = [
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/CEN1/CEN1_hour.csv',
    'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/CEN2/CEN2_hour.csv'],
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/HUM/HUM_hour.csv'],
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/NEM/NEM_hour.csv'],
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_L/THU_L_hour.csv',
    'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_L2/THU_L2_hour.csv'],
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_U/THU_U_hour.csv',
    'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_U2/THU_U2_hour.csv']
    ]

for inf in infile: 
    if len(inf)>1:
        all_df = []
        names = []
        for f in range(len(inf)):
            all_df.append(pd.read_csv(inf[f], comment='#', index_col=0,
                                      na_values=['','nan'], parse_dates=True,
                                      sep=',', 
                                      skip_blank_lines=True))    
            names.append(inf[f].split('/')[-1].split('_hour')[0])
        name = names[0]+' '+names[1]
        # df_hour = pd.concat(all_df)
        df_hour = all_df[1].combine_first(all_df[0])
    else:        
        name = inf[0].split('/')[-1].split('_hour')[0]
        df_hour = pd.read_csv(inf[0], comment='#', index_col=0,
                             na_values=['','nan'], parse_dates=True,
                             sep=',', 
                             skip_blank_lines=True)   


    year = 2022
    date_range = [datetime.date(year,3,15), datetime.date(year,10,15)]
    df_hour = df_hour[str(year)+'-03-15':str(year)+'-10-15']

    print('Plotting '+name)

    
    # plt.figure(figsize=(w, h), dpi=d)
    fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3,1]},
                           figsize=(10,5), sharex=True)
    
    fsize1 = 12
    fsize2 = 10
    fsize3 = 9
    fsty = 'arial'
    pad=1.
    lloc=2
    lw=1
    
    color1 = '#1a80bb'
    color2 = '#a00000'
    color3 = '#707070'
    
    df_max = df_hour.resample('1D').max()
    df = df_hour.resample('1D').mean()
    
    # Plot temperature
    if 't_l' in df:
        # df['t'] = pd.concat([df['t_u'], df['t_l']])
        df['t'] = df['t_u'].combine_first(df['t_l'])
        df['t'].plot(ax=ax[0], c=color1,  linewidth=lw, linestyle='-', 
                     x_compat=True, label='Aver. daily temperature')

        df_max['t'] = df_max['t_u'].combine_first(df_max['t_l'])
        df_max['t'].plot(ax=ax[0], c=color3,  linewidth=lw, linestyle='--', 
                          x_compat=True, label='Max. daily temperature')
        
        # df['t_u_std'] = df['t'].rolling(30).std()
        df['t_u_std_pos'] = df['t']+df['t'].std()
        df['t_u_std_neg'] = df['t']-df['t'].std()
        df['t_zero'] = df['t']

    else:
        df['t_u'].plot(ax=ax[0], c=color1, linestyle='-', linewidth=lw, 
                       x_compat=True, label='Aver. daily temperature')
        df_max['t_u'].plot(ax=ax[0], c=color3, linestyle='--', linewidth=lw, 
                            x_compat=True, label='Max. daily temperature')
        
        # df['t_u_std'] = df['t_u'].rolling(30).std()
        df['t_u_std_pos'] = df['t_u']+df['t_u'].std()
        df['t_u_std_neg'] = df['t_u']-df['t_u'].std()
        df['t_zero'] = df['t_u']

    m2 = math.ceil(df['t_u_std_pos'].max() / 10.0) * 10    
    m1 = math.floor(df['t_u_std_neg'].min() / 10.0) * 10 
    ax[0].set_ylim([m1, m2])

    # Calculate and plot standard deviation
    ax[0].fill_between(df.index, df['t_u_std_pos'], df['t_u_std_neg'], 
                       color=color1, alpha=0.2, label='Standard deviation')  
    
    # Calculate and plot cumulative PDD
    df.loc[df["t_zero"] <= 0] = 0 
    df.loc[df["t_zero"] > 0] = 1 
    df['t_cum'] = df['t_zero'].cumsum()
    df['t_cum'].plot(ax=ax[1], c=color2, linewidth=lw, linestyle='-', 
                     x_compat=True, label='Cumulative Positive Degree Days')

    # Add station as title
    props = dict(boxstyle='round', facecolor='#CAA84F', alpha=0.3)
    ax[0].text(0.5, 1.1, name, fontsize=fsize1, horizontalalignment='center', 
                bbox=props, transform=ax[0].transAxes)


    # Format ax0
    ax[0].set_ylabel('Air temperature $^\circ$C', fontsize=fsize2, labelpad=9)
    # ax[0].set_ylim([-50, 10])
    # ax[0].set_yticks([-50,-40,-30,-20,-10,0,10])
    ax[0].legend(loc=lloc, fontsize=fsize3)

    # Format ax1
    # m = math.ceil(df['t_cum'].max() / 10.0) * 10    
    ax[1].set_ylim([0, df['t_cum'].max() + 1])
    ax[1].set_ylabel('Cumulative count', fontsize=fsize2, labelpad=15)   
    ax[1].set_xlabel('', fontsize=0)  
    ax[1].legend(loc=lloc, fontsize=fsize3)
    ax[1].text(0.5, -0.65, str(year), fontsize=fsize1, 
               transform=ax[0].transAxes, horizontalalignment='center')
     
    ax[1].set_xticklabels(['01-Apr', '01-May', '01-Jun', '01-Jul',
                           '01-Aug', '01-Sep', '01-Oct'], fontsize=fsize2)        
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
 
    ticks = [datetime.date(year, 4, 1), datetime.date(year, 5, 1),
             datetime.date(year, 6, 1), datetime.date(year, 7, 1),
             datetime.date(year, 8, 1), datetime.date(year, 9, 1),
             datetime.date(year, 10, 1)]  
    
    # Add grid
    for a in ax:
        a.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
        a.xaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
        a.set_xticks(ticks)
        a.tick_params(axis='x', which='minor', bottom=False)
    ax[0].tick_params(axis='x', which='major', bottom=False)
    
    plt.subplots_adjust(wspace=1, hspace=0.1)#, left=0.1, right=0.75)
    plt.show()
    plt.savefig(name+'_'+str(year)+'_temperature.jpg', dpi=300)
