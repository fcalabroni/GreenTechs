#%%
import pandas as pd
import numpy as np

user = "MBV"
sN = slice(None)

paths = 'Paths.xlsx'

fileParam = f"{pd.read_excel(paths, index_col=[0]).loc['fileParam',user]}"
fileSolar = f"{pd.read_excel(paths, index_col=[0]).loc['fileSolar',user]}"
fileWind = f"{pd.read_excel(paths, index_col=[0]).loc['fileWind',user]}"

years = list(range(2000,2101))
n_years = list(range(0,years[-1]-years[0]+1))

Weibull_params =  pd.read_excel(fileParam, "Weibull", index_col=[0,1])
techs = list(set(Weibull_params.index.get_level_values(0)))
sens = list(set(Weibull_params.index.get_level_values(1)))

USD_to_EUR = pd.read_excel(fileParam,"USD to EURO", header=0, index_col=0)
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
WindOff_Capacity = pd.read_excel(fileWind, "Offshore", header=0, index_col=0)
WindOn_Capacity = pd.read_excel(fileWind, "Onshore", header=0, index_col=0)
SolarPV_Capacity = pd.read_excel(fileSolar, "SolarPV", header=0, index_col=0)
region = list(WindOff_Capacity.index.get_level_values(0))

CAP = {
   'Onshore wind plants': WindOn_Capacity,
   'Offshore wind plants': WindOff_Capacity,
   'Photovoltaic plants': SolarPV_Capacity,
   } #installed capacity in MW

WindOff_Cost = pd.read_excel(fileWind, "Cost_Offshore", header=0, index_col=0)
WindOn_Cost = pd.read_excel(fileWind, "Cost_Onshore", header=0, index_col=0)
SolarPV_Cost = pd.read_excel(fileSolar, "Cost_PV", header=0, index_col=0)
Cost = {
        'Onshore wind plants': WindOn_Cost,
        'Offshore wind plants': WindOff_Cost,
        'Photovoltaic plants': SolarPV_Cost,
        } #cost in MUSD/kW

#%% Calculation EoL products
# Create DataFrames for EoL products and annual installed capacity
EoL = {}
AIC = {} #addition capacity
for t in techs:
    EoL[t] = {}
    AIC[t] = {}
    for s in sens:
        EoL[t][s] = pd.DataFrame(0, index=region, columns=list(range(2000,2102)))
        AIC[t][s] = pd.DataFrame(0, index=region, columns=years)

# Calculation loop
for t in techs:
    for s in sens:
        for i in years[1:]:
            for ii in range(0, (i+1-years[1:][0])):
                # Check if the key exists in the DataFrame index before accessing it
                AIC[t][s].loc[:, i] = ((CAP[t].loc[:, i]*1000*Cost[t].loc[:, i]*USD_to_EUR.loc['EURO/USD', i]) + EoL[t][s].loc[:, i]) - ((CAP[t].loc[:, i-1]*1000*Cost[t].loc[:, i]*USD_to_EUR.loc['EURO/USD', i]))#+ EoL[t][s].loc[0, i-1]) 
                for r in region:
                    if AIC[t][s].loc[r,i] < 0:
                        AIC[t][s].loc[r,i] = 0
                # Check if the key exists in the DataFrame index before accessing it
                EoL[t][s].loc[:, i+1] = (AIC[t][s].loc[:, i-ii] * Weib[t][s][ii]) + EoL[t][s].loc[:, i+1]


#%% Estimation of scraps trhough Collector and Disassembler
comp = ['Generator Onshore', 'Generator Offshore', 'Panel', 'Wires']

CR_tech = pd.read_excel(fileParam, "CR", header = 0 , index_col=None)
DR_tech = pd.read_excel(fileParam, "DR", header = 0 , index_col=None)

Inventory_comp = pd.read_excel(fileParam, "Inventory_comp", header = 0, index_col = 0)
#comp = list(Inventory_comp.get_level_values(0))
CR = {
  'Onshore wind plants': CR_tech.loc[0,'WT'],
  'Offshore wind plants': CR_tech.loc[0,'WT'],
  'Photovoltaic plants': CR_tech.loc[0,'PV'],
      }
DR = {
  'Onshore wind plants': DR_tech.loc[0,'WT'],
  'Offshore wind plants': DR_tech.loc[0,'WT'],
  'Photovoltaic plants': DR_tech.loc[0,'PV'],
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
            scraps[t][c][s] = EoL[t][s] * DR[t]  * Inv_comp[c][t]

#%% Estimation of recycled materials
met = ['Neodymium', 'Dysprosium', 'Copper', 'Raw silicon']

RE_comp = pd.read_excel(fileParam, "RE", header = 0, index_col = None)
RR_met = pd.read_excel(fileParam, "RR", header = [0,1], index_col = 0)

#met = list((RR_met.columns.get_level_values(1)))
Inventory_met = pd.read_excel(fileParam, "Inventory_mat", header = 0, index_col = 0)

upgrade = ['hist', 'target', 'full']
RE = {
  'Generator Onshore': RE_comp.loc[0,'Generator Onshore'],
  'Generator Offshore': RE_comp.loc[0,'Generator Offshore'],
  'Panel': RE_comp.loc[0,'Panel'],
  'Wires': RE_comp.loc[0,'Wires'],
      }

RR = {}
for u in upgrade:
    RR[u] = {}
    RR[u] = pd.DataFrame(0,index = met, columns = years)
    for i in years:
        RR[u].loc[:,i] = RR_met.loc[i,(u,met)].values

Inv_met = {
   'Neodymium': Inventory_met.loc['%Nd', :], 
   'Dysprosium': Inventory_met.loc['%Dy', :], 
   'Copper': Inventory_met.loc['%Cu', :], 
   'Raw silicon': Inventory_met.loc['%Si', :],
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
                    met_recycled_specific[t][s][c][m][u] = scraps[t][c][s] * RE[c] * RR[u].loc[m,:] *Inv_met[m][c]
 
            
#%% Estimation of recycled materials pt2
met_sum = {}  # Dizionario per la somma del materiale

for m in met:
    met_sum[m] = {}  # Dizionario per ogni m
    for s in sens:
        met_sum[m][s] = {}  # Dizionario per ogni s
        for u in upgrade:
            met_sum[m][s][u] = pd.DataFrame(0, index=region, columns=years) # Inizializza la somma a zero
            for t in techs:
                for c in comp:
                    met_sum[m][s][u] += met_recycled_specific[t][s][c][m][u]
                    
#%% Estimation of residues
residues = ['z_dis_WT','z_dis_PV','z_ref_OnGen','z_ref_OffGen','z_ref_Panel', 'z_ref_Wires']

res = {}
for r in residues:
    res[r] = {}
    for s in sens: 
        res[r][s] = pd.DataFrame(0, index=[0], columns=list(range(2000,2102)))

for s in sens:
    res['z_dis_WT'][s] = (1 - (CR_tech.loc[0,'WT']*DR_tech.loc[0,'WT']))* (EoL['Onshore wind plants'][s] +EoL['Offshore wind plants'][s]) 
    res['z_dis_PV'][s] = (1 - (CR_tech.loc[0,'PV']*DR_tech.loc[0,'PV']))* (EoL['Photovoltaic plants'][s]) # va in residues il 23.5% dei PV in EoL perché consideri ciò che esce dal disassembler (quindi consideri sia CR che DR (CR*DR = 76.5%))
    res['z_ref_OnGen'][s] = (1 - RE_comp.loc[0, 'Generator Onshore'])* scraps['Onshore wind plants']['Generator Onshore'][s]
    res['z_ref_OffGen'][s] = (1 - RE_comp.loc[0, 'Generator Offshore'])* scraps['Offshore wind plants']['Generator Offshore'][s]
    res['z_ref_Panel'][s] = (1 - RE_comp.loc[0, 'Panel'])* scraps['Photovoltaic plants']['Panel'][s]
    res['z_ref_Wires'][s] = (1 - RE_comp.loc[0, 'Wires'])* (scraps['Photovoltaic plants']['Wires'][s] + scraps['Onshore wind plants']['Wires'][s] + scraps['Offshore wind plants']['Wires'][s])

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
        W2[s][i] = pd.DataFrame(0, index= 4*waste_type, columns = 4*waste_sectors )
        W2[s][i].index = pd.MultiIndex.from_arrays([['EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','China', 'China', 'China', 'China','China','China','China','China','USA', 'USA', 'USA', 'USA','USA', 'USA', 'USA', 'USA','RoW', 'RoW', 'RoW', 'RoW','RoW', 'RoW', 'RoW', 'RoW'],['Sector'] * len(waste_type)*4, 4*waste_type], names=['Region', 'Level', 'Item'])
        W2[s][i].columns = pd.MultiIndex.from_arrays([['EU27+UK', 'EU27+UK', 'EU27+UK','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','China', 'China', 'China', 'China','China','China','China','USA', 'USA', 'USA', 'USA','USA', 'USA', 'USA','RoW', 'RoW', 'RoW', 'RoW','RoW', 'RoW', 'RoW'], ['Sector'] * len(waste_sectors)*4, 4*waste_sectors], names=['Region', 'Level', 'Item'])
        

for s in sens:
    for i in years:
        for r in region:
            W2[s][i].loc[(r,'Sector','Scraps of generator of Offshore WT'),(r,'Sector','Disassembler of Wind Turbines')] = scraps['Offshore wind plants']['Generator Offshore'][s].loc[r, i]
            W2[s][i].loc[(r,'Sector','Scraps of generator of Onshore WT'),(r,'Sector','Disassembler of Wind Turbines')] = scraps['Onshore wind plants']['Generator Onshore'][s].loc[r, i]
            W2[s][i].loc[(r,'Sector','Scraps of wires'),(r,'Sector','Disassembler of Wind Turbines')] = scraps['Offshore wind plants']['Wires'][s].loc[r, i] + scraps['Onshore wind plants']['Wires'][s].loc[r, i]
            W2[s][i].loc[(r,'Sector','Residues'),(r,'Sector','Disassembler of Wind Turbines')] = res['z_dis_WT'][s].loc[r, i]
    
            W2[s][i].loc[(r,'Sector','Scraps of wires'),(r,'Sector','Disassembler of PV panels')] = scraps['Photovoltaic plants']['Wires'][s].loc[r, i]
            W2[s][i].loc[(r,'Sector','Scraps of Silicon layer'),(r,'Sector','Disassembler of PV panels')] = scraps['Photovoltaic plants']['Panel'][s].loc[r, i]
            W2[s][i].loc[(r,'Sector','Residues'),(r,'Sector','Disassembler of PV panels')] = res['z_dis_PV'][s].loc[r, i]
    
            W2[s][i].loc[(r,'Sector','Residues'),(r,'Sector','Refinery of Generators of Offshore Wind Turbines')] = res['z_ref_OffGen'][s].loc[r, i]
            W2[s][i].loc[(r,'Sector','Residues'),(r,'Sector','Refinery of Generators of Onshore Wind Turbines')] = res['z_ref_OnGen'][s].loc[r, i]
            W2[s][i].loc[(r,'Sector','Residues'),(r,'Sector','Refinery of Silicon layer in PV panel')] = res['z_ref_Panel'][s].loc[r, i]
            W2[s][i].loc[(r,'Sector','Residues'),(r,'Sector','Refinery of Cu in wires of WT and PV')] = res['z_ref_Wires'][s].loc[r, i]
    
#region_FD = ['EU27+UK','USA','RoW','China'] 
wFD = {}
for s in sens:
    wFD[s] = {}
    for i in years:
        wFD[s][i] = pd.DataFrame(0, index= waste_type*4, columns = region )
        wFD[s][i].index = W2[s][i].index
        
for s in sens:
    for i in years:
        for r in region:
            wFD[s][i].loc[(r,'Sector','EoL of Offshore WT'),r] = EoL['Offshore wind plants'][s].loc[r, i]
            wFD[s][i].loc[(r,'Sector','EoL of Onshore WT'),r] = EoL['Onshore wind plants'][s].loc[r, i]
            wFD[s][i].loc[(r,'Sector','EoL of PV'),r] = EoL['Photovoltaic plants'][s].loc[r, i] 

#%% Create allocation matrix (S)
S_matrix = pd.read_excel(fileParam, "S", header = 0, index_col = 0 )
S = pd.DataFrame(0,index = W2[s][i].columns , columns = W2[s][i].index )
for r in region:
    S.loc[(r,'Sector',waste_sectors),(r,'Sector',waste_type)] = S_matrix.values

#%% Calculating SW2 and SwFD
SW2 = {}
for s in sens:
    SW2[s] = {}
    for i in years:
        SW2[s][i] = pd.DataFrame(0, index= W2[s][i].columns, columns = W2[s][i].columns )

for s in sens:
    for i in years:
        SW2[s][i] = S @ W2[s][i] 


SwFD = {}
for s in sens:
    SwFD[s] = {}
    for i in years:
        SwFD[s][i] = pd.DataFrame(0, index= waste_sectors*4, columns = region )
        SwFD[s][i].index = W2[s][i].columns

for s in sens:
    for i in years:
        SwFD[s][i]= S @ wFD[s][i]


           
#%% Calculating coefficient matrix SG2 = SW2 * (Xw)^-1
                                           
SG2 = {}
for s in sens:
    SG2[s]= {}
    for i in range(2011,2101):
        SG2[s][i] = pd.DataFrame(0, index= W2[s][i].columns, columns = W2[s][i].columns)
        
Xw = {}
for s in sens:
    Xw[s] = {}
    for i in range(2011,2101):
        Xw[s][i] = pd.DataFrame(0, index= W2[s][i].columns, columns = ['Xw'] )
        
for s in sens:
    for i in range(2011,2101):
        Xw[s][i] = SW2[s][i].sum(axis = 1) + SwFD[s][i].sum(axis = 1)

for s in sens:
    for i in range(2011,2101):
        #SG2[s][i] = SW2[s][i] @ np.linalg.inv(np.diag(Xw[s][i]))
        reg_term = 1e-9  # Puoi regolare questo valore
        SG2[s][i] = SW2[s][i] @ np.linalg.inv(np.diag(Xw[s][i]) + reg_term * np.eye(len(Xw[s][i])))
        SG2[s][i].columns= W2[s][i].columns
# det = np.linalg.det(np.diag(Xw[s][i]))
# if np.isclose(det, 0.0):
#     print("La matrice è singolare.")
        
# for s in sens:
#     for i in range(2011,2101):        
#         SG2[s][i].index =  pd.MultiIndex.from_arrays([['EU27+UK'] * len(waste_sectors), ['Sector'] * len(waste_sectors), waste_sectors], names=['Region', 'Level', 'Item'])   
#         SG2[s][i].columns = pd.MultiIndex.from_arrays([['EU27+UK'] * len(waste_sectors), ['Sector'] * len(waste_sectors), waste_sectors])

#%% Creating Allocation Matrix a 
# ref = [
#     'Refinery of Generators of Onshore Wind Turbines' ,
#     'Refinery of Generators of Offshore Wind Turbines' ,
#     'Refinery of Silicon layer in PV panel',
#     'Refinery of Cu in wires of WT and PV',
# ]

path_Act = f"{pd.read_excel(paths, index_col=[0]).loc['Act',user]}\\Act coeff.xlsx"
a_base = pd.read_excel(path_Act,sheet_name='Allocation matrix base', index_col=[0,1,2], header=[0,1,2])  #far cambiare per baseline e per act
a_act = pd.read_excel(path_Act,sheet_name='Allocation matrix act', index_col=[0,1,2], header=[0,1,2,3])  #far cambiare per baseline e per act
ref = list((a_act.columns.get_level_values(3)))
ref = ref[:4]
a_act.index = pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 4 * len(met), met*4])
a_base.index = pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 4 * len(met), met*4])
#a.index = pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 4 * len(met), met*4])
#a.columns = pd.MultiIndex.from_arrays([['EU27+UK'] * len(ref), ['Sector'] * len(ref), ref])
     
#%% Calculating coefficient matrix A2 for both Baseline and Act scenario 

coeff_rec = {}
for u in upgrade:
    coeff_rec[u] = {}
    for i in years:
        coeff_rec[u][i] = pd.DataFrame(0, index = a_base.index , columns = 4*comp)
    
for u in upgrade:
    for i in years:
        for c in comp:
            for m in met:
                for r in region:
                    #A2[s][u][i].loc[m][c] = RE[c] * RR[m][u] *Inv_met[m][c]
                    coeff_rec[u][i].loc[(r,'Sector',m),c] = - RE[c] * RR[u].loc[m,i] *Inv_met[m][c]
                    
for u in upgrade:
    for i in years:
        coeff_rec[u][i].columns = a_base.columns

A2_all = {}
for s in sens:
    A2_all[s] = {}
    for u in upgrade:
        A2_all[s][u] = {}
        for i in range(2011,2101):
            A2_all[s][u][i] = coeff_rec[u][i]
            
A2 = {}
for s in sens:
    A2[s] = {}
    for u in upgrade:
        A2[s][u] = {}
        for i in range(2011,2101):
            A2[s][u][i] = pd.DataFrame(0, index = met*4, columns = comp)
            A2[s][u][i] = A2_all[s][u][i]*a_base

A2_act = {}
for s in sens:
    A2_act[s] = {}
    for u in upgrade:
        A2_act[s][u] = {}
        for i in range(2011,2101):
            if i in range(2011,2024):                
                A2_act[s][u][i]= pd.DataFrame(0, index = met*4, columns =  comp)
                A2_act[s][u][i] = A2_all[s][u][i]*a_act.loc[:,2023]
                for r in region:
                    if r != 'EU27+UK':
                       A2_act[s][u][i].loc[:,(r,'Sector', ref)] = A2[s][u][i].loc[:,(r,'Sector', ref)]
                
                #A2[s][u][i].index = pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 4 * len(met), met*4])
                #A2[s][u][i].columns= pd.MultiIndex.from_arrays([['EU27+UK'] * len(ref), ['Sector'] * len(ref), ref])
                
            elif i in range(2024,2031):
                A2_act[s][u][i]= pd.DataFrame(0, index = met*4, columns =  comp)
                A2_act[s][u][i] = A2_all[s][u][i]*a_act.loc[:,i]
                for r in region:
                    if r != 'EU27+UK':
                       A2_act[s][u][i].loc[:,(r,'Sector', ref)] = A2[s][u][i].loc[:,(r,'Sector', ref)]
                #A2[s][u][i].index = pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 4 * len(met), met*4])
                #A2[s][u][i].columns= pd.MultiIndex.from_arrays([['EU27+UK'] * len(ref), ['Sector'] * len(ref), ref])
                
            else:
                A2_act[s][u][i]= pd.DataFrame(0, index = met*4, columns =  comp)
                A2_act[s][u][i] = A2_all[s][u][i]*a_act.loc[:,2030]
                for r in region:
                    if r != 'EU27+UK':
                       A2_act[s][u][i].loc[:,(r,'Sector', ref)] = A2[s][u][i].loc[:,(r,'Sector', ref)]
                #A2[s][u][i].index = pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 4 * len(met), met*4])
                #A2[s][u][i].columns= pd.MultiIndex.from_arrays([['EU27+UK'] * len(ref), ['Sector'] * len(ref), ref])
                

#%% Reshaping Dictionary AIC
Tech_FD = {}        
for s in sens:
    Tech_FD[s]={}
    for i in years:
        Tech_FD[s][i] = pd.DataFrame(0, index=techs*4, columns=region)
        Tech_FD[s][i].index = pd.MultiIndex.from_arrays([['EU27+UK','EU27+UK','EU27+UK','USA','USA','USA','RoW','RoW','RoW','China','China','China'],['Sector']*len(techs)*len(region),techs*len(region)], names=['Region', 'Level', 'Item'])
       
for s in sens:
    for t in techs:
        for i in years:
            for r in region:
                Tech_FD[s][i].loc[(r,'Sector',t),r]= AIC[t][s].loc[r,i]
                Tech_FD[s][i].columns = pd.MultiIndex.from_arrays([region,['Consumption category'] * len(region), ['Final consumption expenditure by households'] * len(region)], names=['Region', 'Level', 'Item']    ) 
                SwFD[s][i].columns = pd.MultiIndex.from_arrays([region,['Consumption category'] * len(region), ['Final consumption expenditure by households'] * len(region)], names=['Region', 'Level', 'Item']    ) 

new_order = ['EU27+UK', 'USA', 'RoW', 'China']  # Nuovo ordine delle colonne
for s in sens:
    for i in years:
        SwFD[s][i] = SwFD[s][i][new_order]
        Tech_FD[s][i] = Tech_FD[s][i][new_order]              
# for s in sens:
#     for i in years:
#         Tech_FD[s][i] = Tech_FD[s][i].set_index([pd.Index(['EU27+UK'] * len(techs)),pd.Index(['Sector'] * len(techs)), techs])
#         SwFD[s][i] = SwFD[s][i].set_index([pd.Index(['EU27+UK'] * len(waste_sectors)),pd.Index(['Sector'] * len(waste_sectors)), waste_sectors])

# regions = Tech_FD[s][i].columns
# for s in sens:
#     for i in years:
#         # Aggiungi gli indici a Tech_FD[s][i]
#             Tech_FD[s][i].index = pd.MultiIndex.from_arrays([['EU27+UK'] * len(techs), ['Sector'] * len(techs), techs],
#                                                            names=['Region', 'Level', 'Item'])
#             Tech_FD[s][i].columns = pd.MultiIndex.from_arrays(
#                     [regions,['Consumption category'] * len(regions), ['Final consumption expenditure by households'] * len(regions)], names=['Region', 'Level', 'Item']    ) 
#             # Aggiungi gli indici a SwFD[s][i]
#             SwFD[s][i].index = pd.MultiIndex.from_arrays([['EU27+UK'] * len(waste_sectors), ['Sector'] * len(waste_sectors), waste_sectors],
#                                                          names=['Region', 'Level', 'Item'])
#             SwFD[s][i].columns = pd.MultiIndex.from_arrays(
#                     [regions,['Consumption category'] * len(regions), ['Final consumption expenditure by households'] * len(regions)], names=['Region', 'Level', 'Item']    ) 

#%% Metals recycled for each component 
met_rec_comp = {} 
for s in sens:              
    met_rec_comp[s]={}
    for u in upgrade:
        met_rec_comp[s][u]={}
        for i in years:
            met_rec_comp[s][u][i] = pd.DataFrame(0, index=a_base.index, columns = pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 4 * len(comp), comp*4]))

for s in sens:
    for u in upgrade:
        for i in years:
            for r in region:
                for m in met:
                    for c in comp:           
                        for t in techs:
                            met_rec_comp[s][u][i].loc[(r,'Sector',m),(r,'Sector',c)] += -met_recycled_specific[t][s][c][m][u].loc[r,i]
                            
for s in sens:   
    for u in upgrade:
        for c in comp:
            for i in years:
                for t in techs:
                    for m in met:
                        met_rec_comp[s][u][i].columns = a_base.columns #pd.MultiIndex.from_arrays([['EU27+UK'] * len(ref), ['Sector'] * len(ref), ref],names=['Region', 'Level', 'Item'])
                        
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
           
    with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['AIC',user]}\\AIC_{s}.xlsx") as writer:
            for key, df in Tech_FD[s].items():
                sheet_name = f'{key}'
                df.to_excel(writer, sheet_name=sheet_name, index= True)
    
    # for u in upgrade:
    #     with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['metrec',user]}\\metrec_{s}_{u}.xlsx") as writer:
    #         for key, df in met_rec_comp[s][u].items():
    #             sheet_name = f'{key}'
    #             df.to_excel(writer, sheet_name=sheet_name, index= True)
    # for u in upgrade:
    #     with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['metrec',user]}\\metrec_{s}_{u}.xlsx") as writer:
    #         for key, df in met_sum[m][s][u].items():
    #             sheet_name = f'{key}'
    #             df.to_excel(writer, sheet_name=sheet_name, index= True)        
    for u in upgrade:
        with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['A2',user]}\\Baseline\\A2_{s}_{u}.xlsx") as writer:
            for key, df in A2[s][u].items():
                sheet_name = f'{key}'
                df.to_excel(writer, sheet_name=sheet_name, index= True)
        
    for u in upgrade:
        with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['A2',user]}\\Act\\A2_act_{s}_{u}.xlsx") as writer:
            for key, df in A2_act[s][u].items():
                sheet_name = f'{key}'
                df.to_excel(writer, sheet_name=sheet_name, index= True)


#%% Materials recycled in physical units [tons] (questo probabilmente si può ricavare direttamente da X2 una volta che è stato runnato lo scenario desiderato)
price_materials = pd.read_excel(fileParam,sheet_name='price materials', index_col=[0], header=[0])
price = pd.concat([price_materials] * 4, ignore_index= True) #unit of price [USD/kg]
price.index = pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 16, ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']*4])

USD_to_EUR = pd.read_excel(fileParam,"USD to EURO", header=0, index_col=0)

met_rec_mon = {} #unit M€
for s in sens:
    met_rec_mon[s] = {}
    for u in upgrade:
        met_rec_mon[s][u] = {}
        for i in years:
            met_rec_mon[s][u][i] = {} #pd.DataFrame(0, index=['Recycled'],columns = met)
            met_rec_mon[s][u][i] = -met_rec_comp[s][u][i].sum(axis =1)
            
met_rec = {}    #conversion in tons
for s in sens:
    met_rec[s] = {}
    for u in upgrade:
        met_rec[s][u] = {}
        for p in sens:
            met_rec[s][u][p] = {}
            for i in years:
                for r in region:
                    met_rec[s][u][p][i] = {}
                    met_rec[s][u][p][i] = ((met_rec_mon[s][u][i] * 10**6)/(price.loc[:,p] * USD_to_EUR.loc['EURO/USD',i] ))* 10**-3
                                             
for s in sens:
    for u in upgrade:
        for p in price:
            with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['metrec',user]}\\metrec_{s}_{u}_{p}.xlsx") as writer:
                for key, df in met_rec[s][u][p].items():
                    sheet_name = f'{key}'
                    df.to_excel(writer, sheet_name=sheet_name, index= True)
                    
#%% Material recycled in each tecnology in physical units [tons]
price_materials = pd.read_excel(fileParam,sheet_name='price materials', index_col=[0], header=[0])
price = pd.concat([price_materials] * 4, ignore_index= True) #unit of price [USD/kg]
price.index = pd.MultiIndex.from_arrays([['China', 'China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'EU27+UK','RoW', 'RoW', 'RoW', 'RoW','USA', 'USA', 'USA', 'USA'], ['Sector'] * 16, ['Neodymium','Dysprosium', 'Copper', 'Raw silicon']*4])

USD_to_EUR = pd.read_excel(fileParam,"USD to EURO", header=0, index_col=0)

met_rec_tech_mon = {}
for s in sens:
    met_rec_tech_mon[s] = {}
    for u in upgrade:
        met_rec_tech_mon[s][u] = {}
        for i in years:
            met_rec_tech_mon[s][u][i] = pd.DataFrame(0, index=a_base.index ,columns = pd.MultiIndex.from_arrays([['China', 'China', 'China','EU27+UK', 'EU27+UK', 'EU27+UK', 'RoW', 'RoW', 'RoW', 'USA', 'USA', 'USA'],['Sector']*len(techs)*len(region),techs*len(region)]))
            
                
for s in sens:
    for u in upgrade:
        for c in comp:
            for i in years:
                for t in techs:
                    for m in met:
                        for r in region:
                            met_rec_tech_mon[s][u][i].loc[(r,'Sector',m),(r,'Sector',t)] += met_recycled_specific[t][s][c][m][u].loc[r,i]


met_rec_tech = {}    #conversion in tons
for s in sens:
    met_rec_tech[s] = {}
    for u in upgrade:
        met_rec_tech[s][u] = {}
        for p in sens:
            met_rec_tech[s][u][p] = {}
            for i in years:
                met_rec_tech[s][u][p][i] = pd.DataFrame(0, index = a_base.index, columns= met_rec_tech_mon[s][u][i].columns)                
                
                
for s in sens:
    for u in upgrade:
        for p in sens:
            for i in years:               
                for r in region:
                    for t in techs:
                        met_rec_tech[s][u][p][i].loc[:,(r,'Sector',t)] = ((met_rec_tech_mon[s][u][i].loc[:,(r,'Sector',t)]* 10**6)/(price.loc[:,p] * USD_to_EUR.loc['EURO/USD',i] ))* 10**-3
                        
for s in sens:
    for u in upgrade:
        for p in price:
            with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['metrec_tech',user]}\\metrec_tech_{s}_{u}_{p}.xlsx") as writer:
                for key, df in met_rec_tech[s][u][p].items():
                    sheet_name = f'{key}'
                    df.to_excel(writer, sheet_name=sheet_name, index= True)





