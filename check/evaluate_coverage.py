#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 13:08:16 2024

@author: pho
"""
from pathlib import Path
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from pypromice.process.aws import AWS

station_name='NUK_U'

config_tx = '/home/pho/python_workspace/promice/aws-l0/tx/config/'+station_name+'.toml'
in_tx = '/home/pho/python_workspace/promice/aws-l0/tx/'

config_raw = '/home/pho/python_workspace/promice/aws-l0/raw/config/'+station_name+'.toml'
in_raw = '/home/pho/python_workspace/promice/aws-l0/raw/'+station_name

tx = AWS(config_tx, in_tx)
print('TX\n')
for t in tx.L0:

    f = Path(str(t.file)).name
    start = t.time[0].values
    end = t.time[-1].values
    print(str(f) + '\n' + str(start)[0:16] + ' to ' + str(end)[0:16] + '\n')


raw = AWS(config_raw, in_raw)
print('\nRAW\n')       
for t in raw.L0:

    f = Path(str(t.file)).name
    start = t.time[0].values
    end = t.time[-1].values
    print(str(f) + '\n' + str(start)[0:16] + ' to ' + str(end)[0:16] + '\n')
    

    

