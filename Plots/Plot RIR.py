import matplotlib.pyplot as plt
import pandas as pd 
from matplotlib.gridspec import GridSpec
import numpy as np

user = 'CF'
paths = 'Paths.xlsx'


#%%
sens = ['hist', 'target', 'full']
met = ['Dysprosium','Neodymium','Copper','Raw silicon']
price = ['Min','Max','Avg']

RIR = {}

RIR_price_hist = {}
RIR_price_target = {}
RIR_price_full = {}

for s in sens:
    RIR[s] = {}
    for m in met:
        RIR[s][m] = {}
        
for p in price:
    RIR_price_hist[p] = {}
    RIR_price_target[p] = {}
    RIR_price_full[p] = {}
    for m in met:
       RIR_price_hist[p][m] = {}
       RIR_price_target[p][m] = {}
       RIR_price_full[p][m] = {}  
for s in sens:
    for m in met:
        fileResults = f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Baseline\\EoL-RIR\\EoL-RIR_base_{s}.xlsx"
        RIR[s][m] =  pd.read_excel(fileResults, f"{m}", index_col=[0])
for p in price:
    fileSens_hist_price = f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Sensitivity\\EOL-RIR\\Price\\EOL_RIR_hist_price_{p}.xlsx"
    fileSens_target_price = f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Sensitivity\\EOL-RIR\\Price\\EOL_RIR_target_price_{p}.xlsx"
    fileSens_full_price = f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Sensitivity\\EOL-RIR\\Price\\EOL_RIR_full_price_{p}.xlsx"
    for m in met:
        RIR_price_hist[p][m] = pd.read_excel(fileSens_hist_price, f"{m}", index_col=[0])
        RIR_price_target[p][m] = pd.read_excel(fileSens_target_price, f"{m}", index_col=[0])
        RIR_price_full[p][m] = pd.read_excel(fileSens_full_price, f"{m}", index_col=[0])
       
#%%
years = range(2011,2101)
selected_years = RIR_price_hist['Avg']['Copper'].columns
RIR_EU = {}
RIR_price_hist_EU = {}
RIR_price_target_EU = {}
RIR_price_full_EU = {}
for s in sens:
    RIR_EU[s] = pd.DataFrame(0,index=met, columns=years)
    
for p in price:
    RIR_price_hist_EU[p] = pd.DataFrame(0,index=met, columns=selected_years)
    RIR_price_target_EU[p] = pd.DataFrame(0,index=met, columns=selected_years)
    RIR_price_full_EU[p] = pd.DataFrame(0,index=met, columns=selected_years)
    
for s in sens:
    for m in met:
        RIR_EU[s].loc[m,years] = RIR[s][m].loc['EU27+UK',:]

for p in price:
    for m in met:
        RIR_price_hist_EU[p].loc[m,selected_years] = RIR_price_hist[p][m].loc['EU27+UK',:]
        RIR_price_target_EU[p].loc[m,selected_years] = RIR_price_target[p][m].loc['EU27+UK',:]
        RIR_price_full_EU[p].loc[m,selected_years] = RIR_price_full[p][m].loc['EU27+UK',:]


#%% RIR dy
# Definizione delle dimensioni del grafico
fig, ax = plt.subplots(figsize=(16, 10))

# Anni selezionati
years_elected = [2011, 2030, 2050, 2100]
sensitivities = ['hist', 'target', 'full']

# Larghezza delle barre
bar_width = 0.2

# Posizioni delle barre per ogni anno
positions = np.arange(len(years_elected))

# Colori per ogni sensibilità
colors = {'hist': '#95a5a6', 'target': '#e74c3c', 'full': '#3498db'}

# Metallo selezionato
metal = 'Dysprosium'

dysprosium_2011_hist_price_min = RIR_price_hist_EU['Min'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[0]]
dysprosium_2030_hist_price_min = RIR_price_hist_EU['Min'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[1]]
dysprosium_2050_hist_price_min = RIR_price_hist_EU['Min'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[2]]
dysprosium_2100_hist_price_min = RIR_price_hist_EU['Min'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[-1]]

dysprosium_2011_hist_price_max = RIR_price_hist_EU['Max'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[0]]
dysprosium_2030_hist_price_max = RIR_price_hist_EU['Max'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[1]]
dysprosium_2050_hist_price_max = RIR_price_hist_EU['Max'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[2]]
dysprosium_2100_hist_price_max = RIR_price_hist_EU['Max'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[-1]]


dysprosium_2011_target_price_min = RIR_price_target_EU['Min'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[0]]
dysprosium_2030_target_price_min = RIR_price_target_EU['Min'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[1]]
dysprosium_2050_target_price_min = RIR_price_target_EU['Min'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[2]]
dysprosium_2100_target_price_min = RIR_price_target_EU['Min'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[-1]]

dysprosium_2011_target_price_max = RIR_price_target_EU['Max'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[0]]
dysprosium_2030_target_price_max = RIR_price_target_EU['Max'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[1]]
dysprosium_2050_target_price_max = RIR_price_target_EU['Max'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[2]]
dysprosium_2100_target_price_max = RIR_price_target_EU['Max'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[-1]]


dysprosium_2011_full_price_min = RIR_price_full_EU['Min'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[0]]
dysprosium_2030_full_price_min = RIR_price_full_EU['Min'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[1]]
dysprosium_2050_full_price_min = RIR_price_full_EU['Min'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[2]]
dysprosium_2100_full_price_min = RIR_price_full_EU['Min'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[-1]]

dysprosium_2011_full_price_max = RIR_price_full_EU['Max'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[0]]
dysprosium_2030_full_price_max = RIR_price_full_EU['Max'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[1]]
dysprosium_2050_full_price_max = RIR_price_full_EU['Max'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[2]]
dysprosium_2100_full_price_max = RIR_price_full_EU['Max'].loc[['Dysprosium'], RIR_price_hist_EU['Min'].columns[-1]]


dysprosium_RIR_EU_hist_2011 = RIR_EU['hist'].loc['Dysprosium', 2011]
dysprosium_RIR_EU_hist_2030 = RIR_EU['hist'].loc['Dysprosium', 2030]
dysprosium_RIR_EU_hist_2050 = RIR_EU['hist'].loc['Dysprosium', 2050]
dysprosium_RIR_EU_hist_2100 = RIR_EU['hist'].loc['Dysprosium', 2100]

dysprosium_RIR_EU_target_2011 = RIR_EU['target'].loc['Dysprosium', 2011]
dysprosium_RIR_EU_target_2030 = RIR_EU['target'].loc['Dysprosium', 2030]
dysprosium_RIR_EU_target_2050 = RIR_EU['target'].loc['Dysprosium', 2050]
dysprosium_RIR_EU_target_2100 = RIR_EU['target'].loc['Dysprosium', 2100]

dysprosium_RIR_EU_full_2011 = RIR_EU['full'].loc['Dysprosium', 2011]
dysprosium_RIR_EU_full_2030 = RIR_EU['full'].loc['Dysprosium', 2030]
dysprosium_RIR_EU_full_2050 = RIR_EU['full'].loc['Dysprosium', 2050]
dysprosium_RIR_EU_full_2100 = RIR_EU['full'].loc['Dysprosium', 2100]


min_price_Dy = {}
max_price_Dy = {}
metal = 'Dysprosium'

for sensitivity in sensitivities:
    min_price_Dy[sensitivity] = pd.DataFrame(0, index = ['Dysprosium'],columns=[2011,2020,2050,2100])
    max_price_Dy[sensitivity] = pd.DataFrame(0, index = ['Dysprosium'],columns=[2011,2020,2050,2100])


min_price_Dy['full'] = RIR_price_full_EU['Min'].loc[['Dysprosium'], :]
min_price_Dy['target'] = RIR_price_target_EU['Min'].loc[['Dysprosium'], :]
min_price_Dy['hist'] = RIR_price_hist_EU['Min'].loc[['Dysprosium'], :]
max_price_Dy['full'] = RIR_price_full_EU['Max'].loc[['Dysprosium'], :]
max_price_Dy['target'] = RIR_price_target_EU['Max'].loc[['Dysprosium'], :]
max_price_Dy['hist'] = RIR_price_hist_EU['Max'].loc[['Dysprosium'], :]

# Example access: min_price_data['hist'][2011]['dysprosium_2011_hist_price_min']
# Example access: max_price_data['hist'][2011]['dysprosium_2011_hist_price_max']


for i, sensitivity in enumerate(colors.keys()):
    # Barre cumulative per ogni metallo
    bottom = np.zeros_like(years_elected, dtype=float)

    # Barre non trasparenti
    bars = ax.bar(positions + i * bar_width, RIR_EU[sensitivity].loc[metal, years_elected], width=bar_width, label=f'{sensitivity.capitalize()} - {metal}', color=colors[sensitivity], alpha=0.8)

    # Aggiungi etichette sui dati non trasparenti se il valore è diverso da zero
    for bar in bars:
        yval = bar.get_height()
        # Formatta il testo dell'etichetta
        if yval == 0.0 or (0 < yval < 0.01):
            label_text = '0'
        else:
            label_text = '{:.2f}'.format(yval)
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.01, label_text, ha='center', va='bottom', fontsize='x-large')

    # Aggiungi la banda di errore con ax.errorbar
    
    x_positions = positions + i * bar_width
    
    # Access the specific sensitivity and year in the error bar section
    ax.errorbar(x_positions, RIR_EU[sensitivity].loc[metal, years_elected], yerr=[RIR_EU[sensitivity].loc[metal, years_elected] - max_price_Dy[sensitivity].loc['Dysprosium', years_elected],min_price_Dy[sensitivity].loc['Dysprosium', years_elected] - RIR_EU[sensitivity].loc['Dysprosium', years_elected]  ], fmt='_', color=colors[sensitivity], capsize=5, label='Error Band')

# Aggiungi etichette e legenda
ax.set_xlabel('Year', fontsize='xx-large')
ax.set_ylabel('Percentage (%)', fontsize='xx-large')
ax.set_title(f'Percentage Distribution of RIR for {metal} Over Time', fontsize=20)
ax.set_xticks(positions + bar_width)
ax.set_xticklabels(years_elected)
ax.legend(fontsize='xx-large', loc = 'upper left')

ax.tick_params(axis='both', labelsize='xx-large')
# Aggiungi una griglia
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Mostra il grafico
plt.show()



#%% RIR for Neodymium
# Definizione delle dimensioni del grafico
fig, ax = plt.subplots(figsize=(16, 10))

# Anni selezionati
years_elected = [2011, 2030, 2050, 2100]

# Larghezza delle barre
bar_width = 0.2

# Posizioni delle barre per ogni anno
positions = np.arange(len(years_elected))

# Colori per ogni sensibilità
colors = {'hist': '#95a5a6', 'target': '#e74c3c', 'full': '#3498db'}

# Metallo selezionato
metal = 'Neodymium'

min_price_Nd = {}
max_price_Nd = {}

for sensitivity in sensitivities:
    min_price_Nd[sensitivity] = pd.DataFrame(0, index = ['Neodymium'],columns=[2011,2020,2050,2100])
    max_price_Nd[sensitivity] = pd.DataFrame(0, index = ['Neodymium'],columns=[2011,2020,2050,2100])


min_price_Nd['full'] = RIR_price_full_EU['Min'].loc[['Neodymium'], :]
min_price_Nd['target'] = RIR_price_target_EU['Min'].loc[['Neodymium'], :]
min_price_Nd['hist'] = RIR_price_hist_EU['Min'].loc[['Neodymium'], :]
max_price_Nd['full'] = RIR_price_full_EU['Max'].loc[['Neodymium'], :]
max_price_Nd['target'] = RIR_price_target_EU['Max'].loc[['Neodymium'], :]
max_price_Nd['hist'] = RIR_price_hist_EU['Max'].loc[['Neodymium'], :]

for i, sensitivity in enumerate(colors.keys()):
    # Barre cumulative per ogni metallo
    bottom = np.zeros_like(years_elected, dtype=float)

    # Barre trasparenti
    ax.bar(positions + i * bar_width, 1, label=f'{sensitivity.capitalize()} - {metal}', bottom=bottom, color=colors[sensitivity], alpha=0.2, width=bar_width)

    # Barre non trasparenti
    bars = ax.bar(positions + i * bar_width, RIR_EU[sensitivity].loc[metal, years_elected], width=bar_width, label=f'{sensitivity.capitalize()} - {metal}', color=colors[sensitivity], alpha=0.8)

    # Aggiungi etichette sui dati non trasparenti se il valore è diverso da zero
    for bar in bars:
        yval = bar.get_height()
        # Formatta il testo dell'etichetta
        if yval == 0.0 or (0 < yval < 0.01):
            label_text = '0'
        else:
            label_text = '{:.2f}'.format(yval)
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.01, label_text, ha='center', va='bottom', fontsize='x-large')
     
    x_positions = positions + i * bar_width
     
     # Access the specific sensitivity and year in the error bar section
    ax.errorbar(x_positions, RIR_EU[sensitivity].loc[metal, years_elected], yerr=[RIR_EU[sensitivity].loc[metal, years_elected] - max_price_Nd[sensitivity].loc[metal, years_elected],min_price_Nd[sensitivity].loc[metal, years_elected] - RIR_EU[sensitivity].loc[metal, years_elected]  ], fmt='_', color=colors[sensitivity], capsize=5, label='Error Band')

# Aggiungi etichette e legenda
ax.set_xlabel('Year', fontsize='xx-large')
ax.set_ylabel('Percentage (%)', fontsize='xx-large')
ax.set_title(f'Percentage Distribution of RIR for {metal} Over Time', fontsize=20)
ax.set_xticks(positions + bar_width)
ax.set_xticklabels(years_elected)
ax.legend(fontsize='xx-large', loc = 'upper left')

ax.tick_params(axis='both', labelsize='xx-large')
# Aggiungi una griglia
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Mostra il grafico
plt.show()

#%% RIR for Copper
# Definizione delle dimensioni del grafico
fig, ax = plt.subplots(figsize=(16, 10))

# Anni selezionati
years_elected = [2011, 2030, 2050, 2100]

# Larghezza delle barre
bar_width = 0.2

# Posizioni delle barre per ogni anno
positions = np.arange(len(years_elected))

# Colori per ogni sensibilità
colors = {'hist': '#2ecc71', 'target': '#e74c3c', 'full': '#3498db'}

# Metallo selezionato
metal = 'Copper'
min_price_Cu = {}
max_price_Cu = {}

for sensitivity in sensitivities:
    min_price_Cu[sensitivity] = pd.DataFrame(0, index = ['Copper'],columns=[2011,2020,2050,2100])
    max_price_Cu[sensitivity] = pd.DataFrame(0, index = ['Copper'],columns=[2011,2020,2050,2100])


min_price_Cu['full'] = RIR_price_full_EU['Min'].loc[['Copper'], :]
min_price_Cu['target'] = RIR_price_target_EU['Min'].loc[['Copper'], :]
min_price_Cu['hist'] = RIR_price_hist_EU['Min'].loc[['Copper'], :]
max_price_Cu['full'] = RIR_price_full_EU['Max'].loc[['Copper'], :]
max_price_Cu['target'] = RIR_price_target_EU['Max'].loc[['Copper'], :]
max_price_Cu['hist'] = RIR_price_hist_EU['Max'].loc[['Copper'], :]

for i, sensitivity in enumerate(colors.keys()):
    # Barre cumulative per ogni metallo
    bottom = np.zeros_like(years_elected, dtype=float)

    # Barre trasparenti
    ax.bar(positions + i * bar_width, 1, label=f'{sensitivity.capitalize()} - {metal}', bottom=bottom, color=colors[sensitivity], alpha=0.2, width=bar_width)

    # Barre non trasparenti
    bars = ax.bar(positions + i * bar_width, RIR_EU[sensitivity].loc[metal, years_elected], width=bar_width, label=f'{sensitivity.capitalize()} - {metal}', color=colors[sensitivity], alpha=0.8)

    # Aggiungi etichette sui dati non trasparenti se il valore è diverso da zero
    for bar in bars:
        yval = bar.get_height()
        # Formatta il testo dell'etichetta
        if yval == 0.0 or (0 < yval < 0.01):
            label_text = '0'
        else:
            label_text = '{:.2f}'.format(yval)
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.01, label_text, ha='center', va='bottom', fontsize='x-large')
    x_positions = positions + i * bar_width
      
      # Access the specific sensitivity and year in the error bar section
    ax.errorbar(x_positions, RIR_EU[sensitivity].loc[metal, years_elected], yerr=[RIR_EU[sensitivity].loc[metal, years_elected] - max_price_Cu[sensitivity].loc[metal, years_elected],min_price_Cu[sensitivity].loc[metal, years_elected] - RIR_EU[sensitivity].loc[metal, years_elected]  ], fmt='_', color=colors[sensitivity], capsize=5, label='Error Band')

# Aggiungi etichette e legenda
ax.set_xlabel('Year', fontsize='xx-large')
ax.set_ylabel('Percentage (%)', fontsize='xx-large')
ax.set_title(f'Percentage Distribution of RIR for {metal} Over Time', fontsize=20)
ax.set_xticks(positions + bar_width)
ax.set_xticklabels(years_elected)
ax.legend(fontsize='xx-large', loc = 'upper left')

ax.tick_params(axis='both', labelsize='xx-large')
# Aggiungi una griglia
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Mostra il grafico
plt.show()

#%% RIR for Raw silicon
# Definizione delle dimensioni del grafico
fig, ax = plt.subplots(figsize=(16, 10))

# Anni selezionati
years_elected = [2011, 2030, 2050, 2100]

# Larghezza delle barre
bar_width = 0.2

# Posizioni delle barre per ogni anno
positions = np.arange(len(years_elected))

# Colori per ogni sensibilità
colors = {'hist': '#95a5a6', 'target': '#e74c3c', 'full': '#3498db'}

# Metallo selezionato
metal = 'Raw silicon'
min_price_Si = {}
max_price_Si = {}

for sensitivity in sensitivities:
    min_price_Si[sensitivity] = pd.DataFrame(0, index = ['Raw silicon'],columns=[2011,2020,2050,2100])
    max_price_Si[sensitivity] = pd.DataFrame(0, index = ['Raw silicon'],columns=[2011,2020,2050,2100])


min_price_Si['full'] = RIR_price_full_EU['Min'].loc[['Raw silicon'], :]
min_price_Si['target'] = RIR_price_target_EU['Min'].loc[['Raw silicon'], :]
min_price_Si['hist'] = RIR_price_hist_EU['Min'].loc[['Raw silicon'], :]
max_price_Si['full'] = RIR_price_full_EU['Max'].loc[['Raw silicon'], :]
max_price_Si['target'] = RIR_price_target_EU['Max'].loc[['Raw silicon'], :]
max_price_Si['hist'] = RIR_price_hist_EU['Max'].loc[['Raw silicon'], :]

for i, sensitivity in enumerate(colors.keys()):
    # Barre cumulative per ogni metallo
    bottom = np.zeros_like(years_elected, dtype=float)

    # Barre trasparenti
    ax.bar(positions + i * bar_width, 1, label=f'{sensitivity.capitalize()} - {metal}', bottom=bottom, color=colors[sensitivity], alpha=0.2, width=bar_width)

    # Barre non trasparenti
    bars = ax.bar(positions + i * bar_width, RIR_EU[sensitivity].loc[metal, years_elected], width=bar_width, label=f'{sensitivity.capitalize()} - {metal}', color=colors[sensitivity], alpha=0.8)

    # Aggiungi etichette sui dati non trasparenti se il valore è diverso da zero
    for bar in bars:
        yval = bar.get_height()
        # Formatta il testo dell'etichetta
        if yval == 0.0 or (0 < yval < 0.01):
            label_text = '0'
        else:
            label_text = '{:.2f}'.format(yval)
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.01, label_text, ha='center', va='bottom', fontsize='x-large')
    x_positions = positions + i * bar_width
     
     # Access the specific sensitivity and year in the error bar section
    ax.errorbar(x_positions, RIR_EU[sensitivity].loc[metal, years_elected], yerr=[RIR_EU[sensitivity].loc[metal, years_elected] - max_price_Si[sensitivity].loc[metal, years_elected],min_price_Si[sensitivity].loc[metal, years_elected] - RIR_EU[sensitivity].loc[metal, years_elected]  ], fmt='_', color=colors[sensitivity], capsize=5, label='Error Band')

# Aggiungi etichette e legenda
ax.set_xlabel('Year', fontsize='xx-large')
ax.set_ylabel('Percentage (%)', fontsize='xx-large')
ax.set_title(f'Percentage Distribution of RIR for {metal} Over Time', fontsize=20)
ax.set_xticks(positions + bar_width)
ax.set_xticklabels(years_elected)
ax.legend(fontsize='xx-large', loc = 'upper left')

ax.tick_params(axis='both', labelsize='xx-large')
# Aggiungi una griglia
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Mostra il grafico
plt.show()

#%%

import matplotlib.pyplot as plt

# Define the overall plot size
fig, axs = plt.subplots(2, 2, figsize=(16, 12))

# List of metals
metals = ['Dysprosium', 'Neodymium', 'Copper', 'Raw silicon']
min_price = {}
max_price = {}

for sensitivity in sensitivities:
    min_price[sensitivity] = pd.DataFrame(0, index=[metals], columns=[2011, 2020, 2050, 2100])
    max_price[sensitivity] = pd.DataFrame(0, index=[metals], columns=[2011, 2020, 2050, 2100])

min_price['full'] = RIR_price_full_EU['Min'].loc[metals, :]
min_price['target'] = RIR_price_target_EU['Min'].loc[metals, :]
min_price['hist'] = RIR_price_hist_EU['Min'].loc[metals, :]
max_price['full'] = RIR_price_full_EU['Max'].loc[metals, :]
max_price['target'] = RIR_price_target_EU['Max'].loc[metals, :]
max_price['hist'] = RIR_price_hist_EU['Max'].loc[metals, :]

# Iterate through subplots and metals
for i, ax in enumerate(axs.flat):
    metal = metals[i]

    # Selected years
    years_elected = [2011, 2030, 2050, 2100]

    # Bar width
    bar_width = 0.3

    # Positions of the bars for each year
    positions = np.arange(len(years_elected))

    # Colors for each sensitivity
    colors = {'hist': '#239d58', 'target': '#ff6b81', 'full': '#3498db'}

    for j, sensitivity in enumerate(colors.keys()):
        # Cumulative bars for each metal
        bottom = np.zeros_like(years_elected, dtype=float)

        # Transparent bars
      #  ax.bar(positions + j * bar_width, 1, bottom=bottom, color=colors[sensitivity], alpha=0.2, width=bar_width)

        # Non-transparent bars
        bars = ax.bar(positions + j * bar_width, RIR_EU[sensitivity].loc[metal, years_elected], width=bar_width, label=f'{sensitivity.capitalize()} - {metal}', color=colors[sensitivity], alpha=0.8)

        # Add labels on non-transparent bars if the value is non-zero
        for bar in bars:
            yval = bar.get_height()
            # Format label text
            if yval == 0.0 or (0 < yval < 0.01):
                label_text = '0'
            else:
                label_text = '{:.2f}'.format(yval)
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.01, label_text, ha='center', va='bottom', fontsize='x-large')

        # Access the specific sensitivity and year in the error bar section
        x_positions = positions + j * bar_width
        ax.errorbar(x_positions, RIR_EU[sensitivity].loc[metal, years_elected],
                    yerr=[RIR_EU[sensitivity].loc[metal, years_elected] - max_price[sensitivity].loc[metal, years_elected],
                          min_price[sensitivity].loc[metal, years_elected] - RIR_EU[sensitivity].loc[metal, years_elected]],
                    fmt='_', color=colors[sensitivity], capsize=5, label='Error Band')

    # Add labels and legend
    ax.set_xlabel('Year', fontsize='xx-large')
    ax.set_ylabel('Percentage (%)', fontsize='xx-large')
    ax.set_title(f'RIR for {metal} Over Time', fontsize=20)
    ax.set_xticks(positions + bar_width)

    ax.legend(fontsize='xx-large', loc='upper left')

    ax.tick_params(axis='both', labelsize='xx-large')
    # Add a grid
    ax.grid(axis='y', linestyle='--', alpha=0.7)

# Adjust subplot layout
plt.tight_layout()

# Show the overall plot
plt.show()


#%%
