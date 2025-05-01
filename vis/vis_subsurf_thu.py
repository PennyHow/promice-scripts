#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:15:18 2024

@author: pho
"""

import glob
import xarray as xr
import pandas as pd
import datetime, sys
import matplotlib.pyplot as plt

infile = [
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_L/THU_L_day.csv',
    'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_L2/THU_L2_day.csv'],
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_U/THU_U_day.csv',
    'https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/THU_U2/THU_U2_day.csv']
    ]

all_names = []
dfs = []
for inf in infile: 
    if len(inf)>1:
        all_df = []
        names = []
        for f in range(len(inf)):
            all_df.append(pd.read_csv(inf[f], comment='#', index_col=0,
                                      na_values=['','nan'], parse_dates=True,
                                      sep=',', 
                                      skip_blank_lines=True))    
            names.append(inf[f].split('/')[-1].split('_day')[0])
        name = names[0]+' '+names[1]
        df = pd.concat(all_df)
    else:        
        name = inf[0].split('/')[-1].split('_day')[0]
        df = pd.read_csv(inf[0], comment='#', index_col=0,
                             na_values=['','nan'], parse_dates=True,
                             sep=',', 
                             skip_blank_lines=True)   

    print('Loaded '+name)
    all_names.append(name)
    dfs.append(df)


# plt.figure(figsize=(w, h), dpi=d)
fig, ax = plt.subplots(2, 1, figsize=(10,5), sharex=True)
fsize1 = 9
fsize2 = 10
fsize3 = 12
fsize4 = 14
fsty = 'arial'
pad=1.
lloc=4
lw=1

for i in range(len(dfs)):

    # Fourth plot
    clrs = [None, '#FF0018', '#FFA52C', '#FFFF41', '#008018','#0000F9', '#86007D', '#5BCEFA', '#F5A9B8', '#FFF200', '#8548A6']
    for r in list(range(1,11)):
        n = 't_i_' + str(r)
        if n in dfs[i]:

            window_size = 2
            numbers_series = dfs[i][n]
            windows = numbers_series.rolling(window_size)
            
            dfs[i][n+'_rolling'] = windows.mean()
            dfs[i][n+'_rolling'].plot(ax=ax[i], c=clrs[r], linewidth=lw, 
                                      label= str(r) + ' m subsurf. temp.')
            
    ax[i].set_ylim([-30, 10])  
    ax[i].set_yticks([-30,-20,-10,0,10])
    if i == range(len(dfs))[0]:
        ax[i].set_yticklabels(['-30','-20','-10','0','10']) 
    else:
        ax[i].set_yticklabels(['-30','-20','-10','0','']) 
    # ax[i].legend(loc=lloc, ncol=2, fontsize=fsize2, bbox_to_anchor=(1.285, -0.07))
    ax[i].set_xlim([datetime.date(2010,1,1), datetime.date(2024,1,1)])
    ax[i].minorticks_off()

    props = dict(boxstyle='round', facecolor='#FFEAB0', alpha=0.7)
    ax[i].text(datetime.date(2010,4,1), 3, all_names[i], fontsize=fsize2, 
           horizontalalignment='left', bbox=props)#, transform=ax[2].transAxes)
    ax[i].set_xlabel('', fontsize=0)


for a in ax:
    a.yaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)
    a.xaxis.grid(color='gray', linestyle='dashed', linewidth=0.5)

    a1=a.twinx()
    lims = a.get_ylim()
    a1.set_ylim(lims)
    tx = a.get_yticks()
    lab = a.get_yticklabels()
    a1.set_yticks(tx)
    a1.set_yticklabels(lab, fontsize=fsize2)

    a.tick_params(which='both', labelsize=fsize2)    
    a1.tick_params(which='both', labelsize=fsize2)  
    
ax[1].legend(bbox_to_anchor=(0.5, -0.43), loc='center', ncol=4)    
    
    # for i in list(range(df.index[0].date().year,df.index[-1].date().year)):
    #     a.vlines(x=datetime.date(i,1,1),ymin=lims[0], ymax=lims[1], linewidth=1, color='#636363')

fig.text(0.06, 0.5, 'Subsurface temperature $^\circ$C', va='center', rotation='vertical', fontsize=fsize3)
fig.text(0.94, 0.5, 'Subsurface temperature $^\circ$C', va='center', rotation=270, fontsize=fsize3)

plt.subplots_adjust(wspace=1,hspace=0)#, left=0.1, right=0.75)
plt.show()
plt.savefig('subsurface_data_thu.jpg', dpi=300)