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
infile = "https://thredds.geus.dk/thredds/fileServer/aws/l3sites/csv/hour/NUK_K_hour.csv"

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
fig, ax1 = plt.subplots(1, figsize=(15,5))
  
# Resample albedo to daily mean
df_mean = df_hour.resample('1D').mean()

# Filter for 10 AM to 11 AM
df_1011 = df_hour.between_time('09:55', '11:05')
df_1011 = df_1011.resample('1D').mean()

# Calculate moving averages
window_size=7
df_mean['albedo_moving_avg'] = df_mean['albedo'].rolling(window=window_size).mean()
df_1011['albedo_moving_avg'] = df_1011['albedo'].rolling(window=window_size).mean()


# Plot daily average albedo 
# df_mean['albedo'].plot(ax=ax1, c=colors[0], linestyle='-', linewidth=lw, 
#                 x_compat=True, label='Daily average albedo')
df_mean['albedo_moving_avg'].plot(ax=ax1, c=colors[0], linestyle='-', linewidth=lw, 
                                  label='Daily average albedo')


# Plot 10-11am average albedo  
# df_1011['albedo'].plot(ax=ax1, c=colors[1], linestyle='-', linewidth=lw, 
#                 x_compat=True, label='10-11am average albedo')
df_1011['albedo_moving_avg'].plot(ax=ax1, c=colors[1], linestyle='-', linewidth=lw, 
                                  label='10-11am average albedo')


# Add texts
props = dict(boxstyle='round', facecolor='#86BECC', alpha=0.3)
ax1.text(0.5, 1.1, name, fontsize=fsize1, horizontalalignment='center', 
            bbox=props, transform=ax1.transAxes)

# Format axs
ax1.set_ylabel(f'In situ albedo ({window_size}-day moving average)', fontsize=fsize2, labelpad=10)  

ticks = [datetime.date(2014, 1, 1),
         datetime.date(2015, 1, 1), 
         datetime.date(2016, 1, 1),
         datetime.date(2017, 1, 1), 
         datetime.date(2018, 1, 1),
         datetime.date(2019, 1, 1), 
         datetime.date(2020, 1, 1),
         datetime.date(2021, 1, 1),
         datetime.date(2022, 1, 1), 
         datetime.date(2023, 1, 1),
         datetime.date(2024, 1, 1)]       
ax1.set_xlim([ticks[0], ticks[-1]])
ax1.set_xticks(ticks)
ax1.set_xticklabels(['2014','2015','2016','2017','2018','2019','2020','2021',
                     '2022','2023','2024'], fontsize=fsize2) 
 
ax1.set_ylim([0, 1])
ax1.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
ax1.xaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)

ax1.tick_params(axis='x', which='minor', bottom=False)

fig.align_ylabels(ax1)

      
ax1.legend(loc=4, fontsize=fsize3)

# Show and save
plt.show()
plt.savefig(name.split('/')[0]+'_albedo_average_all.png', dpi=300)

