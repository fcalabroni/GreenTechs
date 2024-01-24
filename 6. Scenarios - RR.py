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
price.index = pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 16, ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']*4])

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
        Critical_met_world_base[s][year] = pd.DataFrame(0, index= pd.MultiIndex.from_arrays([['World']*4, ['Sector']*4 , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']]), columns=['production'])

Greentech_base = {}
for s in sens:
    Greentech_base[s] = {}
    for year in years:
        Greentech_base[s][year] = {}

Greentech_mat_base = {}
for s in sens:
    Greentech_mat_base[s] = {}
    for year in years:
        Greentech_mat_base[s][year] = {} #pd.DataFrame(0, index= pd.MultiIndex.from_arrays([['EU27+UK']*4, ['Sector']*4 , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']]),columns = pd.MultiIndex.from_arrays([['EU27+UK']*3,['Sector']*3,['Offshore wind plants','Onshore wind plants','Photovoltaic plants']]))

        
Results_world_base = {}
for s in sens:
    Results_world_base[s] = pd.DataFrame(0,index= pd.MultiIndex.from_arrays([['World']*4, ['Sector']*4 , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']]), columns = years)

Results_region_base = {}
for s in sens:
    Results_region_base[s] = pd.DataFrame(0,index= pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 16, ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']*4]), columns = years)

Cumulative_world_base = {}
for s in sens:
    Cumulative_world_base[s] = pd.DataFrame(0,index= pd.MultiIndex.from_arrays([['World']*4, ['Sector']*4 , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']]), columns = years)

Cumulative_region_base = {}
for s in sens:
    Cumulative_region_base[s] = pd.DataFrame(0,index= pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 16, ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']*4]), columns = years)

met_rec = {}    
for s in sens:
    met_rec[s] = {}

EOL_RIR_base = {}
for t in techs:
    EOL_RIR_base[t] = {}
    for s in sens:
        EOL_RIR_base[t][s] = pd.DataFrame(0, index = pd.MultiIndex.from_arrays([['EU27+UK']*4, ['Sector']*4, ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']]), columns = years)

# Z_Cu = {}
# for s in sens:
#     Z_Cu[s] = {}    
#     for year in years:
#         Z_Cu[s][year]= {}
#Useful only for some checks 
# z = {}  
# for s in sens:
#     z[s] = {}
#     for year in years:
#         z[s][year] = {}

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
                    Y = WIOT.get_data(matrices=['Y'],scenarios=scemario,format='dict',units = False, indeces = False)
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
                
                #Z_Cu[s][year] = Z[scemario]['Z'].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Copper'),:]
                #Critical materials consumption in physical units [ton] for each region for each year
                Critical_met_base[s][year] = ((X[scemario]['X'].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),'production'] * 10**6 )/ (price.loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),'Avg'] * USD_to_EUR.loc['EURO/USD',year] ))* 10**-3
                #Consumption of critical materials by green techs divided in country of origin
                Greentech_base[s][year] = Z[scemario]['Z'].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(['EU27+UK','China','RoW','USA'],'Sector',['Offshore wind plants','Onshore wind plants','Photovoltaic plants'])] #monetary units [M€]
                for r in region:
                    Greentech_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(r,'Sector','Offshore wind plants')] = ((Greentech_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(r,'Sector','Offshore wind plants')]* 10**6 )/ (price.loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),'Avg'] * USD_to_EUR.loc['EURO/USD',year] ))* 10**-3  #physical unit [ton]
                    Greentech_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(r,'Sector','Onshore wind plants')] = ((Greentech_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(r,'Sector','Onshore wind plants')]* 10**6 )/ (price.loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),'Avg'] * USD_to_EUR.loc['EURO/USD',year] ))* 10**-3
                    Greentech_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(r,'Sector','Photovoltaic plants')] = ((Greentech_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(r,'Sector','Photovoltaic plants')]* 10**6 )/ (price.loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),'Avg'] * USD_to_EUR.loc['EURO/USD',year] ))* 10**-3
                    #Consumption of critical materials by green techs without distinction from country of origin
                    Greentech_mat_base[s][year].loc[(r,'Sector','Neodymium')] = Greentech_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Neodymium'),(r, 'Sector', ['Offshore wind plants','Onshore wind plants','Photovoltaic plants'])].sum()
                    Greentech_mat_base[s][year].loc[(r,'Sector','Dysprosium')] = Greentech_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Dysprosium'),(r, 'Sector', ['Offshore wind plants','Onshore wind plants','Photovoltaic plants'])].sum()
                    Greentech_mat_base[s][year].loc[(r,'Sector','Copper')] = Greentech_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Copper'),(r, 'Sector', ['Offshore wind plants','Onshore wind plants','Photovoltaic plants'])].sum()
                    Greentech_mat_base[s][year].loc[(r,'Sector','Raw silicon')] = Greentech_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Raw silicon'),(r, 'Sector', ['Offshore wind plants','Onshore wind plants','Photovoltaic plants'])].sum()
                #Critical materials consumption in physical units [ton] in the world           
                Critical_met_world_base[s][year].loc[('World','Sector','Neodymium')] = Critical_met_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Neodymium')].sum()
                Critical_met_world_base[s][year].loc[('World','Sector','Dysprosium')] = Critical_met_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Dysprosium')].sum()
                Critical_met_world_base[s][year].loc[('World','Sector','Copper')] = Critical_met_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' ,'Copper')].sum()
                Critical_met_world_base[s][year].loc[('World','Sector','Raw silicon')] = Critical_met_base[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Raw silicon')].sum()
                #Reshaping results to export as wanted
                Results_world_base[s].loc[:,float(year)]= Critical_met_world_base[s][year].loc[:,'production']
            
                Results_region_base[s].loc[:,float(year)]= Critical_met_base[s][year].loc[:]
                #Calculation of cumulative consumption of critical materials
                if year == 2011:
                    Cumulative_region_base[s].loc[:,float(year)] = Results_region_base[s].loc[:,float(year)]
                    Cumulative_world_base[s].loc[:,float(year)] = Results_world_base[s].loc[:,float(year)]
                else:
                    Cumulative_region_base[s].loc[:,float(year)] = Cumulative_region_base[s].loc[:,float(year - 1)] + Results_region_base[s].loc[:,float(year)]
                    Cumulative_world_base[s].loc[:,float(year)] = Cumulative_world_base[s].loc[:,float(year - 1)] + Results_world_base[s].loc[:,float(year)]

                #Calculating EoL- RIR Indicator
                # for t in techs:
                #     EOL_RIR_base[t][s].loc[:,year] = met_rec.loc[:,('EU27+UK','Sector',t)]/(Greentech_mat_base[s][year].loc[:,('EU27+UK','Sector',t)])
                #     EOL_RIR_base[t][s] = EOL_RIR_base[t][s].fillna(0)
                
#%%  Export Data BASELINE RR sens
for s in sens:
    with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Baseline\\RR\\Results_world_base_RR_{s}.xlsx") as writer:
            sheet_name = "Annual production"
            Results_world_base[s].to_excel(writer, sheet_name=sheet_name, index=True)
            sheet2_name ="Cumulative"            
            Cumulative_world_base[s].to_excel(writer, sheet_name = sheet2_name,index = True)
            
    with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Baseline\\RR\\Results_region_base_RR_{s}.xlsx") as writer:
            sheet_name = "Annual production"
            Results_region_base[s].to_excel(writer, sheet_name=sheet_name, index=True)
            sheet2_name ="Cumulative"            
            Cumulative_region_base[s].to_excel(writer, sheet_name = sheet2_name,index = True)

# for t in techs:
#         with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Baseline\\EoL-RIR\\EoL-RIR_base_{t}.xlsx") as writer:
#             for key, df in EOL_RIR_base[t].items():
#                 sheet_name = f'RR_{key}'
#                 df.to_excel(writer, sheet_name=sheet_name, index= True)
            
#%% ACT with sensitivity on Recycling Rate (Weib = Avg, price = Avg)
fileParam = f"{pd.read_excel(paths, index_col=[0]).loc['fileParam',user]}"
RR_upgrade =  pd.read_excel(fileParam, "RR", index_col=[0])
Weibull_params =  pd.read_excel(fileParam, "Weibull", index_col=[0,1])
#sens = list(set(RR_upgrade.index.get_level_values(0)))
sens = ['hist', 'target', 'full']
region = pd.read_excel(fileParam, "region",header = None, index_col=[0])
region = list(region.index.get_level_values(0))
scenario = ['Baseline','Act']
techs = list(set(Weibull_params.index.get_level_values(0)))

price_materials = pd.read_excel(fileParam,sheet_name='price materials', index_col=[0], header=[0])
price = pd.concat([price_materials] * 4, ignore_index= True) #unit of price [USD/kg]
price.index = pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 16, ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']*4])

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
        Critical_met_world_act[s][year] = pd.DataFrame(0, index= pd.MultiIndex.from_arrays([['World']*4, ['Sector']*4 , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']]), columns=['production'])

Greentech_act = {}
for s in sens:
    Greentech_act[s] = {}
    for year in years:
        Greentech_act[s][year] = {}

Greentech_mat_act = {}
for s in sens:
    Greentech_mat_act[s] = {}
    for year in years:
        Greentech_mat_act[s][year] = {}#pd.DataFrame(0, index= pd.MultiIndex.from_arrays([['EU27+UK']*4, ['Sector']*4 , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']]),columns = pd.MultiIndex.from_arrays([['EU27+UK']*3,['Sector']*3,['Offshore wind plants','Onshore wind plants','Photovoltaic plants']]))

Results_world_act = {}
for s in sens:
    Results_world_act[s] = pd.DataFrame(0,index= pd.MultiIndex.from_arrays([['World']*4, ['Sector']*4 , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']]), columns = years)

Results_region_act = {}
for s in sens:
    Results_region_act[s] = pd.DataFrame(0,index= pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 16, ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']*4]), columns = years)

Cumulative_world_act = {}
for s in sens:
    Cumulative_world_act[s] = pd.DataFrame(0,index= pd.MultiIndex.from_arrays([['World']*4, ['Sector']*4 , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']]), columns = years)

Cumulative_region_act = {}
for s in sens:
    Cumulative_region_act[s] = pd.DataFrame(0,index= pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 16, ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']*4]), columns = years)

met_rec = {}    
for s in sens:
    met_rec[s] = {}

EOL_RIR_act = {}
for t in techs:
    EOL_RIR_act[t] = {}
    for s in sens:
        EOL_RIR_act[t][s] = pd.DataFrame(0, index = pd.MultiIndex.from_arrays([['EU27+UK']*4, ['Sector']*4, ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']]), columns = years)
         
#Useful only for some check 
# z = {}  
# for s in sens:
#     z[s] = {}
#     for year in years:
#         z[s][year] = {}
        
for scen in ['Act']:   
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
            met_rec = pd.read_excel(path_rec, sheet_name=str(year),header= [0,1,2], index_col = [0,1,2])
            A1_act.index = A2_act.index
            
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
                    Z = WIOT.get_data(matrices=['Z'],scenarios= scemario, format='dict',units = False, indeces = False)
                    
                elif year == list(range(2012,2024)):
                    WIOT.clone_scenario(scenario=f'{scen} - {year - 1} - {s}',name=scemario)
                        
                    z_new = WIOT.matrices[scemario]['z']
                    z_new.update(SG2)
                    
                    Y_new = WIOT.matrices[scemario]['Y']
                    Y_new*=0
                    Y_new.update(FD)
                    
                    z_new.update(A2_act)
                    #z[s][year] = z_new
                    WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
                    WIOT.reset_to_coefficients(scenario=scemario)
                    print(scemario)
                
                    X = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)
                    Z = WIOT.get_data(matrices=['Z'],scenarios= scemario, format='dict',units = False, indeces = False)
                    
                elif year == list(range(2024,2031)):
                    WIOT.clone_scenario(scenario=f'{scen} - {year - 1} - {s}',name=scemario)
                        
                    z_new = WIOT.matrices[scemario]['z']
                    z_new.update(SG2)
                    
                    Y_new = WIOT.matrices[scemario]['Y']
                    Y_new*=0
                    Y_new.update(FD)
                    
                    z_new.update(A2_act)
                    z_new.update(A1_act.loc[:,year])
                    #z[s][year] = z_new
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
                    
                    z_new.update(A2_act)
                    z_new.update(A1_act.loc[:,2030])
                    #z[s][year] = z_new
                    WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
                    WIOT.reset_to_coefficients(scenario=scemario)
                    print(scemario)
                
                    X = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)
                    Z = WIOT.get_data(matrices=['Z'],scenarios= scemario, format='dict',units = False, indeces = False)
                
                Critical_met_act[s][year] = ((X[scemario]['X'].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),'production'] * 10**6 )/ (price.loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),'Avg'] * USD_to_EUR.loc['EURO/USD',year] ))* 10**-3
                # #Consumption of critical materials by green techs divided in country of origin
                Greentech_act[s][year] = Z[scemario]['Z'].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(['EU27+UK','China','RoW','USA'],'Sector',['Offshore wind plants','Onshore wind plants','Photovoltaic plants'])] #monetary units [M€]
                for r in region:
                    Greentech_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(r,'Sector','Offshore wind plants')] = ((Greentech_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(r,'Sector','Offshore wind plants')]* 10**6 )/ (price.loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),'Avg'] * USD_to_EUR.loc['EURO/USD',year] ))* 10**-3  #physical unit [ton]
                    Greentech_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(r,'Sector','Onshore wind plants')] = ((Greentech_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(r,'Sector','Onshore wind plants')]* 10**6 )/ (price.loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),'Avg'] * USD_to_EUR.loc['EURO/USD',year] ))* 10**-3
                    Greentech_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(r,'Sector','Photovoltaic plants')] = ((Greentech_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),(r,'Sector','Photovoltaic plants')]* 10**6 )/ (price.loc[(['EU27+UK','China','RoW','USA'], 'Sector' , ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']),'Avg'] * USD_to_EUR.loc['EURO/USD',year] ))* 10**-3
                    #Consumption of critical materials by green techs without distinction from country of origin
                    Greentech_mat_act[s][year].loc[('EU27+UK','Sector','Neodymium')] = Greentech_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Neodymium')].sum()
                    Greentech_mat_act[s][year].loc[('EU27+UK','Sector','Dysprosium')] = Greentech_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Dysprosium')].sum()
                    Greentech_mat_act[s][year].loc[('EU27+UK','Sector','Copper')] = Greentech_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Copper')].sum()
                    Greentech_mat_act[s][year].loc[('EU27+UK','Sector','Raw silicon')] = Greentech_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Raw silicon')].sum()
                                 
                Critical_met_world_act[s][year].loc[('World','Sector','Neodymium')] = Critical_met_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Neodymium')].sum()
                Critical_met_world_act[s][year].loc[('World','Sector','Dysprosium')] = Critical_met_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Dysprosium')].sum()
                Critical_met_world_act[s][year].loc[('World','Sector','Copper')] = Critical_met_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' ,'Copper')].sum()
                Critical_met_world_act[s][year].loc[('World','Sector','Raw silicon')] = Critical_met_act[s][year].loc[(['EU27+UK','China','RoW','USA'], 'Sector' , 'Raw silicon')].sum()
            
                Results_world_act[s].loc[:,float(year)]= Critical_met_world_act[s][year].loc[:,'production']
            
                Results_region_act[s].loc[:,float(year)]= Critical_met_act[s][year].loc[:]
                
                if year == 2011:
                    Cumulative_region_act[s].loc[:,float(year)] = Results_region_act[s].loc[:,float(year)]
                    Cumulative_world_act[s].loc[:,float(year)] = Results_world_act[s].loc[:,float(year)]
                else:
                    Cumulative_region_act[s].loc[:,float(year)] = Cumulative_region_act[s].loc[:,float(year - 1)] + Results_region_act[s].loc[:,float(year)]
                    Cumulative_world_act[s].loc[:,float(year)] = Cumulative_world_act[s].loc[:,float(year - 1)] + Results_world_act[s].loc[:,float(year)]
                    
                # #Calculating EoL- RIR Indicator
                # for t in techs:
                #     EOL_RIR_act[t][s].loc[:,year] = met_rec.loc[:,('EU27+UK','Sector',t)]/(Greentech_mat_act[s][year].loc[:,('EU27+UK','Sector',t)])
                #     EOL_RIR_act[t][s] = EOL_RIR_act[t][s].fillna(0)
                    
#%% Export Data ACT RR sens 
for s in sens:    
    with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Act\\RR\\Results_world_act_RR_{s}.xlsx") as writer:
            sheet_name = "Annual production"
            Results_world_act[s].to_excel(writer, sheet_name=sheet_name, index=True)            
            sheet2_name ="Cumulative"            
            Cumulative_world_act[s].to_excel(writer, sheet_name = sheet2_name,index = True)
            
    with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Act\\RR\\Results_region_act_RR_{s}.xlsx") as writer:
            sheet_name = "Annual production"
            Results_region_act[s].to_excel(writer, sheet_name=sheet_name, index=True)
            sheet2_name ="Cumulative"            
            Cumulative_region_act[s].to_excel(writer, sheet_name = sheet2_name,index = True)
            
# for t in techs:
#         with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Act\\EoL-RIR\\EoL-RIR_act_{t}.xlsx") as writer:
#             for key, df in EOL_RIR_act[t].items():
#                 sheet_name = f'RR_{key}'
#                 df.to_excel(writer, sheet_name=sheet_name, index= True)
        

