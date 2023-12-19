# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 15:39:38 2023

@author: matti
"""
import mario
import pandas as pd
import numpy as np

user = "CF"
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
fileGDP = f"{pd.read_excel(paths, index_col=[0]).loc['GDP projections',user]}"
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
fileProjection = f"{pd.read_excel(paths, index_col=[0]).loc['Projections',user]}"
with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Projections',user]}\\Projections.xlsx") as writer:
    for key, df in FD_proj.items():
        sheet_name = f'{key}'
        df.to_excel(writer, sheet_name=sheet_name, index=True)

# #%%
# fileSwFD = f"{pd.read_excel(paths, index_col=[0]).loc['SwFD', user]}\\SwFD_Avg.xlsx"
# fileAIC = f"{pd.read_excel(paths, index_col=[0]).loc['AIC',user]}\\AIC_Avg.xlsx"
# fileProjection = f"{pd.read_excel(paths, index_col=[0]).loc['Projections',user]}\\Projections.xlsx"
# merged_dfs = {}

# for year in years:
#     df_swfd = pd.read_excel(fileSwFD, sheet_name=str(year))
#     df_aic = pd.read_excel(fileAIC, sheet_name=str(year))

#     # Read DataFrames from Excel files
#     df_projection = pd.read_excel(fileProjection, sheet_name=str(year))

#     # Concatenate the DataFrames along the columns
#     dfs_for_year = [df_projection, df_swfd, df_aic]
#     merged_dfs[year] = pd.concat(dfs_for_year, axis=0)

# # Salva i risultati in un nuovo file Excel
# output_file = f"{pd.read_excel(paths, index_col=[0]).loc['Merged FD',user]}\\merged_file.xlsx"

# with pd.ExcelWriter(output_file) as writer:
#     for year, merged_df in merged_dfs.items():
#         # Scrivi il DataFrame nel file Excel
#         merged_df.to_excel(writer, sheet_name=str(year), index=False)

# print(f"I dati sono stati uniti e salvati in '{output_file}'.")


