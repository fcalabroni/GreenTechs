import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns
from matplotlib.gridspec import GridSpec

user = 'CF'
paths = 'Paths.xlsx'
#%%cumulativa baseline con i tre RR

sens = ['hist', 'target', 'full']
res_base_RR = {}
met_rec_divided = {}

for s in sens:
    res_base_RR[s] = {}
for s in sens:
    met_rec_divided[s] = {}
    for y in range(2000,2101):
        met_rec_divided[s][y] = {}
            
for s in sens:
    fileResults = f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Baseline\\RR\\Results_world_base_RR_{s}.xlsx"
    res_base_RR[s] =  pd.read_excel(fileResults, "Cumulative", index_col=[0,1,2])
    fileMetrec = f"{pd.read_excel(paths, index_col=[0]).loc['metrec',user]}\\metrec_Avg_{s}_Avg.xlsx"
    for y in range(2000,2101):
        met_rec_divided[s][y] = pd.read_excel(fileMetrec, f'{y}',index_col=[0,1,2])

met = res_base_RR['target'].index.get_level_values(2)
region =  res_base_RR['target'].index.get_level_values(0)
sector = res_base_RR['target'].index.get_level_values(1)
years = res_base_RR['target'].columns

met_rec = {}
  
regions = met_rec_divided['target'][2000].index.get_level_values(0)
mets = met_rec_divided['target'][2000].index.get_level_values(2)
for s in sens:        
    for y in range(2000,2101):
        met_rec[s] = pd.DataFrame(0,index= pd.MultiIndex.from_arrays([regions, ['Sector']*16 , mets]), columns = range(2000,2101))
        
        
for s in sens:
    for y in range(2000,2101):
        met_rec[s].loc[:, y] = met_rec_divided[s][y].loc[:, :].values
        
met_rec_world = {}
met_rec_cumulative = {}
for s in sens:
    for m in met:
        
        met_rec_world[s] = pd.DataFrame(0,index = met, columns = range(2000,2101))
        met_rec_cumulative[s] = pd.DataFrame(0, index = met, columns=range(2000,2101))

        met_rec_world[s].loc['Dysprosium'] = met_rec[s].loc[(regions,'Sector','Dysprosium'),:].sum()
        met_rec_world[s].loc['Neodymium'] = met_rec[s].loc[(regions,'Sector','Neodymium'),:].sum()
        met_rec_world[s].loc['Copper'] = met_rec[s].loc[(regions,'Sector','Copper'),:].sum()
        met_rec_world[s].loc['Raw silicon'] = met_rec[s].loc[(regions,'Sector','Raw silicon'),:].sum()
        
        for y in range(2000,2101):
            if y == 2000:
                met_rec_cumulative[s].loc[:,y] = met_rec_world[s].loc[:,y]
            else:
                met_rec_cumulative[s].loc[:,y] = met_rec_cumulative[s].loc[:,y - 1] + met_rec_world[s].loc[:,y]

#%% Cumulative Nd
#%% Cumulative Nd
with plt.style.context('fivethirtyeight'):
    plt.figure(figsize=(12, 8))

    plt.plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Neodymium'), :], label='Target', linestyle='-', markersize=8)
    plt.plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Neodymium'), :], label='Hist', linestyle='--', markersize=8)
    plt.plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Neodymium'), :], label='Full', linestyle='-.', markersize=8)
    # plt.plot(years, [16000000] * len(years), label='Reserves', linestyle='--', color='gray')

     # Adding labels, title, and legend
    plt.legend(fontsize='xx-large')
    plt.xlabel('Year',fontsize='xx-large')
    plt.ylabel('Cumulative Nd extraction in the world',fontsize='xx-large')
    plt.title('Cumulative Nd',fontsize='xx-large')

    # Adding grid
    plt.grid(True, linestyle='-', alpha=0.7)

    # Adding a background color
    plt.axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Neodymium'), :]), facecolor='#f2f2f2', alpha=0.2)
    #sns.set_palette('husl')
    plt.tick_params(axis='both', which='major', labelsize='xx-large')

    plt.tight_layout()
    plt.show()
    
#%% Cumulative Dy
with plt.style.context('fivethirtyeight'):
    plt.figure(figsize=(12, 8))

    plt.plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Dysprosium'), :], label='Target', linestyle='-', markersize=8)
    plt.plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Dysprosium'), :], label='Hist', linestyle='--', markersize=8)
    plt.plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Dysprosium'), :], label='Full', linestyle='-.', markersize=8)
    # plt.plot(years, [544000] * len(years), label='Reserves', linestyle='--', color='gray')

     # Adding labels, title, and legend
    plt.legend(fontsize='xx-large')
    plt.xlabel('Year',fontsize='xx-large')
    plt.ylabel('Cumulative Dysprosium extraction in the world',fontsize='xx-large')
    plt.title('Cumulative Dysprosium',fontsize='xx-large')

    # Adding grid
    plt.grid(True, linestyle='-', alpha=0.7)

    # Adding a background color
    plt.axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Dysprosium'), :]), facecolor='#f2f2f2', alpha=0.2)
    #sns.set_palette('husl')
    plt.tick_params(axis='both', which='major', labelsize='xx-large')

    plt.tight_layout()
    plt.show()

#%% Cumulative Cu
with plt.style.context('fivethirtyeight'):
    plt.figure(figsize=(12, 8))

    plt.plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Copper'), :], label='Target', linestyle='-', markersize=8)
    plt.plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Copper'), :], label='Hist', linestyle='--', markersize=8)
    plt.plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Copper'), :], label='Full', linestyle='-.', markersize=8)
    # plt.plot(years, [890000000] * len(years), label='Reserves', linestyle='--', color='gray')

     # Adding labels, title, and legend
    plt.legend(fontsize='xx-large')
    plt.xlabel('Year',fontsize='xx-large')
    plt.ylabel('Cumulative Copper extraction in the world',fontsize='xx-large')
    plt.title('Cumulative Copper',fontsize='xx-large')

    # Adding grid
    plt.grid(True, linestyle='-', alpha=0.7)

    # Adding a background color
    plt.axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Copper'), :]), facecolor='#f2f2f2', alpha=0.2)
    #sns.set_palette('husl')
    plt.tick_params(axis='both', which='major', labelsize='xx-large')

    plt.tight_layout()
    plt.show()

#%% Cumulative Si
with plt.style.context('fivethirtyeight'):
    plt.figure(figsize=(12, 8))

    plt.plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Raw silicon'), :], label='Target', linestyle='-', markersize=8)
    plt.plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Raw silicon'), :], label='Hist', linestyle='--', markersize=8)
    plt.plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Raw silicon'), :], label='Full', linestyle='-.', markersize=8)
    # plt.plot(years, [16000000] * len(years), label='Reserves', linestyle='--', color='gray')

     # Adding labels, title, and legend
    plt.legend(fontsize='xx-large')
    plt.xlabel('Year',fontsize='xx-large')
    plt.ylabel('Cumulative Raw silicon extraction in the world',fontsize='xx-large')
    plt.title('Cumulative Raw silicon',fontsize='xx-large')

    # Adding grid
    plt.grid(True, linestyle='-', alpha=0.7)

    # Adding a background color
    plt.axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Raw silicon'), :]), facecolor='#f2f2f2', alpha=0.2)
    #sns.set_palette('husl')
    plt.tick_params(axis='both', which='major', labelsize='xx-large')

    plt.tight_layout()
    plt.show()
    
#%% Ratio between cumulative demand in 2100 and reserves
neodymium_last_year_values_full = res_base_RR['full'].loc[('World', 'Sector', 'Neodymium'), res_base_RR['full'].columns[-1]]/16000000
neodymium_last_year_values_hist = res_base_RR['hist'].loc[('World', 'Sector', 'Neodymium'), res_base_RR['full'].columns[-1]]/16000000
neodymium_last_year_values_target = res_base_RR['target'].loc[('World', 'Sector', 'Neodymium'), res_base_RR['full'].columns[-1]]/16000000
# Calcolo degli offset per distanziare le barre
bar_width = 0.2
offsets = [-bar_width, 0, bar_width]

with plt.style.context('fivethirtyeight'):
    plt.figure(figsize=(12, 8))

    for offset, label, data, color in zip(offsets, ['full', 'hist', 'target'], [neodymium_last_year_values_full, neodymium_last_year_values_hist, neodymium_last_year_values_target], ['skyblue', 'lightcoral', 'lightgreen']):
        plt.bar([0 + offset], [data], width=bar_width, edgecolor='black', label=label, color=color)

    plt.axhline(y=1, linestyle='--', color='gray', label='Reserves')

    plt.xlabel('Neodymium', fontsize=18)
    plt.ylabel('Value', fontsize=18)
    plt.title('Ratio between cumulative demand in 2100 and reserves for Nd', fontsize=18)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks([0 + offset for offset in offsets], ['full', 'hist', 'target'], fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)

    # Aggiunta di effetti di sfondo
    plt.gca().set_facecolor('#f0f0f0')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.show()
#%% Ratio between cumulative demand in 2100 and reserves for Dy
dysprosium_last_year_values_full = res_base_RR['full'].loc[('World', 'Sector', 'Dysprosium'), res_base_RR['full'].columns[-1]]/544000
dysprosium_last_year_values_hist = res_base_RR['hist'].loc[('World', 'Sector', 'Dysprosium'), res_base_RR['full'].columns[-1]]/544000
dysprosium_last_year_values_target = res_base_RR['target'].loc[('World', 'Sector', 'Dysprosium'), res_base_RR['full'].columns[-1]]/544000
# Calcolo degli offset per distanziare le barre
bar_width = 0.2
offsets = [-bar_width, 0, bar_width]

with plt.style.context('fivethirtyeight'):
    plt.figure(figsize=(12, 8))

    for offset, label, data, color in zip(offsets, ['full', 'hist', 'target'], [dysprosium_last_year_values_full, dysprosium_last_year_values_hist, dysprosium_last_year_values_target], ['skyblue', 'lightcoral', 'lightgreen']):
        plt.bar([0 + offset], [data], width=bar_width, edgecolor='black', label=label, color=color)

    plt.axhline(y=1, linestyle='--', color='gray', label='Reserves')

    plt.xlabel('Dysprosium', fontsize=18)
    plt.ylabel('Value', fontsize=18)
    plt.title('Ratio between cumulative demand in 2100 and reserves for Dy', fontsize=18)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks([0 + offset for offset in offsets], ['full', 'hist', 'target'], fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)

    # Aggiunta di effetti di sfondo
    plt.gca().set_facecolor('#f0f0f0')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.show()
    
#%% Ratio between cumulative demand in 2100 and reserves for Cu
copper_last_year_values_full = res_base_RR['full'].loc[('World', 'Sector', 'Copper'), res_base_RR['full'].columns[-1]]/890000000
copper_last_year_values_hist = res_base_RR['hist'].loc[('World', 'Sector', 'Copper'), res_base_RR['full'].columns[-1]]/890000000
copper_last_year_values_target = res_base_RR['target'].loc[('World', 'Sector', 'Copper'), res_base_RR['full'].columns[-1]]/890000000
# Calcolo degli offset per distanziare le barre
bar_width = 0.2
offsets = [-bar_width, 0, bar_width]

with plt.style.context('fivethirtyeight'):
    plt.figure(figsize=(12, 8))

    for offset, label, data, color in zip(offsets, ['full', 'hist', 'target'], [copper_last_year_values_full, copper_last_year_values_hist, copper_last_year_values_target], ['skyblue', 'lightcoral', 'lightgreen']):
        plt.bar([0 + offset], [data], width=bar_width, edgecolor='black', label=label, color=color)

    plt.axhline(y=1, linestyle='--', color='gray', label='Reserves')

    plt.xlabel('Copper', fontsize=18)
    plt.ylabel('Value', fontsize=18)
    plt.title('Ratio between cumulative demand in 2100 and reserves for Cu', fontsize=18)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks([0 + offset for offset in offsets], ['full', 'hist', 'target'], fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)

    # Aggiunta di effetti di sfondo
    plt.gca().set_facecolor('#f0f0f0')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.show()
    
#%% Ratio between cumulative demand in 2100 and reserves (Nd, Dy, Si)
# Crea la legenda con spiegazione per ogni colonna
legend_labels = ['Full', 'Hist', 'Target']

with plt.style.context('fivethirtyeight'):
    fig, ax = plt.subplots(figsize=(18, 6))

    # Plot per Dysprosium
    for offset, label, data, color in zip(offsets, ['full', 'hist', 'target'], [dysprosium_last_year_values_full, dysprosium_last_year_values_hist, dysprosium_last_year_values_target], ['skyblue', 'lightcoral', 'lightgreen']):
        ax.bar([0 + offset], [data], width=bar_width, edgecolor='black', label=f'{label}', color=color)

    # Plot per Neodymium
    for offset, label, data, color in zip(offsets, ['full', 'hist', 'target'], [neodymium_last_year_values_full, neodymium_last_year_values_hist, neodymium_last_year_values_target], ['skyblue', 'lightcoral', 'lightgreen']):
        ax.bar([1 + offset], [data], width=bar_width, edgecolor='black', color=color)

    # Plot per Copper
    for offset, label, data, color in zip(offsets, ['full', 'hist', 'target'], [copper_last_year_values_full, copper_last_year_values_hist, copper_last_year_values_target], ['skyblue', 'lightcoral', 'lightgreen']):
        ax.bar([2 + offset], [data], width=bar_width, edgecolor='black',  color=color)

    # Retta orizzontale comune a tutti i gruppi
    ax.axhline(y=1, linestyle='--', color='gray', label='Reserves')

    # Impostazione della legenda
    ax.legend(loc='upper left', bbox_to_anchor=(0, 1), fontsize=14)

    # Impostazioni aggiuntive
    ax.set_title('Ratio between cumulative demand in 2100 and reserves', fontsize=18)
    ax.set_ylabel('Ratio', fontsize=16)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(['Dysprosium', 'Neodymium', 'Copper'], fontsize=14)

    # Aggiunta di effetti di sfondo
    ax.set_facecolor('#f0f0f0')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.show()

#%%
# ... (il resto del tuo codice)

# Creazione del grafico per gli istogrammi

