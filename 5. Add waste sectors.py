import mario
import pandas as pd

user = "LR"
sN = slice(None)
years = range(2011,2012)

paths = 'Paths.xlsx'

#%% Parse and SUT to IOT

world = {}

for year in years:
    world[year] = mario.parse_from_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\d. Baseline\\{year}\\flows", table='SUT', mode="coefficients")
    world[year].to_iot(method='B')

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
# world[year].get_add_sectors_excel(new_sectors = waste_sectors, regions= [world[year].get_index('Region')[1]],path=path_waste_sector, item='Sector')

#%% Adding new commodities and activities
for year in years:
    world[year].add_sectors(io=path_waste_sector, new_sectors= waste_sectors, regions= [world[year].get_index('Region')[1]], item='Sectors', inplace=True)
    
#%%  Aggregated database with new sectors to txt

for year in years:
    world[year].to_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\e. WIOT\\{year}", flows=True, coefficients=True)

