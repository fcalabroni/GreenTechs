import matplotlib.pyplot as plt
import pandas as pd 
from matplotlib.gridspec import GridSpec
import numpy as np

user = 'CF'
paths = 'Paths.xlsx'


#%%
sens = ['hist', 'target', 'full']
met = ['Dysprosium','Neodymium','Copper','Raw silicon']
RIR = {}

for s in sens:
    RIR[s] = {}
    for m in met:
        RIR[s][m] = {}
            
for s in sens:
    for m in met:
        fileResults = f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Baseline\\EoL-RIR\\EoL-RIR_base_{s}.xlsx"
        RIR[s][m] =  pd.read_excel(fileResults, f"{m}", index_col=[0])
        
#%%
years = range(2011,2101)
RIR_EU = {}
for s in sens:
    RIR_EU[s] = pd.DataFrame(0,index=met, columns=years)
    
for s in sens:
    for m in met:
        RIR_EU[s].loc[m,years] = RIR[s][m].loc['EU27+UK',:]
        
#%% RIR dy
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
metal = 'Dysprosium'

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

# Definizione delle dimensioni del grafico complessivo
fig, axs = plt.subplots(2, 2, figsize=(16, 12))

# Lista dei metalli
metals = ['Dysprosium', 'Neodymium', 'Copper', 'Raw silicon']

# Itera attraverso i sottografi e i metalli
for i, ax in enumerate(axs.flat):
    metal = metals[i]

    # Anni selezionati
    years_elected = [2011, 2030, 2050, 2100]

    # Larghezza delle barre
    bar_width = 0.3

    # Posizioni delle barre per ogni anno
    positions = np.arange(len(years_elected))
    # Colori per ogni sensibilità
    colors = {'hist': '#239d58', 'target': '#ff6b81', 'full': '#3498db'}
    for j, sensitivity in enumerate(colors.keys()):
        # Barre cumulative per ogni metallo
        bottom = np.zeros_like(years_elected, dtype=float)
        # Barre trasparenti
        ax.bar(positions + j * bar_width, 1, bottom=bottom, color=colors[sensitivity], alpha=0.2, width=bar_width)

        # Barre non trasparenti
        bars = ax.bar(positions + j * bar_width, RIR_EU[sensitivity].loc[metal, years_elected], width=bar_width, label=f'{sensitivity.capitalize()} - {metal}', color=colors[sensitivity], alpha=0.8)

        # Aggiungi etichette sui dati non trasparenti se il valore è diverso da zero
        for bar in bars:
            yval = bar.get_height()
            # Formatta il testo dell'etichetta
            if yval == 0.0 or (0 < yval < 0.01):
                label_text = '0'
            else:
                label_text = '{:.2f}'.format(yval)
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.01, label_text, ha='center', va='bottom', fontsize='x-large')

    # Aggiungi etichette e legenda
    ax.set_xlabel('Year', fontsize='xx-large')
    ax.set_ylabel('Percentage (%)', fontsize='xx-large')
    ax.set_title(f'RIR for {metal} Over Time', fontsize=20)
    ax.set_xticks(positions + bar_width)
    
    ax.legend(fontsize='xx-large', loc='upper left')

    ax.tick_params(axis='both', labelsize='xx-large')
    # Aggiungi una griglia
    ax.grid(axis='y', linestyle='--', alpha=0.7)

# Aggiusta la disposizione dei sottografi
plt.tight_layout()

# Mostra il grafico complessivo
plt.show()
