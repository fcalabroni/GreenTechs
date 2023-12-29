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
#%%
fileParam = f"{pd.read_excel(paths, index_col=[0]).loc['fileParam',user]}"
Weibull_params =  pd.read_excel(fileParam, "Weibull", index_col=[0,1])
sens = list(set(Weibull_params.index.get_level_values(1)))
region = 'EU27+UK'

metrecs = {}
for year in years:
    metrecs[year] = {}

Critical_met = {}
for s in sens:
    Critical_met[s] = {}
    for year in years:
        Critical_met[s][year] = {}

Old = {}  
for s in sens:
    Old[s] = {}
    for year in years:
        Old[s][year] = {}

Coeff = {}  
for s in sens:
    Coeff[s] = {}
    for year in years:
        Coeff[s][year] = {}

z = {}  
for s in sens:
    z[s] = {}
    for year in years:
        z[s][year] = {}
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




for year in years:
    for s in ['Avg']:
        path_SG2 = f"{pd.read_excel(paths, index_col=[0]).loc['SG2',user]}\\SG2_{s}.xlsx"
        path_FD = f"{pd.read_excel(paths, index_col=[0]).loc['FD Total',user]}\\FD_total_{s}.xlsx"
        path_metrec = f"{pd.read_excel(paths, index_col=[0]).loc['metrec',user]}\\metrec_{s}_b2.xlsx"
        
        SG2 = pd.read_excel(path_SG2,sheet_name=str(year),index_col=[0,1,2],header= [0,1,2])
        FD = pd.read_excel(path_FD,sheet_name=str(year), index_col=[0,1,2], header= [0,1,2]) #check indici
        metrec = pd.read_excel(path_metrec,sheet_name=str(year), index_col=[0,1,2], header=[0,1,2])
        
        metrecs[year] = metrec
        
        scemario = f"{year} - {s}"
        
        if year == 2011:
            WIOT.clone_scenario(scenario='baseline',name=scemario)
            
            z_new = WIOT.matrices[scemario]['z']
            z_new.update(SG2)
            
            Y_new = WIOT.matrices[scemario]['Y']
            Y_new*=0
            Y_new.update(FD)
            
            WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
            WIOT.reset_to_coefficients(scenario=scemario)
            print(scemario)
            
            X = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)
            
        else:
            WIOT.clone_scenario(scenario=f'{year - 1} - {s}',name=scemario)
                
            z_new = WIOT.matrices[scemario]['z']
            z_new.update(SG2)
            
            Y_new = WIOT.matrices[scemario]['Y']
            Y_new*=0
            Y_new.update(FD)
            
            X_old = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)
            Old[s][year] = X_old[scemario]['X']
            metnat_data = X_old[scemario]['X'].loc[('EU27+UK', 'Sector' , ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']),'production']
            metnat = np.diag(metnat_data)

            coeff_rec = pd.DataFrame(0, index= metrec.index, columns = metrec.columns )
            coeff_rec = metrecs[year - 1] @ np.linalg.inv(metnat)  
            coeff_rec.columns = pd.MultiIndex.from_arrays([['EU27+UK'] * len(ref), ['Sector'] * len(ref), ref],names=['Region', 'Level', 'Item'])
            Coeff[s][year] = coeff_rec
            z_new.update(coeff_rec)
            z[s][year] = z_new
            WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
            WIOT.reset_to_coefficients(scenario=scemario)
            print(scemario)

            X = WIOT.get_data(matrices=['X'],scenarios= scemario, format='dict',units = False, indeces = False)
        
        Critical_met[s][year] = X[scemario]['X'].loc[('EU27+UK', 'Sector' , ['Neodymium','Dysprosium', 'Copper ores and concentrates', 'Raw silicon']),'production']








    
#%%  Aggregated database with new sectors to txt
for year in years:
    world[year].to_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\e. WIOT\\{year}", flows=True, coefficients=True)

