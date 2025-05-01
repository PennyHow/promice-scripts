#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 10:58:25 2024

@author: pho
"""
import pandas as pd
import xarray as xr
import numpy as np

station="EGP"

infile1 = "https://test-thredds.geus.dk/thredds/fileServer/aws/l2stations/csv/hour/"+station+"_hour.csv"
infile2 = "https://test-thredds.geus.dk/thredds/dodsC/aws/l2stations/netcdf/hour/"+station+"_hour.nc"


# Open CSV
name1 = infile1.split('/')[-1].split('_hour')[0]
df1 = pd.read_csv(infile1, comment='#', index_col=0,
                     na_values=['','nan'], parse_dates=True,
                     sep=',', 
                     skip_blank_lines=True)

# Open NetCDF   
df2 = xr.open_dataset(infile2)


# Count rows in file and calculation anticipated rows
def anticipated_rows(df):
    try:
        min_date = df.index.min()
        max_date = df.index.max()
    except:
        min_date = df.to_dataframe().index.min()
        max_date = df.to_dataframe().index.max()
    dates_range = pd.date_range(min_date, max_date, freq = '1H')
    return len(dates_range)

def fill_gaps(ds):
    '''Fill data gaps with nan values
    
    Parameters
    ----------
    ds : xarray.Dataset
        Data set to gap fill
    
    Returns
    -------
    ds_filled : xarray.Dataset
        Gap-filled dataset
    '''    
    min_date = ds.to_dataframe().index.min()
    max_date = ds.to_dataframe().index.max()
    
    # Determine common time interval
    time_diffs = np.diff(ds['time'].values)
    common_diff = pd.Timedelta(pd.Series(time_diffs).mode()[0])
    
    print('Common diff: ')
    print(common_diff)
    
    # Determine gap filled index
    full_time_range = pd.date_range(start=min_date, 
                                    end=max_date, 
                                    freq=common_diff)
    
    # Apply gap-fille index to dataset
    ds_filled = ds.reindex({'time': full_time_range}, fill_value=np.nan)
    return ds_filled


print('\nCSV file rows')
print('Actual rows: ' + str(len(df1)))
print('Anticipated rows: ' + str(anticipated_rows(df1)))
      
print('\nNetCDF file rows')
print('Actual rows: ' + str(len(df2['time'].values)))
print('Anticipated rows: ' + str(anticipated_rows(df2)))

ds = fill_gaps(df2)
print('Corrected rows: ' + str(len(ds['time'].values)))