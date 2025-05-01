#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 09:58:22 2023

@author: pho
"""
import xarray as xr
import pandas as pd
import datetime
from pathlib import Path
import matplotlib.pyplot as plt

indir = '/home/pho/Downloads/'
name = ['CEN2','CP1','DY2','HUM','JAR','NAE','NAU','NEM','NSE','SDM','SWC','TUN']

files = [Path(indir).joinpath(n+'.csv') for n in name]
plot_size = len(files)
fig, ax = plt.subplots(plot_size, 1, figsize=(10,10), sharex=True)
props = dict(boxstyle='round', facecolor='#FFFFFF', edgecolor='#DFDFDF', alpha=0.8)

fsize1 = 9
fsize2 = 8
fsize3 = 10
fsize4 = 12
fsty = 'arial'
pad = 1.
lloc = 4
lw = 1

for f in range(len(files)):    
    df = pd.read_csv(files[f], comment='#', index_col=0,
                     na_values=['','nan'], parse_dates=True,
                     sep=',', skip_blank_lines=True) 
    
    df['time'] = df.index
    df1 = df.groupby(pd.PeriodIndex(df['time'], freq='M'))['t_u'].mean()       
    df2 = df.groupby(pd.PeriodIndex(df['time'], freq='M'))['t_l'].mean()  
   
    # Plot temperature
    df1.plot(ax=ax[f], c='#3FC0D7', linestyle='-', linewidth=lw, label='Upper temperature')
    df2.plot(ax=ax[f], c='#3F8BD7',  linewidth=lw, linestyle='-', label='Lower temperature')
    rolling1 =df1.rolling(12).mean()
    rolling2 =df2.rolling(12).mean()
    rolling1.plot(ax=ax[f], c='#000000', linewidth=lw, linestyle='--', label='Moving average')
    rolling2.plot(ax=ax[f], c='#000000', linewidth=lw, linestyle='--', label='_t_l')
    
    # Plotting formatting
    ax[f].set_ylim([-40, 20])
    ax[f].set_yticks([-40,-20,0,20])
    ax[f].set_yticklabels(['','-20','0',''], fontsize=fsize3)

    ax[f].set_xlim([datetime.date(1995,1,1), datetime.date(2024,1,1)])    
    ax[f].set_xticks([datetime.date(1996,1,1), datetime.date(1998,1,1), 
                      datetime.date(2000,1,1), datetime.date(2002,1,1), 
                      datetime.date(2004,1,1),
                      datetime.date(2006,1,1), datetime.date(2008,1,1),
                      datetime.date(2010,1,1), datetime.date(2012,1,1),
                      datetime.date(2014,1,1), datetime.date(2016,1,1),
                      datetime.date(2018,1,1), datetime.date(2020,1,1),
                      datetime.date(2022,1,1), datetime.date(2024,1,1)])

    # ax[f].text(1.2, -3.8, 'Active since: June 2021\n\nPosition: 63.15, -44.82\n\nStation design: Two-boom\n\nNr. transmissions: 20.000\n\nData type: RAW/TX\n\nLast visit: 2023-06-11', fontsize=fsize2, horizontalalignment='center', 
    #         bbox=props, transform=ax[0].transAxes)


    ax[f].text(datetime.date(2024,6,1), -20, name[f], fontsize=fsize4, bbox=props)
 
    ax[f].set_xlabel('', fontsize=0)
    ax[f].set_ylabel('', fontsize=0)
    
    ax[f].grid(True)
    ax[f].set_axisbelow(True)
    
ax[-1].set_xticklabels(['1996','1998','2000','2002','2004','2006','2008',
                       '2010','2012','2014','2016','2018','2020','2022',''], 
                       rotation=45, fontsize=fsize3)
ax[-1].set_xlabel('Date', fontsize=fsize4)

ax[-1].text(datetime.date(1992,6,1), 250,'Air temperature $^\circ$C', fontsize=fsize4, rotation=90)
ax[-1].legend(loc=lloc, fontsize=fsize3, ncol=4, bbox_to_anchor=(0.95,-1.6))

a1 = ax[0].twiny()
a1.set_xlim([datetime.date(1995,1,1), datetime.date(2024,1,1)])
a1.set_xticks([datetime.date(1996,1,1), datetime.date(1998,1,1), 
                  datetime.date(2000,1,1), datetime.date(2002,1,1), 
                  datetime.date(2004,1,1),
                  datetime.date(2006,1,1), datetime.date(2008,1,1),
                  datetime.date(2010,1,1), datetime.date(2012,1,1),
                  datetime.date(2014,1,1), datetime.date(2016,1,1),
                  datetime.date(2018,1,1), datetime.date(2020,1,1),
                  datetime.date(2022,1,1), datetime.date(2024,1,1)])
a1.set_xticklabels(['1996','1998','2000','2002','2004','2006','2008',
                    '2010','2012','2014','2016','2018','2020','2022',''], 
                    rotation=45, fontsize=fsize3)
plt.subplots_adjust(wspace=1,hspace=0, left=0.1, right=0.75)

plt.savefig('/home/pho/Desktop/L4_data_temperature.jpg', dpi=300)


for f in range(len(files)):    
    df = pd.read_csv(files[f], comment='#', index_col=0,
                     na_values=['','nan'], parse_dates=True,
                     sep=',', skip_blank_lines=True) 
    
    df['time'] = df.index
    df1 = df.groupby(pd.PeriodIndex(df['time'], freq='M'))['t_u'].mean()       
    df2 = df.groupby(pd.PeriodIndex(df['time'], freq='M'))['t_l'].mean()  
   
    # Plot temperature
    df1.plot(ax=ax[f], c='#3FC0D7', linestyle='-', linewidth=lw, label='Upper temperature')
    df2.plot(ax=ax[f], c='#3F8BD7',  linewidth=lw, linestyle='-', label='Lower temperature')
    rolling1 =df1.rolling(12).mean()
    rolling2 =df2.rolling(12).mean()
    rolling1.plot(ax=ax[f], c='#000000', linewidth=lw, linestyle='--', label='Moving average')
    rolling2.plot(ax=ax[f], c='#000000', linewidth=lw, linestyle='--', label='_t_l')
    
    # Plotting formatting
    ax[f].set_ylim([-40, 20])
    ax[f].set_yticks([-40,-20,0,20])
    ax[f].set_yticklabels(['','-20','0',''], fontsize=fsize3)

    ax[f].set_xlim([datetime.date(1995,1,1), datetime.date(2024,1,1)])    
    ax[f].set_xticks([datetime.date(1996,1,1), datetime.date(1998,1,1), 
                      datetime.date(2000,1,1), datetime.date(2002,1,1), 
                      datetime.date(2004,1,1),
                      datetime.date(2006,1,1), datetime.date(2008,1,1),
                      datetime.date(2010,1,1), datetime.date(2012,1,1),
                      datetime.date(2014,1,1), datetime.date(2016,1,1),
                      datetime.date(2018,1,1), datetime.date(2020,1,1),
                      datetime.date(2022,1,1), datetime.date(2024,1,1)])

    # ax[f].text(1.2, -3.8, 'Active since: June 2021\n\nPosition: 63.15, -44.82\n\nStation design: Two-boom\n\nNr. transmissions: 20.000\n\nData type: RAW/TX\n\nLast visit: 2023-06-11', fontsize=fsize2, horizontalalignment='center', 
    #         bbox=props, transform=ax[0].transAxes)


    ax[f].text(datetime.date(2024,6,1), -20, name[f], fontsize=fsize4, bbox=props)
 
    ax[f].set_xlabel('', fontsize=0)
    ax[f].set_ylabel('', fontsize=0)
    
    ax[f].grid(True)
    ax[f].set_axisbelow(True)
    
ax[-1].set_xticklabels(['1996','1998','2000','2002','2004','2006','2008',
                       '2010','2012','2014','2016','2018','2020','2022',''], 
                       rotation=45, fontsize=fsize3)
ax[-1].set_xlabel('Date', fontsize=fsize4)

ax[-1].text(datetime.date(1992,6,1), 250,'Air temperature $^\circ$C', fontsize=fsize4, rotation=90)
ax[-1].legend(loc=lloc, fontsize=fsize3, ncol=4, bbox_to_anchor=(0.95,-1.6))

a1 = ax[0].twiny()
a1.set_xlim([datetime.date(1995,1,1), datetime.date(2024,1,1)])
a1.set_xticks([datetime.date(1996,1,1), datetime.date(1998,1,1), 
                  datetime.date(2000,1,1), datetime.date(2002,1,1), 
                  datetime.date(2004,1,1),
                  datetime.date(2006,1,1), datetime.date(2008,1,1),
                  datetime.date(2010,1,1), datetime.date(2012,1,1),
                  datetime.date(2014,1,1), datetime.date(2016,1,1),
                  datetime.date(2018,1,1), datetime.date(2020,1,1),
                  datetime.date(2022,1,1), datetime.date(2024,1,1)])
a1.set_xticklabels(['1996','1998','2000','2002','2004','2006','2008',
                    '2010','2012','2014','2016','2018','2020','2022',''], 
                    rotation=45, fontsize=fsize3)
plt.subplots_adjust(wspace=1,hspace=0, left=0.1, right=0.75)

plt.savefig('/home/pho/Desktop/L4_data.jpg', dpi=300)