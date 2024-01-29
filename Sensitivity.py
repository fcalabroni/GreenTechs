# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 11:29:02 2024

@author: matti
"""
#%%
import mario
import pandas as pd
import numpy as np

user = "MBV"
sN = slice(None)
years = range(2011,2101)

paths = 'Paths.xlsx'
#%% Sensitivity for EOL_RIR
fileParam = f"{pd.read_excel(paths, index_col=[0]).loc['fileParam',user]}"
price_materials = pd.read_excel(fileParam,sheet_name='price materials', index_col=[0], header=[0])
region = pd.read_excel(fileParam, "region",header = None, index_col=[0])
region = list(region.index.get_level_values(0))
met = list(price_materials.index.get_level_values(0))
RR = ['hist', 'target', 'full']
price = ['Avg','Max','Min']
# sens = list(set(price_materials.columns.get_level_values(0)))
lifetime = ['Min','Avg','Max']
# Weibull_params =  pd.read_excel(fileParam, "Weibull", index_col=[0,1])
# lifetime = sens = list(set(Weibull_params.index.get_level_values(1)))
y = [2011,2020,2050,2100]

Greentech_tot_s = {}
for rr in RR:
    Greentech_tot_s[rr] = {}
    for s in lifetime:
        Greentech_tot_s[rr][s] = {}
        for year in y:
            Greentech_tot_s[rr][s][year] = pd.DataFrame(0, index= met ,columns = pd.MultiIndex.from_arrays([region,['Green Tech']*len(region)]))

Greentech_tot_p = {}
for rr in RR:
    Greentech_tot_p[rr] = {}
    for p in price:
        Greentech_tot_p[rr][p] = {}
        for year in y:
            Greentech_tot_p[rr][p][year] = pd.DataFrame(0, index= met ,columns = pd.MultiIndex.from_arrays([region,['Green Tech']*len(region)]))

met_rec_tot = {}
met_rec_tot = pd.DataFrame(0, index= met, columns = Greentech_tot_s[rr][s][year].columns)

met_rec= {}
for s in lifetime:
    met_rec[s] = {}
    for rr in RR:
        met_rec[s][rr] = {}
        for p in price:
            met_rec[s][rr][p] = {}
            for year in y:
                met_rec[s][rr][p][year] = pd.DataFrame(0,index= met, columns = Greentech_tot_s[rr][s][year].columns)
            
EOL_RIR_s = {}
for rr in RR:
    EOL_RIR_s[rr] = {} 
    for s in lifetime:
        EOL_RIR_s[rr][s] = {}
        for m in met: 
            EOL_RIR_s[rr][s][m] = pd.DataFrame(0, index = region, columns = [2011,2020,2050,2100])
            
EOL_RIR_p = {}
for rr in RR:
    EOL_RIR_p[rr] = {} 
    for p in price:
        EOL_RIR_p[rr][p] = {} 
        for m in met:
            EOL_RIR_p[rr][p][m] = pd.DataFrame(0, index = region, columns = [2011,2020,2050,2100])
    
            
for year in y:
    for s in lifetime:
        for rr in RR:
            for p in price:                                    
                for r in region:
                    for m in met:
                        path_rec = f"{pd.read_excel(paths, index_col=[0]).loc['metrec_tech',user]}\\metrec_tech_{s}_{rr}_{p}.xlsx"
                        met_recs = pd.read_excel(path_rec, sheet_name=str(year),header= [0,1,2], index_col = [0,1,2])
                        #Critical materials recycled by green techs wthout disction from the technologies
                        met_rec_tot.loc['Neodymium',(r,'Green Tech')] = met_recs.loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Neodymium'),(r, 'Sector', ['Offshore wind plants','Onshore wind plants','Photovoltaic plants'])].sum().sum()
                        met_rec_tot.loc['Dysprosium',(r,'Green Tech')] = met_recs.loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Dysprosium'),(r, 'Sector', ['Offshore wind plants','Onshore wind plants','Photovoltaic plants'])].sum().sum()
                        met_rec_tot.loc['Copper',(r,'Green Tech')] = met_recs.loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Copper'),(r, 'Sector', ['Offshore wind plants','Onshore wind plants','Photovoltaic plants'])].sum().sum()
                        met_rec_tot.loc['Raw silicon',(r,'Green Tech')] = met_recs.loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Raw silicon'),(r, 'Sector', ['Offshore wind plants','Onshore wind plants','Photovoltaic plants'])].sum().sum()                                        
                        met_rec[s][rr][p][year].loc[met,(region,'Green Tech')] = met_rec_tot.loc[met,(region,'Green Tech')]
                        
                        path_cons_s = f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Sensitivity\\Consumption\\Lifetime\\cons_gt_{s}.xlsx"
                        path_cons_p = f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Sensitivity\\Consumption\\price\\cons_gt_{p}.xlsx"
                        Greentech_tot_s[rr][s][year] = pd.read_excel(path_cons_s, sheet_name=str(year),header= [0,1], index_col = [0])
                        Greentech_tot_p[rr][p][year] = pd.read_excel(path_cons_p, sheet_name=str(year),header= [0,1], index_col = [0])
                                               
for s in lifetime:
    for m in met:
        for r in region:
            for year in y:
                EOL_RIR_s['target'][s][m].loc[r,year] = met_rec[s]['target']['Avg'][year].loc[m,(r,'Green Tech')]/(Greentech_tot_s['target'][s][year].loc[m,(r,'Green Tech')])
                EOL_RIR_s['hist'][s][m].loc[r,year] = met_rec[s]['hist']['Avg'][year].loc[m,(r,'Green Tech')]/(Greentech_tot_s['hist'][s][year].loc[m,(r,'Green Tech')])
                EOL_RIR_s['full'][s][m].loc[r,year] = met_rec[s]['full']['Avg'][year].loc[m,(r,'Green Tech')]/(Greentech_tot_s['full'][s][year].loc[m,(r,'Green Tech')])
                
for p in price:
    for m in met:
        for r in region:
            for year in y:
                EOL_RIR_s['target'][p][m].loc[r,year] = met_rec['Avg']['target'][p][year].loc[m,(r,'Green Tech')]/(Greentech_tot_s['target'][p][year].loc[m,(r,'Green Tech')])
                EOL_RIR_s['hist'][p][m].loc[r,year] = met_rec['Avg']['hist'][p][year].loc[m,(r,'Green Tech')]/(Greentech_tot_s['hist'][p][year].loc[m,(r,'Green Tech')])
                EOL_RIR_s['full'][p][m].loc[r,year] = met_rec['Avg']['full'][p][year].loc[m,(r,'Green Tech')]/(Greentech_tot_s['full'][p][year].loc[m,(r,'Green Tech')])
                
                
#%% Export Data 
for rr in RR:
    for s in lifetime:
        with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Sensitivity\\EOL-RIR\\Lifetime\\EOL_RIR_{rr}_Lifetime_{s}.xlsx") as writer: 
             for key, df in EOL_RIR_s[rr][s].items():
                 sheet_name = f'{key}'
                 df.to_excel(writer, sheet_name=sheet_name, index= True)
                 
    for p in price:
        with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Sensitivity\\EOL-RIR\\Price\\EOL_RIR_{rr}_price_{p}.xlsx") as writer: 
             for key, df in EOL_RIR_s[rr][p].items():
                 sheet_name = f'{key}'
                 df.to_excel(writer, sheet_name=sheet_name, index= True)
     
        
     
        
     
        
     
        
     
        