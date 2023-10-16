# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 22:03:47 2023

@author: loren
"""

import mario
import pandas as pd

user = "LR"
sN = slice(None)
years = range(2011,2020)

paths = 'Paths.xlsx'

#%% Parse aggregated database from txt
prices = pd.DataFrame()
e = pd.DataFrame()
x = pd.DataFrame()

for year in years:
    world = mario.parse_from_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\a. Aggregated_SUT\\{year}\\flows", table='SUT', mode="flows")
    E = world.E.loc["Energy Carrier Supply: Total",(sN,sN,world.search("Activity","Production of electricity"))].to_frame().groupby(level=[0],axis=0).sum()*1e9/3600
    X = world.X.loc[(sN,sN,world.search("Activity","Production of electricity")),"production"].groupby(level=[0],axis=0).sum().to_frame()
    
    e = pd.concat([
        e,
        pd.DataFrame(E.values, index=E.index, columns=[year]),
        ], axis=1)
    
    x = pd.concat([
        x,
        pd.DataFrame(X.values, index=X.index, columns=[year]),
        ], axis=1)
    
    prices = pd.concat([
        prices,
        pd.DataFrame(X.values/E.values, index=X.index, columns=[year]),
        ], axis=1)