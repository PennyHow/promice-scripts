#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 09:40:34 2023

@author: pho
"""
import pandas as pd
import matplotlib.pyplot as plt

nukk_e3 = pd.read_csv('/home/pho/Desktop/NUK_K_hour_Edition3.txt', delimiter='\s+', na_values=[-999], parse_dates=[[0,1,2,3]], header=0)

nukk_e4 = pd.read_csv('/home/pho/Desktop/NUK_K_hour_Edition4.csv', delimiter=',', header=0)



nukk_e3.plot(kind='line',x="Year_MonthOfYear_DayOfMonth_HourOfDay(UTC)",y="CloudCover")
nukk_e4.plot(kind='line',x="time",y="cc")


nukk_e3.iloc[14:65424].plot(kind='line',x="Year_MonthOfYear_DayOfMonth_HourOfDay(UTC)", y='CloudCover')
nukk_e4.iloc[0:65410].plot(kind='line',x="time",y="cc")



nukk_e3_s = nukk_e3.iloc[14:65424]
nukk_e4_s = nukk_e4.iloc[0:65410]

nukk_e3_s = nukk_e3[['Year_MonthOfYear_DayOfMonth_HourOfDay(UTC)','CloudCover']]
nukk_e4_s = nukk_e4[['time','cc']]



nukk_e3_l = list(nukk_e3_s['CloudCover'])
nukk_e4_l = list(nukk_e4_s['cc'])

plt.plot(list(range(len(nukk_e3_l))), nukk_e3_l, 'r+')
plt.plot(list(range(len(nukk_e4_l))), nukk_e4_l, 'b+')
plt.show()
