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
    #FD[year] = exio_iot[year].Y.sum(axis=1)
    FD[year] = exio_iot[year].Y.groupby(level=[ 0],sort=False, axis=1).sum()
    
#%% Projection FD
# Calculating average growth from historic data for each sector
Rn = FD[2020]/FD[2000]
Rn = Rn.fillna(1)
Rn.replace([np.inf, -np.inf], 1, inplace=True)

rn = np.power(Rn.values, 1/20)
rn = pd.DataFrame(rn, index=Rn.index, columns = Rn.columns)

#%%

FD_elastic = {}
sn = {}
fileGDP = f"{pd.read_excel(paths, index_col=[0]).loc['GDP projection',user]}"
GDP_rate = pd.read_excel(fileGDP,'GDP rate',header=0,index_col=0)
for i in years:
    FD_elastic[i] = 0
    sn[i] = 0
    
FD_elastic[2021] = FD[2020] * rn
for i in years:
    FD_elastic[i+1] = FD_elastic[i] * rn
    sn[i] = FD_elastic[i]/FD_elastic[i].sum(axis=0)
    
FD_GDP = {}
FD_proj = {}

for i in years:
    FD_GDP[i] = 0
    FD_proj[i] = 0
    
FD_GDP[2021] = FD[2020].sum(axis=0)*(1+GDP_rate.loc[:,2021])
FD_proj[2021] = FD_GDP[2021]*sn[2021]

for i in range(2022,2101):
    FD_GDP[i] = FD_GDP[i-1].groupby(level=[ 0],sort=False, axis=0).sum()*(1+GDP_rate.loc[:,i])
    FD_proj[i] = FD_GDP[i]*sn[i]
    
    
#%% Building the FD useful for the Database 
#adding installed capacity in Monetary values 
#adding SwFD

        

