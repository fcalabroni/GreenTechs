# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 15:39:38 2023

@author: matti
"""
import mario
import pandas as pd
import numpy as np

user = "MBV"
sN = slice(None)
history = range(2000,2021)
years = range(2021,2101)

paths = 'Paths.xlsx'

#%% Parsing IOT
exio_iot = {}

for year in history:
    exio_iot_path  = pd.read_excel(paths, index_col=[0]).loc['EXIOBASE IOT',user]+f"/IOT_{year}_ixi.zip"

    exio_iot[year]  = mario.parse_exiobase(path=exio_iot_path, table='IOT', unit='Monetary')

#%% Getting excel templates to aggregate raw Exiobase
path_aggr_IOT  = r"Aggregations\Aggregation_raw_IOT.xlsx"
# exio_iot[year].get_aggregation_excel(path_aggr_IOT)

#%% Aggregating exiobase as other models
for year in history:
    exio_iot[year].aggregate(path_aggr_IOT, levels=["Region"])
    
#%% Extrapolation FD
#aggregate sectors
#extrapolate in a dataframe the FD for each year
FD = {}
for year in history:
    FD[year] = exio_iot[year].Y.sum(axis=1)
    #FD[year] = exio_iot[year].Y.groupby(level=[ 0],sort=False, axis=1).sum()
    
#%% Projection FD
# Calculating average growth from historic data for each sector
Rn = FD[2020]/FD[2000]
rn = np.power(Rn.values, 1/20)

rate= {}
FD_elastic = {}
for i in years:
    FD_elastic[i]= {}
    rate[i]= rn
FD_elastic[0] = FD[2020]*rn
for i in years:
    FD_elastic[i+1] = FD_elastic[i] * rate[i]
    #sn[i] = 
    
    
#%% Building the FD useful for the Database 
#adding installed capacity in Monetary values 
#adding SwFD
