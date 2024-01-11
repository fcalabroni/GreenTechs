import mario
import pandas as pd
import numpy as np

user = "MBV"
sN = slice(None)
years = range(2011,2101)

paths = 'Paths.xlsx'

#%% Parse and SUT to IOT

# world = {}

# for year in years:
#     world[year] = mario.parse_from_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\d. Baseline\\2011\\flows", table='SUT', mode="coefficients")
#     world[year].to_iot(method='B')

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
# for year in years:
#     world[year].add_sectors(io=path_waste_sector, new_sectors= waste_sectors, regions= [world[year].get_index('Region')[1]], item='Sectors', inplace=True)

WIOT.add_sectors(io=path_waste_sector, new_sectors= waste_sectors, regions= [WIOT.get_index('Region')[1]], item='Sectors', inplace=True)

#%% BASELINE with sensitivity on Recycling Rate (Lifetime = Avg, price = Avg)
fileParam = f"{pd.read_excel(paths, index_col=[0]).loc['fileParam',user]}"
RR_upgrade =  pd.read_excel(fileParam, "RR", index_col=[0]) #fix
sens = list(set(RR_upgrade.index.get_level_values(0)))
region = 'EU27+UK'
scenario = ['Baseline','Act']

price_materials = pd.read_excel(fileParam,sheet_name='price materials', index_col=[0], header=[0])
price = pd.concat([price_materials] * 4, ignore_index= True) #unit of price [USD/kg]
price.index = pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 16, ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']*4])

USD_to_EUR = pd.read_excel(fileParam,"USD to EURO", header=0, index_col=0)

#Dictionary for data from Baseline scenario
Critical_met_base = {}
for s in sens:
    Critical_met_base[s] = {}
    for year in years:
        Critical_met_base[s][year] = {}

Critical_met_world_base = {}
for s in sens:
    Critical_met_world_base[s] = {}
    for year in years:
        Critical_met_world_base[s][year] = pd.DataFrame(0, index= pd.MultiIndex.from_arrays([['World']*4, ['Sector']*4 , ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']]), columns=['production'])

Results_world_base = {}
for s in sens:
    Results_world_base[s] = pd.DataFrame(0,index= pd.MultiIndex.from_arrays([['World']*4, ['Sector']*4 , ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']]), columns = years)

Results_region_base = {}
for s in sens:
    Results_region_base[s] = pd.DataFrame(0,index= pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 16, ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']*4]), columns = years)

#Useful only for some check 
z = {}  
for s in sens:
    z[s] = {}
    for year in years:
        z[s][year] = {}

# metrecs = {}
# for year in years:
#     metrecs[year] = {}
      
# Old = {}  
# for s in sens:
#     Old[s] = {}
#     for year in years:
#         Old[s][year] = {}

# Coeff = {}  
# for s in sens:
#     Coeff[s] = {}
#     for year in years:
#         Coeff[s][year] = {}
for scen in ['Baseline']:   
    for year in years:
        for s in sens:
            path_SG2 = f"{pd.read_excel(paths, index_col=[0]).loc['SG2',user]}\\SG2_Avg.xlsx"
            path_FD = f"{pd.read_excel(paths, index_col=[0]).loc['FD Total',user]}\\FD_total_Avg.xlsx"
            #path_metrec = f"{pd.read_excel(paths, index_col=[0]).loc['metrec',user]}\\metrec_{s}_b2.xlsx"
            path_A2 = f"{pd.read_excel(paths, index_col=[0]).loc['A2',user]}\\Baseline\\A2_Avg_{s}.xlsx"
            path_A2_act = f"{pd.read_excel(paths, index_col=[0]).loc['A2',user]}\\Act\\A2_act_Avg_{s}.xlsx"
            path_Act = f"{pd.read_excel(paths, index_col=[0]).loc['Act',user]}\\Act coeff.xlsx"
            
            SG2 = pd.read_excel(path_SG2,sheet_name=str(year),index_col=[0,1,2],header= [0,1,2])
            FD = pd.read_excel(path_FD,sheet_name=str(year), index_col=[0,1,2], header= [0,1,2]) 
            #metrec = pd.read_excel(path_metrec,sheet_name=str(year), index_col=[0,1,2], header=[0,1,2])
            A2 = pd.read_excel(path_A2,sheet_name=str(year), index_col=[0,1,2], header=[0,1,2])
            A1_act = pd.read_excel(path_Act,sheet_name='Target consumption', index_col=[0,1,2], header=[0,1,2,3])
            A2_act = pd.read_excel(path_A2_act,sheet_name=str(year), index_col=[0,1,2], header=[0,1,2])
            #metrecs[year] = metrec
            
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
                    
                else:
                    WIOT.clone_scenario(scenario=f'{scen} - {year - 1} - {s}',name=scemario)
                        
                    z_new = WIOT.matrices[scemario]['z']
                    z_new.update(SG2)
                    
                    Y_new = WIOT.matrices[scemario]['Y']
                    Y_new*=0
                    Y_new.update(FD)
                    
                    z_new.update(A2)
                    z[s][year] = z_new
                    WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
                    WIOT.reset_to_coefficients(scenario=scemario)
                    print(scemario)
                
                    X = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)
                
                Critical_met_base[s][year] = ((X[scemario]['X'].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']),'production'] * 10**6 )/ (price.loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']),'Avg'] * USD_to_EUR.loc['EURO/USD',year] ))* 10**-3
            
                
                Critical_met_world_base[s][year].loc[('World','Sector','Neodymium')] = Critical_met_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Neodymium')].sum()
                Critical_met_world_base[s][year].loc[('World','Sector','Dysprosium')] = Critical_met_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Dysprosium')].sum()
                Critical_met_world_base[s][year].loc[('World','Sector','Copper ores and concentrates')] = Critical_met_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' ,'Copper ores and concentrates')].sum()
                Critical_met_world_base[s][year].loc[('World','Sector','Raw silicon')] = Critical_met_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Raw silicon')].sum()
            
                Results_world_base[s].loc[:,float(year)]= Critical_met_world_base[s][year].loc[:,'production']
            
                Results_region_base[s].loc[:,float(year)]= Critical_met_base[s][year].loc[:]
                

        
#%%  Export Data BASELINE RR sens
for s in sens:
    with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Baseline\\RR\\Results_world_base_RR_{s}.xlsx") as writer:
            sheet_name = "Crit_met_world"
            Results_world_base[s].to_excel(writer, sheet_name=sheet_name, index=True)
            
    with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Baseline\\RR\\Results_region_base_RR_{s}.xlsx") as writer:
            sheet_name = "Crit_met_world"
            Results_region_base[s].to_excel(writer, sheet_name=sheet_name, index=True)
            
#%% ACT with sensitivity on Recycling Rate (Weib = Avg, price = Avg)
fileParam = f"{pd.read_excel(paths, index_col=[0]).loc['fileParam',user]}"
RR_upgrade =  pd.read_excel(fileParam, "RR", index_col=[0]) #fix
sens = list(set(RR_upgrade.index.get_level_values(0)))
region = 'EU27+UK'
scenario = ['Baseline','Act']

price_materials = pd.read_excel(fileParam,sheet_name='price materials', index_col=[0], header=[0])
price = pd.concat([price_materials] * 4, ignore_index= True) #unit of price [USD/kg]
price.index = pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 16, ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']*4])

USD_to_EUR = pd.read_excel(fileParam,"USD to EURO", header=0, index_col=0)

#Dictionaries for data from Act scenario
Critical_met_act = {}
for s in sens:
    Critical_met_act[s] = {}
    for year in years:
        Critical_met_act[s][year] = {}

Critical_met_world_act = {}
for s in sens:
    Critical_met_world_act[s] = {}
    for year in years:
        Critical_met_world_act[s][year] = pd.DataFrame(0, index= pd.MultiIndex.from_arrays([['World']*4, ['Sector']*4 , ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']]), columns=['production'])

Results_world_act = {}
for s in sens:
    Results_world_act[s] = pd.DataFrame(0,index= pd.MultiIndex.from_arrays([['World']*4, ['Sector']*4 , ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']]), columns = years)

Results_region_act = {}
for s in sens:
    Results_region_act[s] = pd.DataFrame(0,index= pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 16, ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']*4]), columns = years)

#Useful only for some check 
z = {}  
for s in sens:
    z[s] = {}
    for year in years:
        z[s][year] = {}
        
for scen in ['Act']:   
    for year in years:
        for s in sens:
            path_SG2 = f"{pd.read_excel(paths, index_col=[0]).loc['SG2',user]}\\SG2_Avg.xlsx"
            path_FD = f"{pd.read_excel(paths, index_col=[0]).loc['FD Total',user]}\\FD_total_Avg.xlsx"
            #path_metrec = f"{pd.read_excel(paths, index_col=[0]).loc['metrec',user]}\\metrec_{s}_b2.xlsx"
            path_A2 = f"{pd.read_excel(paths, index_col=[0]).loc['A2',user]}\\Baseline\\A2_Avg_{s}.xlsx"
            path_A2_act = f"{pd.read_excel(paths, index_col=[0]).loc['A2',user]}\\Act\\A2_act_Avg_{s}.xlsx"
            path_Act = f"{pd.read_excel(paths, index_col=[0]).loc['Act',user]}\\Act coeff.xlsx"
            
            SG2 = pd.read_excel(path_SG2,sheet_name=str(year),index_col=[0,1,2],header= [0,1,2])
            FD = pd.read_excel(path_FD,sheet_name=str(year), index_col=[0,1,2], header= [0,1,2]) 
            #metrec = pd.read_excel(path_metrec,sheet_name=str(year), index_col=[0,1,2], header=[0,1,2])
            A2 = pd.read_excel(path_A2,sheet_name=str(year), index_col=[0,1,2], header=[0,1,2])
            A1_act = pd.read_excel(path_Act,sheet_name='Target consumption', index_col=[0,1,2], header=[0,1,2,3])
            A2_act = pd.read_excel(path_A2_act,sheet_name=str(year), index_col=[0,1,2], header=[0,1,2])
            #metrecs[year] = metrec
            
            scemario = f"{scen} - {year} - {s}" 
            
            if scen == 'Act':
                
                if year == 2011:
                    WIOT.clone_scenario(scenario='baseline',name=scemario)
                    
                    z_new = WIOT.matrices[scemario]['z']
                    z_new.update(SG2)
                    
                    Y_new = WIOT.matrices[scemario]['Y']
                    Y_new*=0
                    Y_new.update(FD)
                    
                    z_new.update(A2_act)
                    
                    WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
                    WIOT.reset_to_coefficients(scenario=scemario)
                    print(scemario)
                    
                    X = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)
                    
                elif year == list(range(2012,2024)):
                    WIOT.clone_scenario(scenario=f'{scen} - {year - 1} - {s}',name=scemario)
                        
                    z_new = WIOT.matrices[scemario]['z']
                    z_new.update(SG2)
                    
                    Y_new = WIOT.matrices[scemario]['Y']
                    Y_new*=0
                    Y_new.update(FD)
                    
                    z_new.update(A2_act)
                    z[s][year] = z_new
                    WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
                    WIOT.reset_to_coefficients(scenario=scemario)
                    print(scemario)
                
                    X = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)
                
                elif year == list(range(2024,2031)):
                    WIOT.clone_scenario(scenario=f'{scen} - {year - 1} - {s}',name=scemario)
                        
                    z_new = WIOT.matrices[scemario]['z']
                    z_new.update(SG2)
                    
                    Y_new = WIOT.matrices[scemario]['Y']
                    Y_new*=0
                    Y_new.update(FD)
                    
                    z_new.update(A2_act)
                    z_new.update(A1_act.loc[:,year])
                    z[s][year] = z_new
                    WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
                    WIOT.reset_to_coefficients(scenario=scemario)
                    print(scemario)
                
                    X = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)
            
                else:
                    WIOT.clone_scenario(scenario=f'{scen} - {year - 1} - {s}',name=scemario)
                        
                    z_new = WIOT.matrices[scemario]['z']
                    z_new.update(SG2)
                    
                    Y_new = WIOT.matrices[scemario]['Y']
                    Y_new*=0
                    Y_new.update(FD)
                    
                    z_new.update(A2_act)
                    z_new.update(A1_act.loc[:,2030])
                    z[s][year] = z_new
                    WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
                    WIOT.reset_to_coefficients(scenario=scemario)
                    print(scemario)
                
                    X = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)
                
                Critical_met_act[s][year] = ((X[scemario]['X'].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']),'production'] * 10**6 )/ (price.loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']),'Avg'] * USD_to_EUR.loc['EURO/USD',year] ))* 10**-3
            
                Critical_met_world_act[s][year].loc[('World','Sector','Neodymium')] = Critical_met_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Neodymium')].sum()
                Critical_met_world_act[s][year].loc[('World','Sector','Dysprosium')] = Critical_met_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Dysprosium')].sum()
                Critical_met_world_act[s][year].loc[('World','Sector','Copper ores and concentrates')] = Critical_met_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' ,'Copper ores and concentrates')].sum()
                Critical_met_world_act[s][year].loc[('World','Sector','Raw silicon')] = Critical_met_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Raw silicon')].sum()
            
                Results_world_act[s].loc[:,float(year)]= Critical_met_world_act[s][year].loc[:,'production']
            
                Results_region_act[s].loc[:,float(year)]= Critical_met_act[s][year].loc[:]
               
            
#%% Export Data ACT RR sens 
for s in sens:    
    with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Act\\RR\\Results_world_act_RR_{s}.xlsx") as writer:
            sheet_name = "Crit_met_world"
            Results_world_act[s].to_excel(writer, sheet_name=sheet_name, index=True)
            
    with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Act\\RR\\Results_region_act_RR_{s}.xlsx") as writer:
            sheet_name = "Crit_met_world"
            Results_region_act[s].to_excel(writer, sheet_name=sheet_name, index=True)


#%% OLD
# for year in years:
#     for s in ['Avg']:#sens:
#         path_SG2 = f"{pd.read_excel(paths, index_col=[0]).loc['SG2',user]}\\SG2_{s}.xlsx"
#         path_FD = f"{pd.read_excel(paths, index_col=[0]).loc['FD Total',user]}\\FD_total_{s}.xlsx"
#         path_metrec = f"{pd.read_excel(paths, index_col=[0]).loc['metrec',user]}\\metrec_{s}_b2.xlsx"
        
#         SG2 = pd.read_excel(path_SG2,sheet_name=str(year),index_col=[0,1,2],header= [0,1,2])
#         FD = pd.read_excel(path_FD,sheet_name=str(year), index_col=[0,1,2], header= [0,1,2]) #check indici
#         metrec = pd.read_excel(path_metrec,sheet_name=str(year), index_col=[0,1,2], header=[0,1,2])
        
#         metrecs[year] = metrec
#         metnat[year] = pd.DataFrame(0, index= metrec.index, columns = metrec.columns )
#         #for y in SG2:
#         #for y,matr in FD.items():
#             #mat.columns = mat.index
#             #SG2[y] = mat
#             #FD[y] = matr
#             #y = int{y}
            
#         scemario = f"{year} - {s}"
#         #world[year].clone_scenario(scenario='baseline',name=scemario)
#         WIOT.clone_scenario(scenario='baseline',name=scemario)
        
#         # z_new = world[year].matrices[scemario]['z']
#         # z_new.update(SG2[y])
#         #z_new.loc[(region,'Sector',list(SG2[y].index)),(region,'Sector',list(SG2[y].columns))] = SG2[y].values
        
#         z_new = WIOT.matrices[scemario]['z']
#         z_new.update(SG2)#[year])
        
        
#         # Y_new = world[year].matrices[scemario]['Y']
#         # Y_new*=0
#         # Y_new.update(FD[y])
#         #Y_new.loc[(region,'Sector',list(SwFD[y].index)),(region,'Sector','Gross fixed capital formation')] = SwFD[y].values
        
#         Y_new = WIOT.matrices[scemario]['Y']
#         Y_new*=0
#         Y_new.update(FD)#[year])
        
#         z_new2 = WIOT.matrices[scemario]['z']
#         if year == 2011:
#             coeff_rec = pd.DataFrame(0, index= metrec.index, columns = metrec.columns )
#             #coeff_rec = 0
#             #coeff_rec.columns = pd.MultiIndex.from_arrays([['EU27+UK'] * len(ref), ['Sector'] * len(ref), ref],names=['Region', 'Level', 'Item']) 
#         else:
#             coeff_rec = pd.DataFrame(0, index= metrec.index, columns = metrec.columns )
#             coeff_rec = metrecs[year - 1] @ np.linalg.inv(metnat[year - 1])  #il problema è qua
#             coeff_rec.columns = pd.MultiIndex.from_arrays([['EU27+UK'] * len(ref), ['Sector'] * len(ref), ref],names=['Region', 'Level', 'Item'])
#             z_new.update(coeff_rec)
          
#         #X_new = world[year].matrices[scemario]['X']
#         X_new = WIOT.matrices[scemario]['X'] 
#         metnat[year] =np.diag(X_new.loc[('EU27+UK', 'Sector' , ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']),'production'])
#         #metnat[year] =np.diag(WIOT['{year} - {s}']['X'].loc[('EU27+UK', 'Sector' , ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']),'production'])
#         WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
#         WIOT.reset_to_coefficients(scenario=scemario)
#         # world[year].update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
#         # world[year].reset_to_coefficients(scenario=scemario)
#         #WIOT.to_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\e. WIOT\\{year}", flows=True, coefficients=True)
#         print(scemario)


# if year == 2011:
#     WIOT.clone_scenario(scenario='baseline',name=scemario)
    
#     z_new = WIOT.matrices[scemario]['z']
#     z_new.update(SG2)
    
#     Y_new = WIOT.matrices[scemario]['Y']
#     Y_new*=0
#     Y_new.update(FD)
    
#     WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
#     WIOT.reset_to_coefficients(scenario=scemario)
#     print(scemario)
    
#     X = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)
    
# else:
#     WIOT.clone_scenario(scenario=f'{year - 1} - {s}',name=scemario)
        
#     z_new = WIOT.matrices[scemario]['z']
#     z_new.update(SG2)
    
#     Y_new = WIOT.matrices[scemario]['Y']
#     Y_new*=0
#     Y_new.update(FD)
    
#     X_old = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)
#     Old[s][year] = X_old[scemario]['X']
#     metnat_data = X_old[scemario]['X'].loc[('EU27+UK', 'Sector' , ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']),'production']
#     metnat = np.diag(metnat_data)

#     coeff_rec = pd.DataFrame(0, index= metrec.index, columns = metrec.columns )
#     coeff_rec = metrecs[year - 1] @ np.linalg.inv(metnat)  
#     coeff_rec.columns = pd.MultiIndex.from_arrays([['EU27+UK'] * len(ref), ['Sector'] * len(ref), ref],names=['Region', 'Level', 'Item'])
#     Coeff[s][year] = coeff_rec
#     z_new.update(coeff_rec)
#     z[s][year] = z_new
#     WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
#     WIOT.reset_to_coefficients(scenario=scemario)
#     print(scemario)

#     X = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)

# Critical_met[s][year] = X[scemario]['X'].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']),'production']
