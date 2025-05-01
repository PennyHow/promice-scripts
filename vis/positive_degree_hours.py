#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 14:34:36 2023

@author: pho
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

def findNames(url):
    response = requests.get(url)
    data = response.text
    lines = data.split('\n')
    for l in lines:
        if 'database_fields' in l:
            names = l.split('= ')[-1].split(',')
            return names



# Get GC-Net legacy datasets urls
# Choose filenames from here: https://github.com/GEUS-Glaciology-and-Climate/GC-Net-level-1-data-processing/tree/main/L1
names = ['08-DYE2.csv', '10-Saddle.csv', '15-NASA-SE.csv', 
         '21-PetermannGlacier.csv', '22-PetermannELA.csv']
urls = ['https://raw.githubusercontent.com/GEUS-Glaciology-and-Climate/GC-Net-level-1-data-processing/main/L1/'+n for n in names]

# Get GEUS PROMICE and GC-NET dataset urls
# Choose standard station names
other = ['SDL', 'NSE']
f = pd.read_csv('https://raw.githubusercontent.com/GEUS-Glaciology-and-Climate/pypromice/main/src/pypromice/data_urls.csv')
for i,r in f.iterrows():
    for o in other:
        if o.lower() in r['data_name']:
            names.append(r['data_name'])
            urls.append(r['data_url'])

# Iterate through datasets
for u,n in zip(urls,names):
    print(f'\nPlotting {n.split(".")[0]}')

    # Read from URL (depending on station type)
    if '_hour' in n:
        df = pd.read_csv(u)
    else:
        cols = findNames(u)
        df = pd.read_csv(u, comment='#', names=cols)          
    df['time'] = pd.to_datetime(df.iloc[:,0], format='%Y-%m-%d %H:%M:%S') 
    
    print('Producing PDD bins...')
    
    # Group positive degree hours by year
    try:
        df['pdh'] = np.where(df['airtemp1'] >= 0, 1, 0)
    except:
        df['pdh'] = np.where(df['t_u'] >= 0, 1, 0) 
    df1 = df['pdh'].groupby([df["time"].dt.year]).sum()

    print('Plotting PDD...')    
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(range(len(df1.index)), df1.values, color='g')
    ax.set_title(n.split(".")[0])
    ax.set_xlabel('Year')
    ax.set_xticks(range(len(df1.index)))
    ax.set_xticklabels(list(df1.index), rotation=45)
    plt.savefig(f'{n.split(".")[0]}_pdh.jpg',dpi=300)
    plt.show()
    print('Plotting finished')
