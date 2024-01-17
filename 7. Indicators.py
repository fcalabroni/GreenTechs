# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 11:09:25 2024

@author: matti
"""

import pandas as pd
import numpy as np

user = "MBV"
sN = slice(None)

paths = 'Paths.xlsx'
years = range(2011,2101)

scenario = ['Baseline', 'Act']
sens = ['Avg','Max','Min']
upgrade = ['hist', 'target', 'full']

met_rec = {}    
for s in sens:
    met_rec[s] = {}
    for u in upgrade:
        met_rec[s][u] = {}
        for p in sens:
            met_rec[s][u][p] = {}

EOL_RIR_base = {}
for u in upgrade:
    EOL_RIR_base[u] = pd.DataFrame(0, index = pd.MultiIndex.from_arrays([['EU27+UK']*4, ['Sector']*4, ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']]), columns = years)
 
EOL_RIR_act = {}
for u in upgrade:
    EOL_RIR_act[u] = pd.DataFrame(0, index = pd.MultiIndex.from_arrays([['EU27+UK']*4, ['Sector']*4, ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']]), columns = years)
    
for scen in scenario:
    for year in years:
        for s in ['Avg']:
            for u in upgrade:
                for p in ['Avg']:
                    path_rec = f"{pd.read_excel(paths, index_col=[0]).loc['metrec',user]}\\metrec_{s}_{u}_{p}.xlsx"
                    met_rec = pd.read_excel(path_rec, sheet_name=str(year),header= [0], index_col = [0,1,2]) #,skiprows=[0])
                    
                    if scen == 'Baseline':
                        path_res = f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Baseline\\RR\\Results_world_base_RR_{u}.xlsx"
                        Res = pd.read_excel(path_res, sheet_name='Annual production',header= [0],index_col = [0,1,2])
                        Res.index = pd.MultiIndex.from_arrays([['EU27+UK']*4, ['Sector']*4, ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']])
                        
                        EOL_RIR_base[u].loc[:,year] = met_rec.loc[:,0]/(met_rec.loc[:,0] + Res.loc[:,year])
                    
                    else:
                        path_res = f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Act\\RR\\Results_world_act_RR_{u}.xlsx"
                        Res = pd.read_excel(path_res, sheet_name='Annual production',header= [0],index_col = [0,1,2])
                        Res.index = pd.MultiIndex.from_arrays([['EU27+UK']*4, ['Sector']*4, ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']])
                        
                        EOL_RIR_act[u].loc[:,year] = met_rec.loc[:,0]/(met_rec.loc[:,0] + Res.loc[:,year])
                        

