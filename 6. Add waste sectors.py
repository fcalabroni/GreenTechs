import mario
import pandas as pd

user = "MBV"
sN = slice(None)
years = range(2011,2012)

paths = 'Paths.xlsx'

#%% Parse and SUT to IOT

world = {}

for year in years:
    world[year] = mario.parse_from_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\d. Baseline\\2011\\flows", table='SUT', mode="coefficients")
    world[year].to_iot(method='B')

#WIOT = mario.parse_from_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\d. Baseline\\2011\\flows", table='SUT', mode="coefficients")
#WIOT.to_iot(method='B')
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

#%% Getting excel templates to add waste sectors
path_waste_sector = f"{pd.read_excel(paths, index_col=[0]).loc['Add Sectors',user]}\\new_waste_sector.xlsx"
world[year].get_add_sectors_excel(new_sectors=waste_sectors, regions= [world[year].get_index('Region')[1]],path=path_waste_sector, item='Sector')

#WIOT.get_add_sectors_excel(new_sectors=waste_sectors, regions= [world[year].get_index('Region')[1]],path=path_waste_sector, item='Sector')
#%% Adding new commodities and activities (EMPTY)
for year in years:
    world[year].add_sectors(io=path_waste_sector, new_sectors= waste_sectors, regions= [world[year].get_index('Region')[1]], item='Sectors', inplace=True)

#WIOT.add_sectors(io=path_waste_sector, new_sectors= waste_sectors, regions= [world[year].get_index('Region')[1]], item='Sectors', inplace=True)
#%%
fileParam = f"{pd.read_excel(paths, index_col=[0]).loc['fileParam',user]}"
Weibull_params =  pd.read_excel(fileParam, "Weibull", index_col=[0,1])
sens = list(set(Weibull_params.index.get_level_values(1)))
region = 'EU27+UK'

for year in years:
    for s in ['Avg']:#sens:
        path_SG2 = f"{pd.read_excel(paths, index_col=[0]).loc['SG2',user]}\\SG2_{s}.xlsx"
        path_FD = f"{pd.read_excel(paths, index_col=[0]).loc['FD Total',user]}\\FD_total_{s}.xlsx"
        path_metrec = f"{pd.read_excel(paths, index_col=[0]).loc['metrec',user]}\\metrec_{s}_b2.xlsx"
        
        SG2 = pd.read_excel(path_SG2,sheet_name=None,index_col=[0,1,2],header= [0,1,2])
        FD = pd.read_excel(path_FD,sheet_name=None, index_col=[0,1,2], header= [0,1,2]) #check indici
        metrec = pd.read_excel(path_metrec,sheet_name=None, index_col=None, header= None)
        
        for y in SG2:
        #for y,matr in FD.items():
            #mat.columns = mat.index
            #SG2[y] = mat
            #FD[y] = matr
            
            scemario = f"{y} - {s}"
            world[year].clone_scenario(scenario='baseline',name=scemario)
            #WIOT.clone_scenario(scenario='baseline',name=scemario)
            
            z_new = world[year].matrices[scemario]['z']
            z_new.update(SG2[y])
            #z_new.loc[(region,'Sector',list(SG2[y].index)),(region,'Sector',list(SG2[y].columns))] = SG2[y].values
            
            # z_new = WIOT.matrices[scemario]['z']
            # z_new.update(SG2[y])
            
            
            Y_new = world[year].matrices[scemario]['Y']
            Y_new*=0
            Y_new.update(FD[y])
            #Y_new.loc[(region,'Sector',list(SwFD[y].index)),(region,'Sector','Gross fixed capital formation')] = SwFD[y].values
            
            # Y_new = WIOT.matrices[scemario]['Y']
            # Y_new*=0
            # Y_new.update(FD[y])
            
            X_new = world[year].matrices[scemario]['X']
            #X_new = WIOT.matrices[scemario]['X']
            #z_new2 = metrec[y - 1]/X_new[y - 1]  #il problema è qua
            
            # WIOT.update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
            # WIOT.reset_to_coefficients(scenario=scemario)
            world[year].update_scenarios(scenario=scemario, z=z_new, Y=Y_new)
            world[year].reset_to_coefficients(scenario=scemario)
            #WIOT.to_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\e. WIOT\\{year}", flows=True, coefficients=True)
            print(scemario)

# for yy in range(2011,2101):
#     scemario2 = f"scemario_{yy}"
#     WIOT.clone_scenario(scenario=scemario['{yy} - Avg'],name=scemario2)
    
#     z_new2 = WIOT.matrices[scemario2]['z']
#     z_new2 = metrec[yy -1]/X_new[scemario]
       

        
            
















    
#%%  Aggregated database with new sectors to txt
for year in years:
    world[year].to_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\e. WIOT\\{year}", flows=True, coefficients=True)

