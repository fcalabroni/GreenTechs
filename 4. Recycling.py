#%%
import pandas as pd
import numpy as np

user = "MBV"
sN = slice(None)
years = 2011

paths = 'Paths.xlsx'

fileParam = f"{pd.read_excel(paths, index_col=[0]).loc['fileParam',user]}"
fileSolar = f"{pd.read_excel(paths, index_col=[0]).loc['fileSolar',user]}"
fileWind = f"{pd.read_excel(paths, index_col=[0]).loc['fileWind',user]}"

years = list(range(2000,2101))
n_years = list(range(0,years[-1]-years[0]+1))

Weibull_params =  pd.read_excel(fileParam, "Weibull", index_col=[0,1])
techs = list(set(Weibull_params.index.get_level_values(0)))
sens = list(set(Weibull_params.index.get_level_values(1)))

USD_to_EUR = pd.read_excel(fileParam,"USD to EURO", header=0, index_col=None)
#%% Importing EoL function for Wind and SolarPV

Weib = {}
SF = {}
for t in techs:
    SF[t] = {}
    Weib[t] = {}
    for s in sens:
        lambd = Weibull_params.loc[(t,s),'lambda']
        alpha = Weibull_params.loc[(t,s),'alpha']
        SF[t][s] = []
        for ny in n_years:
            step1 = ny/lambd
            step2 = step1**alpha 
            SF[t][s] += [np.exp(-step2)]

        Weib[t][s] = []            
        for ny in n_years:
            if ny!= n_years[-1]:
                Weib[t][s] += [SF[t][s][ny]-SF[t][s][ny+1]]
            else:
                Weib[t][s] += [SF[t][s][ny]]
                
#%% Importing Installed capacity and cost for green techs
WindOff_Capacity = pd.read_excel(fileWind, "Offshore", header=0, index_col=None)
WindOn_Capacity = pd.read_excel(fileWind, "Onshore", header=0, index_col=None)
SolarPV_Capacity = pd.read_excel(fileSolar, "SolarPV", header=0, index_col=None)
CAP = {
   'Onshore wind': WindOn_Capacity,
   'Offshore wind': WindOff_Capacity,
   'PV': SolarPV_Capacity,
   } #installed capacity in MW

WindOff_Cost = pd.read_excel(fileWind, "Cost_Offshore", header=0, index_col=None)
WindOn_Cost = pd.read_excel(fileWind, "Cost_Onshore", header=0, index_col=None)
SolarPV_Cost = pd.read_excel(fileSolar, "Cost_PV", header=0, index_col=None)
Cost = {
        'Onshore wind': WindOn_Cost,
        'Offshore wind': WindOff_Cost,
        'PV': SolarPV_Cost,
        } #cost in USD/kW

#%% Calculation EoL products

# Create DataFrames for EoL products and annual installed capacity
EoL = {}
AIC = {} #addition capacity
for t in techs:
    EoL[t] = {}
    AIC[t] = {}
    for s in sens:
        EoL[t][s] = pd.DataFrame(0, index=[0], columns=list(range(2000,2102)))
        AIC[t][s] = pd.DataFrame(0, index=[0], columns=years)

# Calculation loop
for t in techs:
    for s in sens:
        for i in years[1:]:
            for ii in range(0, (i+1-years[1:][0])):
                # Check if the key exists in the DataFrame index before accessing it
                AIC[t][s].loc[0, i] = ((CAP[t].loc[0, i]*1000*Cost[t].loc[0, i]*USD_to_EUR.loc[0, 'EURO/USD']) + EoL[t][s].loc[0, i]) - ((CAP[t].loc[0, i-1]*1000*Cost[t].loc[0, i]*USD_to_EUR.loc[0, 'EURO/USD'])+ EoL[t][s].loc[0, i-1]) 
                if AIC[t][s].loc[0,i] < 0:
                    AIC[t][s].loc[0,i] = 0
                # Check if the key exists in the DataFrame index before accessing it
                EoL[t][s].loc[0, i+1] = (AIC[t][s].loc[0, i-ii] * Weib[t][s][ii]) + EoL[t][s].loc[0, i+1]

#%% Create allocation matrix (S)
S = pd.read_excel(fileParam, "S", header = 0, index_col = 0 )

#%% Estimation of scraps trhough Collector and Disassembler
comp = ['Generator Onshore', 'Generator Offshore', 'Panel', 'Wires']

CR_tech = pd.read_excel(fileParam, "CR", header = 0 , index_col=None)
DR_tech = pd.read_excel(fileParam, "DR", header = 0 , index_col=None)

Inventory_comp = pd.read_excel(fileParam, "Inventory_comp", header = 0, index_col = 0)

CR = {
  'Onshore wind': CR_tech.loc[0,'WT'],
  'Offshore wind': CR_tech.loc[0,'WT'],
  'PV': CR_tech.loc[0,'PV'],
      }
DR = {
  'Onshore wind': DR_tech.loc[0,'WT'],
  'Offshore wind': DR_tech.loc[0,'WT'],
  'PV': DR_tech.loc[0,'PV'],
      }

Inv_comp = {
    'Generator Onshore': Inventory_comp.loc['%Generator Onshore', :],
    'Generator Offshore': Inventory_comp.loc['%Generator Offshore', :],
    'Panel': Inventory_comp.loc['%Panel', :],
    'Wires': Inventory_comp.loc['%Wires', :], 
    }
scraps = {}
for t in techs:
    scraps[t] = {}
    for c in comp:
        scraps[t][c] = {}
        for s in sens:
            scraps[t][c][s] = pd.DataFrame(0, index=[0], columns=years)

for t in techs:
    for c in comp:
        for s in sens:
            scraps[t][c][s] = EoL[t][s] * DR[t] * CR[t] * Inv_comp[c][t]

#%% Estimation of recycled materials
met = ['Nd', 'Dy', 'Cu', 'Si']

RE_comp = pd.read_excel(fileParam, "RE", header = 0, index_col = None)
RR_met = pd.read_excel(fileParam, "RR", header = 0, index_col = 0)

Inventory_met = pd.read_excel(fileParam, "Inventory_mat", header = 0, index_col = 0)

upgrade = ['Min', 'Avg', 'Max']
RE = {
  'Generator Onshore': RE_comp.loc[0,'Generator Onshore'],
  'Generator Offshore': RE_comp.loc[0,'Generator Offshore'],
  'Panel': RE_comp.loc[0,'Panel'],
  'Wires': RE_comp.loc[0,'Wires'],
      }

RR = {
  'Nd': RR_met.loc[:, 'Nd'], 
  'Dy': RR_met.loc[:, 'Dy'], 
  'Cu': RR_met.loc[:, 'Cu'], 
  'Si': RR_met.loc[:, 'Si'],
      }

Inv_met = {
   'Nd': Inventory_met.loc['%Nd', :], 
   'Dy': Inventory_met.loc['%Dy', :], 
   'Cu': Inventory_met.loc['%Cu', :], 
   'Si': Inventory_met.loc['%Si', :],
      }

met_recycled_specific = {}
for t in techs:
    met_recycled_specific[t] = {}
    for s in sens:
        met_recycled_specific[t][s] = {}
        for c in comp:
            met_recycled_specific[t][s][c] = {}
            for m in met:
                met_recycled_specific[t][s][c][m] = {}
                for u in upgrade:
                    met_recycled_specific[t][s][c][m][u] = {}

for t in techs:
    for c in comp:
        for s in sens:
            for m in  met:
                for u in upgrade:
                    met_recycled_specific[t][s][c][m][u] = scraps[t][c][s] * RE[c] * RR[m][u] *Inv_met[m][c]
 
            
#%% Estimation of recycled materials pt2
met_sum = {}  # Dizionario per la somma del rame

for m in met:
    met_sum[m] = {}  # Dizionario per ogni m
    for s in sens:
        met_sum[m][s] = {}  # Dizionario per ogni s
        for u in upgrade:
            met_sum[m][s][u] = pd.DataFrame(0, index=[0], columns=years) # Inizializza la somma a zero
            for t in techs:
                for c in comp:
                    met_sum[m][s][u] += met_recycled_specific[t][s][c][m][u]
                    
# for t in techs:
#     for c in comp:            
#         met_sum['Cu']['Avg']['Avg'] += met_recycled_specific[t]['Avg'][c]['Cu']['Avg'].sum()
#         met_sum['Cu']['Max']['Avg'] += met_recycled_specific[t]['Max'][c]['Cu']['Avg'].sum()
#         met_sum['Cu']['Min']['Avg'] += met_recycled_specific[t]['Min'][c]['Cu']['Avg'].sum()
#         met_sum['Cu']['Avg']['Min'] += met_recycled_specific[t]['Avg'][c]['Cu']['Min'].sum()
#         met_sum['Cu']['Max']['Min'] += met_recycled_specific[t]['Max'][c]['Cu']['Min'].sum()
#         met_sum['Cu']['Min']['Min'] += met_recycled_specific[t]['Min'][c]['Cu']['Min'].sum()
#         met_sum['Cu']['Avg']['Max'] += met_recycled_specific[t]['Avg'][c]['Cu']['Max'].sum()
#         met_sum['Cu']['Max']['Max'] += met_recycled_specific[t]['Max'][c]['Cu']['Max'].sum()
#         met_sum['Cu']['Min']['Max'] += met_recycled_specific[t]['Min'][c]['Cu']['Max'].sum()

#         met_sum['Si']['Avg']['Avg'] += met_recycled_specific[t]['Avg'][c]['Si']['Avg'].sum()
#         met_sum['Si']['Max']['Avg'] += met_recycled_specific[t]['Max'][c]['Si']['Avg'].sum()
#         met_sum['Si']['Min']['Avg'] += met_recycled_specific[t]['Min'][c]['Si']['Avg'].sum()
#         met_sum['Si']['Avg']['Min'] += met_recycled_specific[t]['Avg'][c]['Si']['Min'].sum()
#         met_sum['Si']['Max']['Min'] += met_recycled_specific[t]['Max'][c]['Si']['Min'].sum()
#         met_sum['Si']['Min']['Min'] += met_recycled_specific[t]['Min'][c]['Si']['Min'].sum()
#         met_sum['Si']['Avg']['Max'] += met_recycled_specific[t]['Avg'][c]['Si']['Max'].sum()
#         met_sum['Si']['Max']['Max'] += met_recycled_specific[t]['Max'][c]['Si']['Max'].sum()
#         met_sum['Si']['Min']['Max'] += met_recycled_specific[t]['Min'][c]['Si']['Max'].sum()

#         met_sum['Nd']['Avg']['Avg'] += met_recycled_specific[t]['Avg'][c]['Nd']['Avg'].sum()
#         met_sum['Nd']['Max']['Avg'] += met_recycled_specific[t]['Max'][c]['Nd']['Avg'].sum()
#         met_sum['Nd']['Min']['Avg'] += met_recycled_specific[t]['Min'][c]['Nd']['Avg'].sum()
#         met_sum['Nd']['Avg']['Min'] += met_recycled_specific[t]['Avg'][c]['Nd']['Min'].sum()
#         met_sum['Nd']['Max']['Min'] += met_recycled_specific[t]['Max'][c]['Nd']['Min'].sum()
#         met_sum['Nd']['Min']['Min'] += met_recycled_specific[t]['Min'][c]['Nd']['Min'].sum()
#         met_sum['Nd']['Avg']['Max'] += met_recycled_specific[t]['Avg'][c]['Nd']['Max'].sum()
#         met_sum['Nd']['Max']['Max'] += met_recycled_specific[t]['Max'][c]['Nd']['Max'].sum()
#         met_sum['Nd']['Min']['Max'] += met_recycled_specific[t]['Min'][c]['Nd']['Max'].sum()

#         met_sum['Dy']['Avg']['Avg'] += met_recycled_specific[t]['Avg'][c]['Dy']['Avg'].sum()
#         met_sum['Dy']['Max']['Avg'] += met_recycled_specific[t]['Max'][c]['Dy']['Avg'].sum()
#         met_sum['Dy']['Min']['Avg'] += met_recycled_specific[t]['Min'][c]['Dy']['Avg'].sum()
#         met_sum['Dy']['Avg']['Min'] += met_recycled_specific[t]['Avg'][c]['Dy']['Min'].sum()
#         met_sum['Dy']['Max']['Min'] += met_recycled_specific[t]['Max'][c]['Dy']['Min'].sum()
#         met_sum['Dy']['Min']['Min'] += met_recycled_specific[t]['Min'][c]['Dy']['Min'].sum()
#         met_sum['Dy']['Avg']['Max'] += met_recycled_specific[t]['Avg'][c]['Dy']['Max'].sum()
#         met_sum['Dy']['Max']['Max'] += met_recycled_specific[t]['Max'][c]['Dy']['Max'].sum()
#         met_sum['Dy']['Min']['Max'] += met_recycled_specific[t]['Min'][c]['Dy']['Max'].sum()

# met_sum = {}  # Dizionario per la somma del rame

# # Inizializza la struttura del dizionario
# for m in met:
#     met_sum[m] = {}  # Dizionario per ogni m
#     for s in sens:
#         met_sum[m][s] = {}  # Dizionario per ogni s
#         for u in upgrade:
#             met_sum[m][s][u] = pd.DataFrame(0, index=[0], columns=years)  # Inizializza la somma a zero

# # Mapping tra i metalli e le colonne di met_recycled_specific
# metal_columns = {'Cu': 'Cu', 'Si': 'Si', 'Nd': 'Nd', 'Dy': 'Dy'}

# for m in met:
#     for s in sens:
#         for u in upgrade:
#             for t in techs:
#                 for c in comp:
#                     # Somma il metallo corrente per ogni tecnologia, componente, sens e upgrade
#                     met_sum[m][s][u] += met_recycled_specific[t][u][c][metal_columns[m]][s].sum()

#%% Estimation of residues
residues = ['z_dis_WT','z_dis_PV','z_ref_OnGen','z_ref_OffGen','z_ref_Panel', 'z_ref_Wires']

res = {}
for r in residues:
    res[r] = {}
    for s in sens: 
        res[r][s] = pd.DataFrame(0, index=[0], columns=list(range(2000,2102)))

for s in sens:
    res['z_dis_WT'][s] = (1 - (CR_tech.loc[0,'WT']*DR_tech.loc[0,'WT']))* (EoL['Onshore wind'][s] +EoL['Offshore wind'][s]) 
    res['z_dis_PV'][s] = (1 - (CR_tech.loc[0,'PV']*DR_tech.loc[0,'PV']))* (EoL['PV'][s]) # va in residues il 23.5% dei PV in EoL perché consideri ciò che esce dal disassembler (quindi consideri sia CR che DR (CR*DR = 76.5%))
    res['z_ref_OnGen'][s] = (1 - RE_comp.loc[0, 'Generator Onshore'])* scraps['Onshore wind']['Generator Onshore'][s]
    res['z_ref_OffGen'][s] = (1 - RE_comp.loc[0, 'Generator Offshore'])* scraps['Offshore wind']['Generator Offshore'][s]
    res['z_ref_Panel'][s] = (1 - RE_comp.loc[0, 'Panel'])* scraps['PV']['Panel'][s]
    res['z_ref_Wires'][s] = (1 - RE_comp.loc[0, 'Wires'])* (scraps['PV']['Wires'][s] + scraps['Onshore wind']['Wires'][s] + scraps['Offshore wind']['Wires'][s])

#%% Creation of W2 and wFD

waste_sectors = [
    'Disassembler of Wind Turbines',
    'Disassembler of PV panels',
    'Refinery of Generators of Onshore Wind Turbines' ,
    'Refinery of Generators of Offshore Wind Turbines' ,
    'Refinery of Silicon layer in PV panel',
    'Refinery of Cu in wires of WT and PV',
    'Landifill',
    ]

waste_type = [
    'EoL of Offshore WT',
    'EoL of Onshore WT',
    'EoL of PV',
    'Scraps of generator of Offshore WT',
    'Scraps of generator of Onshore WT',
    'Scraps of wires',
    'Scraps of Silicon layer',
    'Residues',
    ]

W2 = {}
for s in sens:
    W2[s] = {}
    for i in years:
        W2[s][i] = pd.DataFrame(0, index= waste_type, columns = waste_sectors )

for s in sens:
    for i in years:
        W2[s][i].loc['Scraps of generator of Offshore WT','Disassembler of Wind Turbines'] = scraps['Offshore wind']['Generator Offshore'][s].loc[0, i]
        W2[s][i].loc['Scraps of generator of Onshore WT','Disassembler of Wind Turbines'] = scraps['Onshore wind']['Generator Onshore'][s].loc[0, i]
        W2[s][i].loc['Scraps of wires','Disassembler of Wind Turbines'] = scraps['Offshore wind']['Wires'][s].loc[0, i] + scraps['Onshore wind']['Wires'][s].loc[0, i]
        W2[s][i].loc['Residues','Disassembler of Wind Turbines'] = res['z_dis_WT'][s].loc[0, i]

        W2[s][i].loc['Scraps of wires','Disassembler of PV panels'] = scraps['PV']['Wires'][s].loc[0, i]
        W2[s][i].loc['Scraps of Silicon layer','Disassembler of PV panels'] = scraps['PV']['Panel'][s].loc[0, i]
        W2[s][i].loc['Residues','Disassembler of PV panels'] = res['z_dis_PV'][s].loc[0, i]

        W2[s][i].loc['Residues','Refinery of Generators of Offshore Wind Turbines'] = res['z_ref_OffGen'][s].loc[0, i]
        W2[s][i].loc['Residues','Refinery of Generators of Onshore Wind Turbines'] = res['z_ref_OnGen'][s].loc[0, i]
        W2[s][i].loc['Residues','Refinery of Silicon layer in PV panel'] = res['z_ref_Panel'][s].loc[0, i]
        W2[s][i].loc['Residues','Refinery of Cu in wires of WT and PV'] = res['z_ref_Wires'][s].loc[0, i]


wFD = {}
for s in sens:
    wFD[s] = {}
    for i in years:
        wFD[s][i] = pd.DataFrame(0, index= waste_type, columns = ['FD'] )

for s in sens:
    for i in years:
        wFD[s][i].loc['EoL of Offshore WT','FD'] = EoL['Offshore wind'][s].loc[0, i]
        wFD[s][i].loc['EoL of Onshore WT','FD'] = EoL['Onshore wind'][s].loc[0, i]
        wFD[s][i].loc['EoL of PV','FD'] = EoL['PV'][s].loc[0, i] 

#%% Calculating SW2 and SwFD

SW2 = {}
for s in sens:
    SW2[s] = {}
    for i in years:
        SW2[s][i] = pd.DataFrame(0, index= waste_sectors, columns = waste_sectors )

for s in sens:
    for i in years:
        SW2[s][i] = S @ W2[s][i]


SwFD = {}
for s in sens:
    SwFD[s] = {}
    for i in years:
        SwFD[s][i] = pd.DataFrame(0, index= waste_sectors, columns = ['FD'] )
        
        
for s in sens:
    for i in years:
        SwFD[s][i] = S @ wFD[s][i]
        
#%% Calculating coefficient matrix SG2 = SW2 * (Xw)^-1

SG2 = {}
for s in sens:
    SG2[s]= {}
    for i in years:
        SG2[s][i] = pd.DataFrame(0, index= waste_sectors, columns = waste_sectors)
        
Xw = {}
for s in sens:
    Xw[s] = {}
    for i in years:
        Xw[s][i] = pd.DataFrame(0, index= waste_sectors, columns = ['Xw'] )
        
for s in sens:
    for i in years:
        Xw[s][i] = SW2[s][i].sum(axis = 1) + SwFD[s][i].loc[:,'FD']

for s in sens:
    for i in range(2010,2101):
        SG2[s][i] = SW2[s][i] @ np.linalg.inv(np.diag(Xw[s][i]))
        
#%% Export Data


for s in sens:
    with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['SwFD',user]}\\SwFD_{s}.xlsx") as writer:
        for key, df in SwFD[s].items():
            sheet_name = f'{key}'
            df.to_excel(writer, sheet_name=sheet_name, index=True)


    with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['SW2',user]}\\SW2_{s}.xlsx") as writer:
        for key, df in SW2[s].items():
            sheet_name = f'{key}'
            df.to_excel(writer, sheet_name=sheet_name, index=True)
            
    with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['SG2',user]}\\SG2_{s}.xlsx") as writer:
        for key, df in SG2[s].items():
            sheet_name = f'{key}'
            df.to_excel(writer, sheet_name=sheet_name, index= True)





