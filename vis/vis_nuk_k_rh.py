#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 10:31:04 2023

@author: pho
"""
import pandas as pd
import matplotlib.pyplot as plt

def parserV1(y, doy, t):                                             
    return pd.to_datetime(f'{y}-{str(doy).zfill(3)}:{str(t).zfill(4)}',
                          format='%Y-%j:%H%M')     


# Define file paths
nuk3 = '/home/pho/Downloads/NUK_K_hour_v03.txt'
nuk4 = '/home/pho/Desktop/NUK_K_hour.csv'
nuk4_new = '/home/pho/Desktop/NUK_K_10min.csv'

# Read Edition 3 and grab RH (minus 14 blank entries at the beginning)
nuk3 = pd.read_csv(nuk3, delim_whitespace=True, parse_dates={'time': ['Year', 'DayOfYear', 'HourOfDay(UTC)']}, date_parser=parserV1)
rh3 = list(nuk3['RelativeHumidity(%)'])[14:]

# Read Edition 4 and grab RH and date
nuk4 = pd.read_csv(nuk4)
nuk4_date = list(nuk4['time'])
rh4_u = list(nuk4['rh_u'])
rh4_cor = list(nuk4['rh_u_cor'])

# Read new Edition 4 (developmental)
nuk4_new = pd.read_csv(nuk4_new, index_col='time', parse_dates=True)
nuk4_new_resam = nuk4_new.resample('60min').mean()
rh4_cor_new = list(nuk4_new_resam['rh_u_cor'])

# Choose plotting time step (e.g. from 1-30 September 2015)
r1 = 9572
r2 = 10291
       
# Plot
plt.figure(figsize=(10,15))
plt.plot(nuk4_date[r1:r2], rh3[r1:r2], 'r', label='Edition 3')
# plt.plot(nuk4_date[r1:r2], rh4_cor[r1:r2], 'g', label='Edition 4 (current)')
plt.plot(nuk4_date[r1:r2], rh4_cor_new[r1:r2], 'b', label='Edition 4 (developmental)')

# Declutter x tick labels and show
plt.xticks(ticks=list(range(0,len(range(r1,r2))))[0::72], rotation=45)
plt.grid()
plt.legend(loc=4)
plt.show()

