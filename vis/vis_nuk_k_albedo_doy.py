#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 08:34:09 2022

@author: pho
"""
import math,datetime,random
import pandas as pd
import matplotlib.pyplot as plt

# Define station file location
infile = 'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/NUK_K/NUK_K_hour.csv'

# Load file     
name = infile.split('/')[-1].split('_hour')[0]
df_hour = pd.read_csv(infile, comment='#', index_col=0,
                     na_values=['','nan'], parse_dates=True,
                     sep=',', 
                     skip_blank_lines=True)   

# Define font sizes
fsize1 = 12
fsize2 = 10
fsize3 = 9
lw=1.

# Get plotting years
years = list(range(df_hour.index[0].year, df_hour.index[-1].year))
y_min=0
y_max=1   
max_pdd=0

# Define color ramp
colors=['#7e4794','#36b700','#ff73b6','#c701ff','#4ecb8d','#ff9d3a',
        '#f9e858','#d83034','#c8c8c8','#f0c571']  


# Start plot
print('Plotting '+name)        
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,5), sharex=True)

# Plot iteratively over years
for y in range(len(years)):
    
    # Subset dataframe to years
    date_range = [datetime.date(years[y],5,1), datetime.date(years[y],9,1)]
    doy_range = [d.timetuple()[7] for d in date_range]
    df_subset = df_hour[str(years[y])+'-04-01':str(years[y])+'-10-01']
    
    # Resample albedo to daily mean
    df_mean = df_subset.resample('1D').mean()
    df_mean['doy'] = df_mean.index.dayofyear
    df_mean = df_mean.set_index('doy')

    # Filter for 10 AM to 11 AM
    df_1011 = df_subset.between_time('10:00', '11:00')
    df_1011 = df_1011.resample('1D').mean()
    df_1011['doy'] = df_1011.index.dayofyear
    df_1011 = df_1011.set_index('doy')
    
    # Plot daily average albedo 
    # else:
    if df_mean['albedo'].isna().sum() < 150:  
        df_mean['albedo'].plot(ax=ax1, c=colors[y], linestyle='-', linewidth=lw, 
                        x_compat=True, label=str(years[y]))
        df_mean['albedo_std_pos'] = df_mean['albedo']+df_mean['albedo'].std()
        df_mean['albedo_std_neg'] = df_mean['albedo']-df_mean['albedo'].std()
    
        # Calculate and plot standard deviation
        ax1.fill_between(df_mean.index, df_mean['albedo_std_pos'], df_mean['albedo_std_neg'], 
                           color=colors[y], alpha=0.15, label=None)# label=str(years[y])+' std. dev.')  

    # Plot 10-11am average albedo 
    if df_1011['albedo'].isna().sum() < 150:  
        df_1011['albedo'].plot(ax=ax2, c=colors[y], linestyle='-', linewidth=lw, 
                        x_compat=True, label=str(years[y]))
        df_1011['albedo_std_pos'] = df_1011['albedo']+df_1011['albedo'].std()
        df_1011['albedo_std_neg'] = df_1011['albedo']-df_1011['albedo'].std()
    
        # Calculate and plot standard deviation
        ax2.fill_between(df_1011.index, df_1011['albedo_std_pos'], df_1011['albedo_std_neg'], 
                           color=colors[y], alpha=0.15, label=None)# label=str(years[y])+' std. dev.')  

# Add texts
props = dict(boxstyle='round', facecolor='#86BECC', alpha=0.3)
ax1.text(0.5, 1.1, name, fontsize=fsize1, horizontalalignment='center', 
            bbox=props, transform=ax1.transAxes)
ax1.text(0.03, 0.1, 'Daily average albedo', fontsize=fsize1, horizontalalignment='left', 
            bbox=props, transform=ax1.transAxes)
ax2.text(0.03, 0.1, '10-11am average albedo', fontsize=fsize1, horizontalalignment='left', 
            bbox=props, transform=ax2.transAxes)

# Format axs
ax1.set_ylabel('In situ albedo', fontsize=fsize2, labelpad=10) 
ax2.set_ylabel('In situ albedo', fontsize=fsize2, labelpad=10) 

ax2.set_xticklabels(['01-May', '01-Jun', '01-Jul','01-Aug', '01-Sep'], fontsize=fsize2) 
ticks = [datetime.date(years[y], 5, 1).timetuple()[7],
         datetime.date(years[y], 6, 1).timetuple()[7], 
         datetime.date(years[y], 7, 1).timetuple()[7],
         datetime.date(years[y], 8, 1).timetuple()[7], 
         datetime.date(years[y], 9, 1).timetuple()[7]] 
yticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
ax1.set_yticklabels(['','0.2','0.4','0.6','0.8','1.0']) 
ax2.set_yticklabels(['0.0','0.2','0.4','0.6','0.8','1.0']) 
 
for ax in [ax1,ax2]:
    ax.set_ylim([0, 1])
    ax.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
    ax.xaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
    ax.set_xticks(ticks)
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.tick_params(axis='x', which='major', bottom=False)
    ax.set_xlim([date_range[0].timetuple().tm_yday,
                    date_range[1].timetuple().tm_yday])
    fig.align_ylabels(ax)

      
ax2.legend(fontsize=fsize3, bbox_to_anchor=(1.01, 1.6))
plt.subplots_adjust(wspace=1, hspace=0, left=0.1, right=0.75)

# Show and save
plt.show()
plt.savefig(name.split('/')[0]+'_albedo_average_doy.jpg', dpi=300)
