import mario
import pandas as pd

user = "CF"
sN = slice(None)
years = range(2011,2012)

paths = 'Paths.xlsx'

#%%
world = {}

for year in years:
    world[year] = mario.parse_from_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\b. Aggregated & new sectors SUT\\{year}\\coefficients", table='SUT', mode="coefficients")
    
#%% From SUT to IOT
#z = pd.read_csv(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\b. Aggregated & new sectors SUT\\{year}\\coefficients\z.txt",index_col=[0,1,2], header=[0,1,2])

world[year] = mario.Database(
            Z = world[year].z,
            Y = world[year].Y,
            E = world[year].e,
            V = world[year].v,
            EY =world[year].EY,
            units = world[year].units,
            table='SUT',
            )
world[year].to_iot(method='B')
# zz = db.z #da scommentare quando farò vedere a mattia 

#%% creating template for waste sectors
waste_sectors = [
    "Refinery of Nd and Dy from permanent magnet" ,
    "Refinery of Si in PV panel",
    "Disassembler of permanent magnet",
    "Disassembler of PV panel",
    "Landifill",
    ]

waste_type = [
    "End of Life of fabricated metal products (28)",
    "End of Life of machinery and equipment n.e.c. (29)",
    "End of Life of office machinery and computers (30)",
    "End of Life of electrical machinery and apparatus n.e.c. (31)",
    "End of Life of radio, television and communication equipment and apparatus",
    "End of Life of medical, precision and optical instruments, watches and clocks (33)",
    "End of Life of motor and electric vehicles, trailers and semi-trailers (34)",
    "End of Life of wind turbine",
    "End of Life of e-bikes",
    "End of Life of product containing Co",
    "End of Life of lithium-ion batteries",
    "scraps of sector m.28",
    "scraps of sector m.29",
    "scraps of sector m.30",
    "scraps of sector m.31",
    "scraps of sector m.32",
    "scraps of sector m.33",
    "scraps of sector m.34",
    "scraps of wind turbine",
    "scraps of e-bikes",
    "scraps of products containing Co",
    "scraps of lithium-ion batteries",
    "Residue",
]
# world[year].get_add_sectors_excel(new_sectors = new_sectors['commodities'],regions= [world[year].get_index('Region')[0]],path=path_commodities, item='Commodity')
# world[year].get_add_sectors_excel(new_sectors = new_sectors['activities'],regions= [world[year].get_index('Region')[0]],path=path_activities, item='Activity')


#%% Getting excel templates to add new commodities
path_waste_sector = f"{pd.read_excel(paths, index_col=[0]).loc['Add Sectors',user]}\\new_waste_sector.xlsx"
path_waste_type = f"{pd.read_excel(paths, index_col=[0]).loc['Add Sectors',user]}\\new_waste_type.xlsx"
# world[year].get_add_sectors_excel(new_sectors = waste_sectors,regions= [world[year].get_index('Region')[0]],path=path_waste_sector)
# world[year].get_add_sectors_excel(new_sectors = waste_type, regions= [world[year].get_index('Region')[0]],path=path_waste_type)

#%% Adding new commodities and activities
for year in years:
    world[year].add_sectors(io=path_waste_sector, new_sectors= waste_sectors, regions= world[year].get_index('Region'), item='Sector', inplace=True)
    world[year].add_sectors(io=path_waste_type,  new_sectors= waste_type,  regions= [world[year].get_index('Region')[0]], item='Sector', inplace=True)

#%%