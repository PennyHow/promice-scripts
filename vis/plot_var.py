#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 16:20:09 2022

Script to get L3 data from L0 messages using the AWS object

@author: Penelope How, pho@geus.dk
"""

import os, sys
import xarray as xr
import matplotlib.pyplot as plt

if __name__ == '__main__':
    """Executed from the command line"""
    station = "KAN_B"
    res = "hour"
    variable = "rainfall_u"

    infile1 = "https://thredds.geus.dk/thredds/dodsC/aws/l3sites/netcdf/" + res + "/" + station + "_" + res + ".nc"
    # infile1 = "https://thredds.geus.dk/thredds/dodsC/aws/l2stations/netcdf/" + res + "/" + station + "_" + res + ".nc"
    # infile1 = "https://thredds.geus.dk/thredds/dodsC/aws/l2stations/netcdf/" + res + "/" + station + "_" + res + ".nc"
    # infile1 = '/home/pho/Desktop/NSE/NSE_hour.nc'

    ds = xr.open_dataset(infile1)
    print(list(ds.variables))
    print(ds)

    print('Plotting ' + station + ' ' + variable)
    print(ds[variable].ffill(dim='time').isel(time=-1).values)
    ds[variable].plot()
    plt.show()

else:
    """Executed on import"""
    pass
        
