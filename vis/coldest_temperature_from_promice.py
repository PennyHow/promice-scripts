#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Penelope How, pho@geus.dk
"""

import datetime as dt
import xarray as xr

# Define stations
stations = [ #GC-Net
            'CEN','CP1','DY2','EGP','HUM','JAR','NAE','NAU','NEM','NSE',
            'SDL','SDM','SWC','TUN',
            #GlacioBasis
            'FRE','LYN_L','LYN_T','NUK_K','ZAC_A','ZAC_L','ZAC_U',
            #PROMICE
            'KAN_B','KAN_L','KAN_M','KAN_T','KAN_U','KPC_L','KPC_U','MIT',
            'NUK_B','NUK_L','NUK_U','QAS_A','QAS_L','QAS_M', #'NUK_N',
            'QAS_U','SCO_L', 'SCO_U','TAS_A', 'TAS_L', 'TAS_U','THU_L',
            'THU_L2', 'THU_U','UPE_L','UPE_U',
            #External
            'RED_L','SER_B','ORO','WEG_B','WEG_L'
            ]

# Plot station location
coldest_temperatures=[]
for s in range(len(stations)):

    # Open file as xarray dataset
    inf = "https://thredds.geus.dk/thredds/dodsC/aws/l3sites/netcdf/hour/" + stations[s] + "_hour.nc"
    ds = xr.open_dataset(inf)

    temp = float(ds["t_u"].min())
    t = ds["t_u"].idxmin(dim="time").values

    if "t_l" in ds:
        temp_l = float(ds["t_l"].min())
        t_l = ds["t_l"].idxmin(dim="time").values
        if temp_l < temp:
            temp = temp_l
            t = t_l

    print(f"{stations[s]}: {temp} ({t})")
    coldest_temperatures.append([stations[s],t,temp])

