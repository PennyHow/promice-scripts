#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 16:20:09 2022

Script to get L3 data from L0 messages using the AWS object

@author: Penelope How, pho@geus.dk
"""

import os, sys
from argparse import ArgumentParser

#try:
sys.path.append('../process/')
from aws import AWS
print('Using local copy')
#except:
#    from pypromice.process import AWS
#    print('Using pypromice pip version')

if __name__ == '__main__':
    """Executed from the command line"""
    config_file = '/home/pho/Desktop/python_workspace/promice/aws-l0/tx/config/EGP.toml'
    inpath = '/home/pho/Desktop/python_workspace/promice/aws-l0/tx'
    issues = '/home/pho/Desktop/python_workspace/promice/PROMICE-AWS-data-issues/'

    station_name = config_file.split('/')[-1].split('.')[0] 
    station_path = os.path.join(inpath, station_name)
    
    print(config_file)
    print(inpath)
    print(station_path)

    if os.path.exists(station_path):
        pAWS = AWS(config_file, station_path, issues)    
    else:
        pAWS = AWS(config_file, inpath, issues)

    print(pAWS.L0)
    pAWS.process()
    print(pAWS.L3)
    L0 = pAWS.L0
    L1 = pAWS.L1
    L2 = pAWS.L2
    L3 = pAWS.L3
    #pAWS.write(args.outpath)
    
else:
    """Executed on import"""
    pass
        
