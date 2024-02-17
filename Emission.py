# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 08:39:35 2024

@author: matti
"""

import mario
import pandas as pd
import numpy as np

user = "MBV"
sN = slice(None)
years = range(2011,2101)

paths = 'Paths.xlsx'

#%% Parse and SUT to IOT

WIOT = mario.parse_from_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\d. Baseline\\2011\\coefficients", table='SUT', mode="coefficients")
WIOT.to_iot(method='B')
#%% creating template for waste sectors

waste_sectors= [
    'Disassembler of Wind Turbines',
    'Disassembler of PV panels',
    'Refinery of Generators of Onshore Wind Turbines',
    'Refinery of Generators of Offshore Wind Turbines',
    'Refinery of Silicon layer in PV panel',
    'Refinery of Cu in wires of WT and PV',
    'Landifill',
    ]

ref = [
       'Refinery of Generators of Onshore Wind Turbines',
       'Refinery of Generators of Offshore Wind Turbines',
       'Refinery of Silicon layer in PV panel',
       'Refinery of Cu in wires of WT and PV',
       ]
#%% Getting excel templates to add waste sectors
path_waste_sector = f"{pd.read_excel(paths, index_col=[0]).loc['Add Sectors',user]}\\new_waste_sector.xlsx"
#world[year].get_add_sectors_excel(new_sectors=waste_sectors, regions= [world[year].get_index('Region')[1]],path=path_waste_sector, item='Sector')

WIOT.get_add_sectors_excel(new_sectors=waste_sectors, regions= [WIOT.get_index('Region')[1]],path=path_waste_sector, item='Sector')
#%% Adding new commodities and activities (EMPTY)
WIOT.add_sectors(io=path_waste_sector, new_sectors= waste_sectors, regions= [WIOT.get_index('Region')[1]], item='Sectors', inplace=True)

#%% Emission coefficient
e = WIOT.e
e_mat = e.loc[("CO2 - combustion - air"),(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon'])]
e_mat = e_mat.to_frame()
reduction = pd.DataFrame(4*[1-0.29, 1-0.79, 1-0.85, 1-0.8], index = e_mat.index, columns = e_mat.columns)
e_rec = pd.DataFrame(0, index= e_mat.index, columns = ["CO2 - combustion - air"])
e_rec = e_mat * reduction
#%% BASELINE with sensitivity on Recycling Rate (Lifetime = Avg, price = Avg)
fileParam = f"{pd.read_excel(paths, index_col=[0]).loc['fileParam',user]}"
RR_upgrade =  pd.read_excel(fileParam, "RR", index_col=[0])
Weibull_params =  pd.read_excel(fileParam, "Weibull", index_col=[0,1])
#sens = list(set(RR_upgrade.index.get_level_values(0)))
#sens = sens[:4]
sens = ['hist', 'target', 'full']
region = pd.read_excel(fileParam, "region",header = None, index_col=[0])
region = list(region.index.get_level_values(0))

scenario = ['Baseline','Act']
techs = list(set(Weibull_params.index.get_level_values(0)))

price_materials = pd.read_excel(fileParam,sheet_name='price materials', index_col=[0], header=[0])
price = pd.concat([price_materials] * 4, ignore_index= True) #unit of price [USD/kg]
price.index = pd.MultiIndex.from_arrays([['EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','China', 'China', 'China', 'China','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 16, ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']*4])

met = list(price_materials.index.get_level_values(0))
USD_to_EUR = pd.read_excel(fileParam,"USD to EURO", header=0, index_col=0)

Total_Demand = {}
for s in sens:
    Total_Demand[s] = {}
    for year in years:
        Total_Demand[s][year] = {}
        
Recycled_Supply = {}
for s in sens:
    Recycled_Supply[s] = {}
    for year in years:
        Recycled_Supply[s][year] = {}

Primary_Supply = {} #Primary == Mining
for s in sens:
    Primary_Supply[s] = {}
    for year in years:
        Primary_Supply[s][year] = {}

for scen in ['Baseline']:   
    for year in years:
        for s in sens:
            path_SG2 = f"{pd.read_excel(paths, index_col=[0]).loc['SG2',user]}\\SG2_Avg.xlsx"
            path_FD = f"{pd.read_excel(paths, index_col=[0]).loc['FD Total',user]}\\FD_total_Avg.xlsx"
            #path_metrec = f"{pd.read_excel(paths, index_col=[0]).loc['metrec',user]}\\metrec_{s}_b2.xlsx"
            path_A2 = f"{pd.read_excel(paths, index_col=[0]).loc['A2',user]}\\Baseline\\A2_Avg_{s}.xlsx"
            path_A2_act = f"{pd.read_excel(paths, index_col=[0]).loc['A2',user]}\\Act\\A2_act_Avg_{s}.xlsx"
            path_Act = f"{pd.read_excel(paths, index_col=[0]).loc['Act',user]}\\Act coeff.xlsx"
            path_rec = f"{pd.read_excel(paths, index_col=[0]).loc['metrec_tech',user]}\\metrec_tech_Avg_{s}_Avg.xlsx"
            
            SG2 = pd.read_excel(path_SG2,sheet_name=str(year),index_col=[0,1,2],header= [0,1,2])
            FD = pd.read_excel(path_FD,sheet_name=str(year), index_col=[0,1,2], header= [0,1,2]) 
            #metrec = pd.read_excel(path_metrec,sheet_name=str(year), index_col=[0,1,2], header=[0,1,2])
            A2 = pd.read_excel(path_A2,sheet_name=str(year), index_col=[0,1,2], header=[0,1,2])
            A1_act = pd.read_excel(path_Act,sheet_name='Target consumption', index_col=[0,1,2], header=[0,1,2,3])            
            A2_act = pd.read_excel(path_A2_act,sheet_name=str(year), index_col=[0,1,2], header=[0,1,2])
            A1_act.index = A2_act.index
            met_rec = pd.read_excel(path_rec, sheet_name=str(year),header= [0,1,2], index_col = [0,1,2])
            
            scemario = f"{scen} - {year} - {s}"
            
            if scen == 'Baseline':
        
                if year == 2011:
                    WIOT.clone_scenario(scenario='baseline',name=scemario)
                    
                    z_new = WIOT.matrices[scemario]['z']
                    z_new.update(SG2)
                    
                    Y_new = WIOT.matrices[scemario]['Y']
                    Y_new*=0
                    Y_new.update(FD)
                    
                    z_new.update(A2)
                    
                    WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
                    WIOT.reset_to_coefficients(scenario=scemario)
                    print(scemario)
                    
                    X = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)
                    Z = WIOT.get_data(matrices=['Z'],scenarios= scemario, format='dict',units = False, indeces = False)
                    
                else:
                    WIOT.clone_scenario(scenario=f'{scen} - {year - 1} - {s}',name=scemario)
                        
                    z_new = WIOT.matrices[scemario]['z']
                    z_new.update(SG2)
                    
                    Y_new = WIOT.matrices[scemario]['Y']
                    Y_new*=0
                    Y_new.update(FD)
                    
                    z_new.update(A2)
                    #z[s][year] = z_new
                    WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
                    WIOT.reset_to_coefficients(scenario=scemario)
                    print(scemario)
                
                    X = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)
                    Z = WIOT.get_data(matrices=['Z'],scenarios= scemario, format='dict',units = False, indeces = False)
                    
                Total_Demand[s][year] = Z[scemario]['Z'].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),:].sum(axis =1) - Z[scemario]['Z'].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(['EU27+UK','China','RoW','USA'],'Sector',['Refinery of Generators of Onshore Wind Turbines','Refinery of Generators of Offshore Wind Turbines','Refinery of Silicon layer in PV panel','Refinery of Cu in wires of WT and PV'])].sum(axis =1)#monetary units [M€]
                Recycled_Supply[s][year] = -Z[scemario]['Z'].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(['EU27+UK','China','RoW','USA'],'Sector',['Refinery of Generators of Onshore Wind Turbines','Refinery of Generators of Offshore Wind Turbines','Refinery of Silicon layer in PV panel','Refinery of Cu in wires of WT and PV'])].sum(axis =1)
                Primary_Supply[s][year] = X[scemario]['X'].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),'production'] #monetary units [M€]
                
#%% Calculating  annual emission

E_Total_Demand = {}
E_Recycled_Supply = {}
E_Recycled_Avoided = {}
E_Primary_Supply = {} #Primary == Mining
E_Effective = {}
check = {}
for s in sens:
    E_Total_Demand[s] = pd.DataFrame(0,index= ['Neodymium','Dysprosium', 'Copper', 'Raw silicon'], columns = years)
    E_Recycled_Supply[s] = pd.DataFrame(0,index= ['Neodymium','Dysprosium', 'Copper', 'Raw silicon'], columns = years)
    E_Recycled_Avoided[s] = pd.DataFrame(0,index= ['Neodymium','Dysprosium', 'Copper', 'Raw silicon'], columns = years)
    E_Primary_Supply[s] = pd.DataFrame(0,index= ['Neodymium','Dysprosium', 'Copper', 'Raw silicon'], columns = years)
    E_Effective[s] = pd.DataFrame(0,index= ['Neodymium','Dysprosium', 'Copper', 'Raw silicon'], columns = years)
    check[s] = pd.DataFrame(0,index= ['Neodymium','Dysprosium', 'Copper', 'Raw silicon'], columns = years)
    
for s in sens:
    for year in years:
        E_Total_Demand[s].loc[:,float(year)] = (Total_Demand[s][year] * e_mat.loc[:,"CO2 - combustion - air"]).groupby(level=[2], sort = False).sum()
        E_Recycled_Supply[s].loc[:,float(year)] = (Recycled_Supply[s][year] * e_rec.loc[:,"CO2 - combustion - air"]).groupby(level=[2], sort = False).sum()
        E_Recycled_Avoided[s].loc[:,float(year)] = (Recycled_Supply[s][year] * (e_mat.loc[:,"CO2 - combustion - air"] - e_rec.loc[:,"CO2 - combustion - air"])).groupby(level=[2], sort = False).sum()
        E_Primary_Supply[s].loc[:,float(year)] = (Primary_Supply[s][year] * e_mat.loc[:,"CO2 - combustion - air"]).groupby(level=[2], sort = False).sum()
    E_Effective[s] = E_Primary_Supply[s] + E_Recycled_Supply[s]
    check[s] = E_Total_Demand[s] - E_Recycled_Supply[s] - E_Primary_Supply[s] - E_Recycled_Avoided[s]

    
#%% Calculating cumulative emissions
E_Cum_Total_Demand = {}
E_Cum_Effective = {}
E_Cum_Recycled_Avoided = {}
for s in sens:
    E_Cum_Total_Demand[s] = pd.DataFrame(0,index= ['Neodymium','Dysprosium', 'Copper', 'Raw silicon'], columns = years)
    E_Cum_Effective[s] = pd.DataFrame(0,index= ['Neodymium','Dysprosium', 'Copper', 'Raw silicon'], columns = years)
    E_Cum_Recycled_Avoided[s] = pd.DataFrame(0,index= ['Neodymium','Dysprosium', 'Copper', 'Raw silicon'], columns = years)
    
for s in sens:
    for year in years:
        if year == 2011:
            E_Cum_Total_Demand[s].loc[:,float(year)] = E_Total_Demand[s].loc[:,float(year)]
            E_Cum_Effective[s].loc[:,float(year)] = E_Effective[s].loc[:,float(year)]
            E_Cum_Recycled_Avoided[s].loc[:,float(year)] = E_Recycled_Avoided[s].loc[:,float(year)]
        else:
            E_Cum_Total_Demand[s].loc[:,float(year)] = E_Cum_Total_Demand[s].loc[:,float(year - 1)] + E_Total_Demand[s].loc[:,float(year)]
            E_Cum_Effective[s].loc[:,float(year)] = E_Cum_Effective[s].loc[:,float(year - 1)] + E_Effective[s].loc[:,float(year)]
            E_Cum_Recycled_Avoided[s].loc[:,float(year)] = E_Cum_Recycled_Avoided[s].loc[:,float(year - 1)] + E_Recycled_Avoided[s].loc[:,float(year)]
        

#%% Export Data
for s in sens:
    with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Emissions\\RR\\Annual_Emission_{s}.xlsx") as writer:
            sheet_name = "Total"
            E_Total_Demand[s].to_excel(writer, sheet_name=sheet_name, index=True)
            sheet2_name ="Effective"            
            E_Effective[s].to_excel(writer, sheet_name = sheet2_name,index = True)
            sheet3_name ="Avoided"            
            E_Recycled_Avoided[s].to_excel(writer, sheet_name = sheet3_name,index = True)            
            
    with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Emissions\\RR\\Cumulative_Emission_{s}.xlsx") as writer:
            sheet_name = "Total"
            E_Cum_Total_Demand[s].to_excel(writer, sheet_name=sheet_name, index=True)
            sheet2_name ="Effective"            
            E_Cum_Effective[s].to_excel(writer, sheet_name = sheet2_name,index = True)
            sheet3_name ="Avoided"            
            E_Cum_Recycled_Avoided[s].to_excel(writer, sheet_name = sheet3_name,index = True)
