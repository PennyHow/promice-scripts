#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 08:34:09 2022

@author: pho
"""
import math,datetime,random
import pandas as pd
import matplotlib.pyplot as plt

# Define station name
name = "NUK_K"              # Asiaq QAS station
#name = "NUK_L"             # Nuuk lower ice sheet station

time_res = "day"            # hour / day / month


# Define station file location
infile = "https://thredds.geus.dk/thredds/fileServer/aws/l3sites/csv/" + time_res + "/" + name + "_" + time_res + ".csv"

# Load file     
df_hour = pd.read_csv(infile, comment='#', index_col=0,
                     na_values=['','nan'], parse_dates=True,
                     sep=',', 
                     skip_blank_lines=True)   

# Define font sizes
fsize1 = 12
fsize2 = 10
fsize3 = 9
lw=1.

# Start plot
print('Plotting '+name)        
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(10,5), sharex=True)

ax1.plot(df_hour.index, df_hour['t_u'])
ax2.plot(df_hour.index, df_hour['albedo'])
ax3.plot(df_hour.index, df_hour['snow_height'])
ax4.plot(df_hour.index, df_hour['z_boom_u'])
ax5.plot(df_hour.index, df_hour['cc'])
    
plt.legend(fontsize=fsize3, bbox_to_anchor=(1.01, 1.6))
plt.subplots_adjust(wspace=1, hspace=0, left=0.1, right=0.75)

# Show and save
plt.show()
#plt.savefig(name.split('/')[0]+'_snow_cover_vars.jpg', dpi=300)
