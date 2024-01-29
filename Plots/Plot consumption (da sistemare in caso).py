import matplotlib.pyplot as plt
import pandas as pd 
from matplotlib.gridspec import GridSpec

user = 'CF'
paths = 'Paths.xlsx'
#%%
sens = ['hist', 'target', 'full']
share_consumption_divided = {}

for s in sens:
    share_consumption_divided[s] = {}
    for y in range(2011,2101):
        share_consumption_divided[s][y] = {}
            
for s in sens:
    fileResults = f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Baseline\\Share consumption\\Share_base_{s}.xlsx"
    for y in range(2011,2101):
        share_consumption_divided[s][y] = pd.read_excel(fileResults, f'{y}',header = [0,1,2],index_col=[0])


regions = ['EU2+UK','China','USA','RoW']
met = ['Neodymium','Dysprosium','Copper','Raw silicon']
share_consumption ={}
for s in sens:  
    share_consumption[s] = {}
    for m in met:
        share_consumption[s][m] = pd.DataFrame(0,index= regions, columns = range(2011,2101))
      
        
for s in sens:
    for m in met:
        for y in range(2011,2101):
            share_consumption[s][m].loc[:, y] = share_consumption_divided[s][y].loc[:, ('World','Green Tech',m)].values

#%%
import matplotlib.pyplot as plt
years_elected = [2011, 2030, 2050, 2100]

data_to_plot_f = share_consumption['full']['Copper'].loc[:, years_elected]
data_to_plot_h = share_consumption['hist']['Copper'].loc[:, years_elected]
data_to_plot_t = share_consumption['target']['Copper'].loc[:, years_elected]

# Plot dello stacked histogram
fig, ax = plt.subplots(figsize=(10, 6))

data_to_plot_f.T.plot(kind='bar', stacked=True, ax=ax)
data_to_plot_h.T.plot(kind='bar', stacked=True, ax=ax)
data_to_plot_t.T.plot(kind='bar', stacked=True, ax=ax)

# Aggiungi etichette e titolo
ax.set_xlabel('Year')
ax.set_ylabel('Share Consumption')
ax.set_title('Stacked Histogram for Share Consumption (s=full, m=Copper)')

# Mostra il plot
plt.legend(title='Regions', loc='upper left', bbox_to_anchor=(1, 1))
plt.show()
#%% SBAGLIATO DA RIFARE
import matplotlib.pyplot as plt

# Seleziona i dati specifici per il grafico a barre
data_to_plot_Nd = share_consumption['target']['Neodymium'].loc[:, years_elected]
data_to_plot_Dy = share_consumption['target']['Dysprosium'].loc[:, years_elected]
data_to_plot_Cu = share_consumption['target']['Copper'].loc[:, years_elected]
data_to_plot_Si = share_consumption['target']['Raw silicon'].loc[:, years_elected]

# Creazione del grafico
fig, ax = plt.subplots(figsize=(12, 8))
offset = 0.2  # Modifica questo valore per regolare l'offset

# Posizioni degli anni
positions = range(len(years_elected))

# Istogramma per il metallo Neodymium
data_to_plot_Nd.T.plot(kind='bar', stacked=True, ax=ax, position=0.1, width=0.3, color=['#26547c', '#ef476f', '#ffd166', '#06d6a0'], edgecolor = 'white')

# Istogramma per il metallo Dysprosium
data_to_plot_Dy.T.plot(kind='bar', stacked=True, ax=ax, position=0.3, width=0.3, color=['#26547c', '#ef476f', '#ffd166', '#06d6a0'], edgecolor = 'white')

# Istogramma per il metallo Copper
data_to_plot_Cu.T.plot(kind='bar', stacked=True, ax=ax, position=0.5, width=0.3, color=['#26547c', '#ef476f', '#ffd166', '#06d6a0'], edgecolor = 'white')

# Istogramma per il metallo Raw silicon
data_to_plot_Si.T.plot(kind='bar', stacked=True, ax=ax, position=0.7, width=0.3, color=['#26547c', '#ef476f', '#ffd166', '#06d6a0'], edgecolor = 'white')

# Aggiungi etichette e titolo
ax.set_xlabel('Year')
ax.set_ylabel('Share Consumption')
ax.set_title('Share Consumption for Each Metal (Sensitivity: target)')

# Mostra la legenda
ax.legend(['EU2+UK', 'China', 'USA', 'RoW'], title='Metals', loc='upper left', bbox_to_anchor=(1, 1))

# Mostra il grafico
plt.show()
