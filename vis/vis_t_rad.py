#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 08:34:09 2022

@author: pho
"""
import glob
import xarray as xr
import pandas as pd
import datetime, sys
import matplotlib.pyplot as plt

infile = [
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/HUM/HUM_hour.csv'],
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/NEM/NEM_hour.csv'],
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/EGP/EGP_hour.csv'],
    ['https://thredds.geus.dk/thredds/fileServer/aws_l3_station_csv/level_3/TUN/TUN_hour.csv']
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
            names.append(inf[f].split('/')[-1].split('_hour')[0])
        name = names[0]+' '+names[1]
        df = pd.concat(all_df)
    else:        
        name = inf[0].split('/')[-1].split('_hour')[0]
        df = pd.read_csv(inf[0], comment='#', index_col=0,
                             na_values=['','nan'], parse_dates=True,
                             sep=',', 
                             skip_blank_lines=True)   


    print('Loaded '+name)
    all_names.append(name)
    dfs.append(df)


# plt.figure(figsize=(w, h), dpi=d)
fig, ax = plt.subplots(8, 1, figsize=(10,10), 
                       gridspec_kw={'height_ratios': [3,1, 3,1, 3,1, 3,1]}, sharex=True)
fsize1 = 9
fsize2 = 10
fsize3 = 12
fsize4 = 14
fsty = 'arial'
pad=1.
lloc=4
lw=0.8

for i in range(len(dfs)):

    # Fourth plot
    clrs = ['#1a80bb', '#b8b8b8', '#ea801c']

    dfs[i]['t_u'].plot(ax=ax[i*2], c=clrs[0], linewidth=lw, label= 't_u')
    if 't_l' in dfs[i]:
        dfs[i]['t_l'].plot(ax=ax[i*2], c=clrs[1], linewidth=lw, label= 't_l')        
    dfs[i]['t_rad'].plot(ax=ax[i*2], c=clrs[2], linewidth=lw, label= 't_rad')
    ax[i*2].set_ylim([-60, 15])  
    ax[i*2].set_yticks([-60,-45,-30,-15,0, 15])
    if i == range(len(dfs))[0]:
        ax[i*2].set_yticklabels(['-60','-45','-30','-15','0', '15']) 
    else:
        ax[i*2].set_yticklabels(['-60','-45','-30','-15','0', '']) 
    # ax[i].legend(loc=lloc, ncol=2, fontsize=fsize2, bbox_to_anchor=(1.285, -0.07))
    ax[i*2].set_xlim([datetime.date(2021,1,1), datetime.date(2024,1,1)])

    props = dict(boxstyle='round', facecolor='#FFEAB0', alpha=0.7)
    ax[i*2].text(datetime.date(2022,6,15), 0, all_names[i], fontsize=fsize2, 
           horizontalalignment='left', bbox=props)#, transform=ax[2].transAxes)
    ax[i*2].set_xlabel('', fontsize=0)

    if 't_l' in dfs[i]:
        dfs[i]['t_l_diff'] = dfs[i]['t_l']-dfs[i]['t_rad']
        dfs[i]['t_l_diff'].plot(ax=ax[i*2+1], c=clrs[1], linewidth=lw, label= 'Difference (t_l - t_rad)')
        
    dfs[i]['t_u_diff'] = dfs[i]['t_u']-dfs[i]['t_rad']
    dfs[i]['t_u_diff'].plot(ax=ax[i*2+1], c='k', linewidth=lw, label= 'Difference (t_u - t_rad)')

    ax[i*2+1].set_ylim([-10, 10])  
    ax[i*2+1].set_yticks([-10,0,10])
    ax[i*2+1].set_yticklabels(['-10','0','']) 
    ax[i*2+1].set_xlabel('', fontsize=0)
        
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
 
handles1, labels1 = ax[0].get_legend_handles_labels() 
handles2, labels2 = ax[1].get_legend_handles_labels() 
for h,l in zip(handles2, labels2):
    handles1.append(h)
    labels1.append(l)
ax[0].legend(handles1, labels1, bbox_to_anchor=(0.5, 1.1), loc='center', ncol=5)    
    
plt.subplots_adjust(wspace=1, hspace=0)#, left=0.1, right=0.75)
plt.show()
plt.savefig('t_rad_compare.jpg', dpi=300)
