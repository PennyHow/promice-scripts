#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

import os, sys
import xarray as xr
import matplotlib.pyplot as plt

if __name__ == '__main__':
    """Executed from the command line"""
    station1 = "NUK_Lv3"
    station2 = "NUK_Uv3"
    res = "mixed"
    variable = "rot_true"

    time1 = "2025-10-01 00:00:00"
    time2 = "2026-02-01 00:00:00"

    infile1 = "https://thredds.geus.dk/thredds/dodsC/aws/l2stations/netcdf/" + res + "/" + station1 + "_" + res + ".nc"
    infile2 = "https://thredds.geus.dk/thredds/dodsC/aws/l2stations/netcdf/" + res + "/" + station2 + "_" + res + ".nc"

    ds_lower = xr.open_dataset(infile1)
    ds_upper = xr.open_dataset(infile2)

    ds_lower = ds_lower.sel(time=slice(time1, time2))
    ds_upper = ds_upper.sel(time=slice(time1, time2))

    ds_lower[variable].plot(linewidth=1, label="NUK_Lv3")
    ds_upper[variable].plot(linewidth=1, label="NUK_Uv3")
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.6)
    plt.legend(loc=2)
    plt.show()

else:
    """Executed on import"""
    pass

