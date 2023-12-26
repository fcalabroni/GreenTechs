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
   'Onshore wind plants': WindOn_Capacity,
   'Offshore wind plants': WindOff_Capacity,
   'Photovoltaic plants': SolarPV_Capacity,
   } #installed capacity in MW

WindOff_Cost = pd.read_excel(fileWind, "Cost_Offshore", header=0, index_col=None)
WindOn_Cost = pd.read_excel(fileWind, "Cost_Onshore", header=0, index_col=None)
SolarPV_Cost = pd.read_excel(fileSolar, "Cost_PV", header=0, index_col=None)
Cost = {
        'Onshore wind plants': WindOn_Cost,
        'Offshore wind plants': WindOff_Cost,
        'Photovoltaic plants': SolarPV_Cost,
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


#%% Estimation of scraps trhough Collector and Disassembler
comp = ['Generator Onshore', 'Generator Offshore', 'Panel', 'Wires']

CR_tech = pd.read_excel(fileParam, "CR", header = 0 , index_col=None)
DR_tech = pd.read_excel(fileParam, "DR", header = 0 , index_col=None)

Inventory_comp = pd.read_excel(fileParam, "Inventory_comp", header = 0, index_col = 0)

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
            scraps[t][c][s] = EoL[t][s] * DR[t] * CR[t] * Inv_comp[c][t]

#%% Estimation of recycled materials
met = ['Neodymium', 'Dysprosium', 'Copper ores and concentrates', 'Raw silicon']

RE_comp = pd.read_excel(fileParam, "RE", header = 0, index_col = None)
RR_met = pd.read_excel(fileParam, "RR", header = 0, index_col = 0)

#met = list(set(RR_met.columns.get_level_values(0)))
Inventory_met = pd.read_excel(fileParam, "Inventory_mat", header = 0, index_col = 0)

upgrade = ['b1', 'b2', 'b3']
RE = {
  'Generator Onshore': RE_comp.loc[0,'Generator Onshore'],
  'Generator Offshore': RE_comp.loc[0,'Generator Offshore'],
  'Panel': RE_comp.loc[0,'Panel'],
  'Wires': RE_comp.loc[0,'Wires'],
      }

RR = {
  'Neodymium': RR_met.loc[:, 'Neodymium'], 
  'Dysprosium': RR_met.loc[:, 'Dysprosium'], 
  'Copper ores and concentrates': RR_met.loc[:, 'Copper ores and concentrates'], 
  'Raw silicon': RR_met.loc[:, 'Raw silicon'],
      }

Inv_met = {
   'Neodymium': Inventory_met.loc['%Nd', :], 
   'Dysprosium': Inventory_met.loc['%Dy', :], 
   'Copper ores and concentrates': Inventory_met.loc['%Cu', :], 
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
        W2[s][i] = pd.DataFrame(0, index= waste_type, columns = waste_sectors )

for s in sens:
    for i in years:
        W2[s][i].loc['Scraps of generator of Offshore WT','Disassembler of Wind Turbines'] = scraps['Offshore wind plants']['Generator Offshore'][s].loc[0, i]
        W2[s][i].loc['Scraps of generator of Onshore WT','Disassembler of Wind Turbines'] = scraps['Onshore wind plants']['Generator Onshore'][s].loc[0, i]
        W2[s][i].loc['Scraps of wires','Disassembler of Wind Turbines'] = scraps['Offshore wind plants']['Wires'][s].loc[0, i] + scraps['Onshore wind plants']['Wires'][s].loc[0, i]
        W2[s][i].loc['Residues','Disassembler of Wind Turbines'] = res['z_dis_WT'][s].loc[0, i]

        W2[s][i].loc['Scraps of wires','Disassembler of PV panels'] = scraps['Photovoltaic plants']['Wires'][s].loc[0, i]
        W2[s][i].loc['Scraps of Silicon layer','Disassembler of PV panels'] = scraps['Photovoltaic plants']['Panel'][s].loc[0, i]
        W2[s][i].loc['Residues','Disassembler of PV panels'] = res['z_dis_PV'][s].loc[0, i]

        W2[s][i].loc['Residues','Refinery of Generators of Offshore Wind Turbines'] = res['z_ref_OffGen'][s].loc[0, i]
        W2[s][i].loc['Residues','Refinery of Generators of Onshore Wind Turbines'] = res['z_ref_OnGen'][s].loc[0, i]
        W2[s][i].loc['Residues','Refinery of Silicon layer in PV panel'] = res['z_ref_Panel'][s].loc[0, i]
        W2[s][i].loc['Residues','Refinery of Cu in wires of WT and PV'] = res['z_ref_Wires'][s].loc[0, i]


wFD = {}
for s in sens:
    wFD[s] = {}
    for i in years:
        wFD[s][i] = pd.DataFrame(0, index= waste_type, columns = ['EU27+UK'] )

for s in sens:
    for i in years:
        wFD[s][i].loc['EoL of Offshore WT','EU27+UK'] = EoL['Offshore wind plants'][s].loc[0, i]
        wFD[s][i].loc['EoL of Onshore WT','EU27+UK'] = EoL['Onshore wind plants'][s].loc[0, i]
        wFD[s][i].loc['EoL of PV','EU27+UK'] = EoL['Photovoltaic plants'][s].loc[0, i] 

#%% Create allocation matrix (S)
S = pd.read_excel(fileParam, "S", header = 0, index_col = 0 )

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
        SwFD[s][i] = pd.DataFrame(0, index= waste_sectors, columns = ['China','EU27+UK','RoW','USA'] )
       

SwFD_EU = {}
for s in sens:
    SwFD_EU[s] = {}
    for i in years:
        SwFD_EU[s][i] = pd.DataFrame(0, index= waste_sectors, columns = ['EU27+UK'] )
        
for s in sens:
    for i in years:
        SwFD_EU[s][i]= S @ wFD[s][i]
        SwFD[s][i].loc[:,'EU27+UK'] = SwFD_EU[s][i].loc[:,'EU27+UK']
        
#%% Calculating coefficient matrix SG2 = SW2 * (Xw)^-1
                                           
SG2 = {}
for s in sens:
    SG2[s]= {}
    for i in range(2011,2101):
        SG2[s][i] = pd.DataFrame(0, index= waste_sectors, columns = waste_sectors)
        
Xw = {}
for s in sens:
    Xw[s] = {}
    for i in range(2011,2101):
        Xw[s][i] = pd.DataFrame(0, index= waste_sectors, columns = ['Xw'] )
        
for s in sens:
    for i in range(2011,2101):
        Xw[s][i] = SW2[s][i].sum(axis = 1) + SwFD[s][i].loc[:,'EU27+UK']

for s in sens:
    for i in range(2011,2101):
        SG2[s][i] = SW2[s][i] @ np.linalg.inv(np.diag(Xw[s][i]))
        
for s in sens:
    for i in range(2011,2101):        
        SG2[s][i].index =  pd.MultiIndex.from_arrays([['EU27+UK'] * len(waste_sectors), ['Sector'] * len(waste_sectors), waste_sectors], names=['Region', 'Level', 'Item'])   
        SG2[s][i].columns = pd.MultiIndex.from_arrays([['EU27+UK'] * len(waste_sectors), ['Sector'] * len(waste_sectors), waste_sectors])
#%% Reshaping Dictionary AIC
Tech_FD = {}
for s in sens:
    Tech_FD[s]={}
    for i in years:
        Tech_FD[s][i] = pd.DataFrame(0, index=techs, columns=['China','EU27+UK','RoW','USA'])

for s in sens:
    for t in techs:
        for i in years:
            Tech_FD[s][i].loc[t,'EU27+UK']= AIC[t][s].loc[0,i]
            
for s in sens:
    for i in years:
        Tech_FD[s][i] = Tech_FD[s][i].set_index([pd.Index(['EU27+UK'] * len(techs)),pd.Index(['Sector'] * len(techs)), techs])
        SwFD[s][i] = SwFD[s][i].set_index([pd.Index(['EU27+UK'] * len(waste_sectors)),pd.Index(['Sector'] * len(waste_sectors)), waste_sectors])

regions = Tech_FD[s][i].columns
for s in sens:
    for i in years:
        # Aggiungi gli indici a Tech_FD[s][i]
            Tech_FD[s][i].index = pd.MultiIndex.from_arrays([['EU27+UK'] * len(techs), ['Sector'] * len(techs), techs],
                                                           names=['Region', 'Level', 'Item'])
            Tech_FD[s][i].columns = pd.MultiIndex.from_arrays(
                    [regions,['Consumption category'] * len(regions), ['Final consumption expenditure by households'] * len(regions)], names=['Region', 'Level', 'Item']    ) 
            # Aggiungi gli indici a SwFD[s][i]
            SwFD[s][i].index = pd.MultiIndex.from_arrays([['EU27+UK'] * len(waste_sectors), ['Sector'] * len(waste_sectors), waste_sectors],
                                                         names=['Region', 'Level', 'Item'])
            SwFD[s][i].columns = pd.MultiIndex.from_arrays(
                    [regions,['Consumption category'] * len(regions), ['Final consumption expenditure by households'] * len(regions)], names=['Region', 'Level', 'Item']    ) 

#%% Metals recycled for each component
met_rec_comp = {}
for s in sens:
    met_rec_comp[s]={}
    for u in upgrade:
        met_rec_comp[s][u]={}
        for i in years:
            met_rec_comp[s][u][i] = pd.DataFrame(0, index=met, columns= comp)

for s in sens:
    for u in upgrade:
        for c in comp:
            for i in years:
                for t in techs:
                    for m in met:
                        met_rec_comp[s][u][i].loc[m,c] += -met_recycled_specific[t][s][c][m][u].loc[0,i]
                        
for s in sens:
    for u in upgrade:
        for c in comp:
            for i in years:
                for t in techs:
                    for m in met:
                        met_rec_comp[s][u][i].index = pd.MultiIndex.from_arrays([['EU27+UK'] * len(comp), ['Sector'] * len(comp), comp],names=['Region', 'Level', 'Item'])
                        met_rec_comp[s][u][i].columns = pd.MultiIndex.from_arrays([['EU27+UK'] * len(met), ['Sector'] * len(met), met])
            
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
    
    for u in upgrade:
        with pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['metrec',user]}\\metrec_{s}_{u}.xlsx") as writer:
            for key, df in met_rec_comp[s][u].items():
                sheet_name = f'{key}'
                df.to_excel(writer, sheet_name=sheet_name, index= True)
            





