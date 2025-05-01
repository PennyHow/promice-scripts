#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 13:08:16 2024

@author: pho
"""
from pathlib import Path
import glob
from pypromice.process.aws import AWS

inf = '/home/pho/python_workspace/promice/aws-l0/'

# Load Level 0 tx files from toml
for i in glob.glob(inf+'tx/**/*.toml', recursive=True):
    print('Loading TX from ' + str(Path(i).stem))
    tx = AWS(i , inf+'tx/')

# Load Level 0 raw files from toml
for i in glob.glob(inf+'raw/**/*.toml', recursive=True):
    print('Loading RAW from ' + str(Path(i).stem))
    raw = AWS(i, inf+'raw/'+str(Path(i).stem))

