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
    station = "SER_B"
    variable = "usr_cor"

    infile1 = "https://thredds.geus.dk/thredds/dodsC/aws/l3sites/netcdf/hour/" + station + "_hour.nc"
    # infile1 = "https://test-thredds.geus.dk/thredds/dodsC/aws/l2stations/netcdf/hour/" + station + "_hour.nc"
    ds = xr.open_dataset(infile1)

    print('Plotting ' + station + ' ' + variable)
    ds[variable].plot()
    plt.show()
    
else:
    """Executed on import"""
    pass
        
