# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 15:39:38 2023

@author: matti
"""
import mario
import pandas as pd
import numpy as np
import os

user = "MBV"
sN = slice(None)
history = range(2000,2021)
years = range(2021,2101)

paths = 'Paths.xlsx'

fileParam = f"{pd.read_excel(paths, index_col=[0]).loc['fileParam',user]}"
Weibull_params =  pd.read_excel(fileParam, "Weibull", index_col=[0,1])
sens = list(set(Weibull_params.index.get_level_values(1)))


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

#%% Projecting FD calculating sn 

         
            
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
    
regions = FD_proj[i].columns
for i in years:

    # Add indices to FD_proj[i]
    FD_proj[i].index = pd.MultiIndex.from_arrays([Rn.index.get_level_values(0), Rn.index.get_level_values(1), Rn.index.get_level_values(2)], names=['Region', 'Level', 'Item']    )     
    FD_proj[i].columns = pd.MultiIndex.from_arrays([regions,['Consumption category'] * len(regions), ['Final consumption expenditure by households'] * len(regions)], names=['Region', 'Level', 'Item']) 

for i in history:
    FD[i].index = pd.MultiIndex.from_arrays([Rn.index.get_level_values(0), Rn.index.get_level_values(1), Rn.index.get_level_values(2)], names=['Region', 'Level', 'Item']    )     
    FD[i].columns = pd.MultiIndex.from_arrays([regions,['Consumption category'] * len(regions), ['Final consumption expenditure by households'] * len(regions)], names=['Region', 'Level', 'Item'])       
    


#%% Building the FD useful for the Database 
fileProjection = f"{pd.read_excel(paths, index_col=[0]).loc['Projections',user]}"
with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Projections',user]}\\Projections.xlsx") as writer:
    for key, df in FD_proj.items():
        sheet_name = f'{key}'
        df.to_excel(writer, sheet_name=sheet_name, index=True)

fileHistory = f"{pd.read_excel(paths, index_col=[0]).loc['History',user]}"
with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Projections',user]}\\Historical_FD.xlsx") as writer:
    for key, df in FD.items():
        sheet_name = f'{key}'
        df.to_excel(writer, sheet_name=sheet_name, index=True)

#%% Merging projected FD in one file Excel

# output_folder = pd.read_excel(paths, index_col=[0]).loc['Merged FD', user]
# file_type = 'xlsx'

# for s in sens:
#     file_swfd = f"{pd.read_excel(paths, index_col=[0]).loc['SwFD', user]}\\SwFD_{s}.{file_type}"
#     file_aic = f"{pd.read_excel(paths, index_col=[0]).loc['AIC', user]}\\AIC_{s}.{file_type}"
#     file_projection = f"{pd.read_excel(paths, index_col=[0]).loc['Projections', user]}\\Projections.{file_type}"

#     merged_dfs = {}
#     for year in years:
#         df_swfd = pd.read_excel(file_swfd, sheet_name=str(year))
#         df_aic = pd.read_excel(file_aic, sheet_name=str(year))
#         df_projection = pd.read_excel(file_projection, sheet_name=str(year))

#         dfs_for_year_proj = [df_projection, df_swfd, df_aic]
#         merged_dfs[year] = pd.concat(dfs_for_year_proj, axis=0)
#         #merged_dfs[year].index = pd.MultiIndex.from_arrays([['EU27+UK'] * 671, ['Sector'] * 671, merged_dfs[2021].index], names=['Region', 'Level', 'Item']    )
#         #merged_dfs[year].columns = pd.MultiIndex.from_arrays([regions,['Consumption category'] * len(regions), ['Final consumption expenditure by households'] * len(regions)], names=['Region', 'Level', 'Item'])
#     output_file_proj = os.path.join(output_folder, f"FD_proj_merged_{s}.{file_type}")
#     with pd.ExcelWriter(output_file_proj) as writer:
#         for year, merged_df in merged_dfs.items():
#             merged_df.to_excel(writer, sheet_name=str(year), index=False)


# #%% Merging historical FD in one file Excel

# output_folder_history = pd.read_excel(paths, index_col=[0]).loc['Historical FD', user]

# for s in sens: 
#     file_historic = f"{pd.read_excel(paths, index_col=[0]).loc['History', user]}\\Historical_FD.{file_type}"

#     merged_dfs_history = {}
#     for year_historic in range(2011, 2021):
#         df_swfd = pd.read_excel(file_swfd, sheet_name=str(year_historic))
#         df_aic = pd.read_excel(file_aic, sheet_name=str(year_historic))
#         df_history = pd.read_excel(file_historic, sheet_name=str(year_historic))

#         dfs_for_year_history = [df_history, df_swfd, df_aic]
#         merged_dfs_history[year_historic] = pd.concat(dfs_for_year_history, axis=0)
        
#     output_file_history = os.path.join(output_folder_history, f"FD_historic_merged_{s}.{file_type}")
#     with pd.ExcelWriter(output_file_history) as writer_hist:
#         for year_hist, merged_df_history in merged_dfs_history.items():
#             merged_df_history.to_excel(writer_hist, sheet_name=str(year_hist), index=False)

# #%%
# output_folder_total = pd.read_excel(paths, index_col=[0]).loc['FD Total', user]
# file_type = 'xlsx'

# for s in sens:
#     file_swfd = f"{pd.read_excel(paths, index_col=[0]).loc['SwFD', user]}\\SwFD_{s}.{file_type}"
#     file_aic = f"{pd.read_excel(paths, index_col=[0]).loc['AIC', user]}\\AIC_{s}.{file_type}"
#     file_projection = f"{pd.read_excel(paths, index_col=[0]).loc['Projections', user]}\\Projections.{file_type}"
#     file_historic = f"{pd.read_excel(paths, index_col=[0]).loc['History', user]}\\Historical_FD.{file_type}"
    
#     merged_dfs_total = {}
#     for year in range(2011, 2101):
#         if year <= 2020:
#             df_swfd = pd.read_excel(file_swfd, sheet_name=str(year))
#             df_aic = pd.read_excel(file_aic, sheet_name=str(year))
#             df_history = pd.read_excel(file_historic, sheet_name=str(year))
            
#             dfs_for_year_history = [df_history, df_swfd, df_aic]
#             merged_dfs_total = pd.concat(dfs_for_year_history, axis=0)
#         else:
#             df_swfd = pd.read_excel(file_swfd, sheet_name=str(year))
#             df_aic = pd.read_excel(file_aic, sheet_name=str(year))
#             df_projection = pd.read_excel(file_projection, sheet_name=str(year))

#             dfs_for_year_proj = [df_projection, df_swfd, df_aic]
#             merged_dfs_total = pd.concat(dfs_for_year_proj, axis=0)
    
#     output_file_total = os.path.join(output_folder_total, f"FD_total_{s}.{file_type}")
#     with pd.ExcelWriter(output_file_total) as writer_total:
#         for year_tot,merged_df_total in merged_dfs_total.items():
#             merged_dfs_total.to_excel(writer_total, sheet_name=str(year), index=False)


#%%
output_folder_total = pd.read_excel(paths, index_col=[0]).loc['FD Total', user]
file_type = 'xlsx'

for s in sens:
    file_swfd = f"{pd.read_excel(paths, index_col=[0]).loc['SwFD', user]}\\SwFD_{s}.{file_type}"
    file_aic = f"{pd.read_excel(paths, index_col=[0]).loc['AIC', user]}\\AIC_{s}.{file_type}"
    file_projection = f"{pd.read_excel(paths, index_col=[0]).loc['Projections', user]}\\Projections.{file_type}"
    file_historic = f"{pd.read_excel(paths, index_col=[0]).loc['History', user]}\\Historical_FD.{file_type}"
    
    output_file_total = os.path.join(output_folder_total, f"FD_total_{s}.{file_type}")
    with pd.ExcelWriter(output_file_total) as writer_total:
        for year in range(2011, 2101):
            if year <= 2020:
                df_swfd = pd.read_excel(file_swfd, sheet_name=str(year),header= None, skiprows=4)
                df_aic = pd.read_excel(file_aic, sheet_name=str(year), header= None, skiprows=4)
                df_history = pd.read_excel(file_historic, sheet_name=str(year), header= None)
                
                dfs_for_year_history = [df_history, df_swfd, df_aic]
                merged_df_history = pd.concat(dfs_for_year_history, axis=0)
                
                
                sheet_name = f"{str(year)}"
                merged_df_history.to_excel(writer_total, sheet_name=sheet_name, index=False, header= False)
            else:
                df_swfd = pd.read_excel(file_swfd, sheet_name=str(year), header = None, skiprows=4)
                df_aic = pd.read_excel(file_aic, sheet_name=str(year), header = None, skiprows=4)
                df_projection = pd.read_excel(file_projection, sheet_name=str(year),header = None)

                dfs_for_year_proj = [df_projection, df_swfd, df_aic]
                merged_df_proj = pd.concat(dfs_for_year_proj, axis=0)
                
                sheet_name = f"{str(year)}"
                merged_df_proj.to_excel(writer_total, sheet_name=sheet_name, index=False, header=False)
            

        

