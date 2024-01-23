import mario 
import pandas as pd

user = "MBV"
sN = slice(None)
years = 2011

paths = 'Paths.xlsx'

#%% Importing databases from EXIOBASE  
world_eco_path  = pd.read_excel(paths, index_col=[0]).loc['EXIOBASE SUT',user]+f"/MRSUT_{years}.zip"
world_hybrid_path  = pd.read_excel(paths, index_col=[0]).loc['EXIOBASE Hybrid',user]+f"/Hybrid_{years}.zip"

world_eco = mario.parse_exiobase(path=world_eco_path, table='SUT', unit='Monetary')
world_hybrid = mario.hybrid_sut_exiobase(path=world_hybrid_path, extension= ['All'])

#%% Aggregating exiobase as other models
path_aggr_eco  = r"Aggregations\Aggregation_raw_SUT.xlsx"
path_aggr_hybrid  = r"Aggregations\Aggregation_hybrid.xlsx"

world_eco.aggregate(path_aggr_eco, levels=["Region"])
world_hybrid.aggregate(path_aggr_hybrid, levels=["Region"])

#%% Calculation of Z and z for both databases
z_hybrid = world_hybrid.z
z_eco = world_eco.z

Z_hybrid = world_hybrid.Z
Z_eco = world_eco.Z

#%%Export Database (ci pensiamo poi se ci serve)

#%%Extraction data useful for activities analyzed
#Extraction of the conusmption of 'Chemicals nec' (p24.d) of the activities selected
# Define the activities from where you want to extract
activities_selected = ['Manufacture of glass and glass products',
               'Manufacture of ceramic goods',
               'Manufacture of basic iron and steel and of ferro-alloys and first products thereof',
               'Other non-ferrous metal production',
               'Manufacture of fabricated metal products, except machinery and equipment (28)',
               'Manufacture of machinery and equipment n.e.c. (29)',
               'Manufacture of office machinery and computers (30)',
               'Manufacture of electrical machinery and apparatus n.e.c. (31)',
               'Manufacture of radio, television and communication equipment and apparatus (32)',
               'Manufacture of medical, precision and optical instruments, watches and clocks (33)',
               'Manufacture of motor vehicles, trailers and semi-trailers (34)',
               'Plastics, basic',
               'Computer and related activities (72)'
               ]

country = ['EU27+UK','China','USA','RoW']

# Create a dictionaries to store the DataFrames
p24d_z_eco = {}
p24d_z_hybrid = {}
p24d_Z_eco = {}
p24d_Z_hybrid = {}

# Loop through activities and extract data
for activity in activities_selected:
    p24d_z_eco[activity] = pd.DataFrame(index=country, columns=country, dtype=float)
    p24d_z_hybrid[activity] = pd.DataFrame(index=country, columns=country, dtype=float)
    p24d_Z_eco[activity] = pd.DataFrame(index=country, columns=country, dtype=float)
    p24d_Z_hybrid[activity] = pd.DataFrame(index=country, columns=country, dtype=float)
    for i in country:
        for j in country:
            p24d_z_eco[activity].loc[i, j] = z_eco.loc[(i,'Commodity' ,'Chemicals nec'), (j,'Activity' ,activity)]
            p24d_z_hybrid[activity].loc[i, j] = z_hybrid.loc[(i,'Commodity' ,'Chemicals nec'), (j,'Activity' ,activity)]
            p24d_Z_eco[activity].loc[i, j] = Z_eco.loc[(i,'Commodity' ,'Chemicals nec'), (j,'Activity' ,activity)]
            p24d_Z_hybrid[activity].loc[i, j] = Z_hybrid.loc[(i,'Commodity' ,'Chemicals nec'), (j,'Activity' ,activity)]

#%% Export data 

with pd.ExcelWriter('1Hybrid_z.xlsx') as writer:
    for key, df in p24d_z_hybrid.items():
        sheet_name = f'{key[:25]}'  # Shorten the name to fit within the limit
        df.to_excel(writer, sheet_name=sheet_name, index=False)

with pd.ExcelWriter('2Hybrid_Z.xlsx') as writer:
    for key, df in p24d_Z_hybrid.items():
        sheet_name = f'{key[:25]}'  # Shorten the name to fit within the limit
        df.to_excel(writer, sheet_name=sheet_name, index=False)

with pd.ExcelWriter('3Economic_z.xlsx') as writer:
    for key, df in p24d_z_eco.items():
        sheet_name = f'{key[:25]}'  # Shorten the name to fit within the limit
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        
with pd.ExcelWriter('4Economic_Z.xlsx') as writer:
    for key, df in p24d_Z_eco.items():
        sheet_name = f'{key[:25]}'  # Shorten the name to fit within the limit
        df.to_excel(writer, sheet_name=sheet_name, index=False)