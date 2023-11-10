#%%
import mario
from mario.tools.constants import _MASTER_INDEX as MI
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import os

user = "LR"
sN = slice(None)
years = range(2011,2012)

paths = 'Paths.xlsx'

world = {}

#%%
for year in years:
    world[year] = mario.parse_from_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\b. Aggregated & new sectors SUT\\{year}\\coefficients", table='SUT', mode="coefficients")
    
#%%
# world[year].get_shock_excel(f"{pd.read_excel(paths, index_col=[0]).loc['Shocks',user]}\_template.xlsx")

#%%
CRMs_shock_data = pd.read_excel(pd.read_excel(paths, index_col=[0]).loc['CRMs shock data',user],sheet_name=None, index_col=[0,1,2], header=[0,1,2])
CRMs_shock_data['info'] = pd.read_excel(pd.read_excel(paths, index_col=[0]).loc['CRMs shock data',user],sheet_name='info').iloc[:,-2:]
CRMs_shock_data['info'].set_index('Code',inplace=True)

shock_template = pd.read_excel(f"{pd.read_excel(paths, index_col=[0]).loc['Shocks',user]}\_template.xlsx",sheet_name=None)

new_z = pd.DataFrame()
for sheet,data in CRMs_shock_data.items():
    if sheet != 'info':
        data = data.droplevel(2,axis=0) 
        data = data.droplevel([1,2],axis=1) 
        data = data.stack().to_frame().reset_index()
        data['row level'] = 'Commodity'
        data['column level'] = 'Activity'
        data['type'] = 'Update'
        data['column sector'] = CRMs_shock_data['info'].loc[sheet,'Label']
        data.columns = ['row region', 'row sector', 'column region', 'value', 'row level',
               'column level', 'type', 'column sector', ]
        
        data.set_index(list(shock_template['z'].columns),inplace=True)
        data.reset_index(inplace=True)
        
        new_z = pd.concat([new_z,data],axis=0)
        
    CRMs_shock_data[sheet] = data
    
shock_template['z'] = new_z

export_path = f"{pd.read_excel(paths, index_col=[0]).loc['Shocks',user]}\Shock_add_CRMs.xlsx"
with pd.ExcelWriter(export_path) as writer:
    for sheet,data in shock_template.items():
        data.to_excel(writer,sheet,index=False)

writer.close()

#%% implement shock on CRMs
for year in years:
    world[year].shock_calc(f"{pd.read_excel(paths, index_col=[0]).loc['Shocks',user]}\Shock_add_CRMs.xlsx", z=True, scenario='CRMs')

#%% Shocked database to txt as Baseline
for year in years:
    world[year].to_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\c. Baseline\\{year}", scenario="CRMs", flows=False, coefficients=True)

    

    