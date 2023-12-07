import mario
import pandas as pd

user = "CF"
sN = slice(None)
years = range(2011,2012)

paths = 'Paths.xlsx'

#%% Parse aggregated database from txt
world = {}
for year in years:
    world[year] = mario.parse_from_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\a. Aggregated_SUT\\{year}\\flows", table='SUT', mode="flows")

#%% Define new commodities
new_sectors = {
    'commodities': [
        'Photovoltaic plants',
        'Onshore wind plants',
        'Offshore wind plants',
        'Neodymium',
        'Dysprosium',
        'Raw silicon',
        ],
    
    'activities': [
        'Production of photovoltaic plants',
        'Production of onshore wind plants',
        'Production of offshore wind plants'
        ]
    }

#%% Getting excel templates to add new commodities
path_commodities = f"{pd.read_excel(paths, index_col=[0]).loc['Add Sectors',user]}\\new_commodities.xlsx"
path_activities  = f"{pd.read_excel(paths, index_col=[0]).loc['Add Sectors',user]}\\new_activities.xlsx"
# world[year].get_add_sectors_excel(new_sectors = new_sectors['commodities'],regions= [world[year].get_index('Region')[0]],path=path_commodities, item='Commodity')
# world[year].get_add_sectors_excel(new_sectors = new_sectors['activities'],regions= [world[year].get_index('Region')[0]],path=path_activities, item='Activity')

#%% Adding new commodities and activities
for year in years:
    world[year].add_sectors(io=path_commodities, new_sectors= new_sectors['commodities'], regions= world[year].get_index('Region'), item= 'Commodity', inplace=True)
    world[year].add_sectors(io=path_activities,  new_sectors= new_sectors['activities'],  regions= [world[year].get_index('Region')[0]], item= 'Activity',  inplace=True)

#%%
f = {}
for year in years:
    f[year] = world[year].f.loc["CO2 - combustion - air",(slice(None),slice(None),world[year].search('Commodity','Electricity'))]

#%% Aggregated database with new sectors to txt
for year in years:
    world[year].to_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\b. Aggregated & new sectors SUT\\{year}", flows=True, coefficients=True)
   
#%%