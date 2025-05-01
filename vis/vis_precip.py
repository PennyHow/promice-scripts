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
inf = [
       # 'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/NUK_U/NUK_U_hour.csv',
       'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/NUK_Uv3/NUK_Uv3_hour.csv'
       ]




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
    df = all_df[1].combine_first(all_df[0])

# If one location is represented by one station
else:        
    name = inf[0].split('/')[-1].split('_hour')[0]
    df = pd.read_csv(inf[0], comment='#', index_col=0,
                         na_values=['','nan'], parse_dates=True,
                         sep=',', 
                         skip_blank_lines=True)   
df['time_plt'] = df.index
# Start plot
print('Plotting '+name)        
fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3,1]},
                       figsize=(10,5), sharex=True)

# Define font sizes
fsize1 = 12
fsize2 = 10
fsize3 = 9
lw=2.
pad=1.
lloc=2
lw=1

# Define color ramp
colors=['#4A009D','#00709D']
          
# Cum. precip
df['precip_u_cor'].plot(ax=ax[0], c=colors[0], linewidth=lw, label='Cumulative precipitation')

ax[0].set_ylim([0, 1000])
ax[0].set_yticks([0,200,400,600, 800, 1000])
ax[0].set_yticklabels(['0','200','400','600','800','1000'],fontsize=fsize2)
ax[0].legend(loc=lloc, fontsize=fsize2)    

# Precip rate
df['precip_u_rate'].plot(ax=ax[1], color=colors[1], linewidth=lw, label='Precipitation rate')
ax[1].set_ylim([0, 40])
ax[1].set_yticks([0,10,20,30,40])
ax[1].set_yticklabels(['0','10','20','30','40'],fontsize=fsize2)
# ax[1].yaxis.set_label_coords(-0.07, 0.5)
ax[1].set_xlabel('', fontsize=0)

ax[0].set_ylabel('Precipitation (mm)', fontsize=fsize1, labelpad=pad)
ax[0].yaxis.set_label_coords(-0.07, 0.3)

props = dict(boxstyle='round', facecolor=colors[0], alpha=0.1)
ax[0].text(0.5, 1.1, name, fontsize=fsize1, horizontalalignment='center', 
           bbox=props, transform=ax[0].transAxes)

# Grids
for a in range(len(ax)):
    ax[a].yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
    ax[a].xaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
    lims = ax[a].get_ylim()

    # Station visits
    ax[a].vlines(x=datetime.date(2022,8,15),ymin=lims[0], ymax=lims[1], 
                 linewidth=2, color='#636363', alpha=0.5,label='Station visit (precip reset)')
    ax[a].vlines(x=datetime.date(2023,8,22),ymin=lims[0], ymax=lims[1], 
                 linewidth=2, color='#636363', alpha=0.5)
    ax[a].vlines(x=datetime.date(2023,9,15),ymin=lims[0], ymax=lims[1], 
                 linewidth=2, color='#636363', alpha=0.5)

ax[0].legend(loc=lloc, fontsize=fsize3) 
ax[1].legend(loc=lloc, fontsize=fsize3)         

# Show and save
fig.align_ylabels(ax)
plt.show()
plt.savefig(name.split('/')[0]+'_all_years_precip.jpg', dpi=300)