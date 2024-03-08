import pandas as pd
import matplotlib.pyplot as plt

# Load data for each element
file_path = 'C:\\Users\\carol\\OneDrive - Politecnico di Milano\\2022-23_WasteMARIO\\dMRWIO model\\dMRWIO\\Data Demand Growth.xlsx'

norec = pd.read_excel(file_path, "No rec", index_col=[0])
rec = pd.read_excel(file_path, "Rec", index_col=[0])

fig, axs = plt.subplots(1, 3, figsize=(16, 6.4), gridspec_kw={'wspace': 0.05},sharex=True, sharey=True)
axs = axs.flatten()
bar_width = 0.35  # Reducing bar_width to create space between bars

# Plot for REE
years = norec.columns


REE_norec = axs[0].bar(years - bar_width/2, norec.iloc[0, :], bar_width, label='REE (No rec)', color='#ff5c77', edgecolor='#ff5c77', alpha=0.9)
REE_rec = axs[0].bar(years + bar_width/2, rec.iloc[0, :], bar_width, label='REE (Rec)', color='#ffad88', edgecolor='#ffad88', alpha=0.9)

axs[0].set_xticks(years)  # Show only these years on x-axis
axs[0].set_xticklabels(['2030', '2050', '2100'], fontsize='xx-large')
axs[0].set_title('REEs', fontsize='xx-large')
axs[0].yaxis.grid(True, linestyle='--', alpha=0.7)
for ax in axs:
    ax.tick_params(axis='y', labelsize='xx-large')
    
for bar, value in zip(REE_norec, norec.iloc[0, :]):
    axs[0].text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{value:.2f}', ha='center', va='bottom', fontsize='x-large')

for bar, value in zip(REE_rec, rec.iloc[0, :]):
    axs[0].text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{value:.2f}', ha='center', va='bottom', fontsize='x-large')

# Plot for Copper
Cu_norec = axs[1].bar(years - bar_width/2, norec.iloc[1, :], bar_width, label='Cu (No rec)', color='#ff5c77', edgecolor='#ff5c77', alpha=0.9)
Cu_rec = axs[1].bar(years + bar_width/2, rec.iloc[1, :], bar_width, label='Cu (Rec)', color='#ffad88', edgecolor='#ffad88', alpha=0.9)

axs[1].set_xticks(years)  # Show only these years on x-axis
axs[1].set_xticklabels(['2030', '2050', '2100'], fontsize='xx-large')
axs[1].set_xlabel('Years', fontsize='xx-large')
axs[1].yaxis.grid(True, linestyle='--', alpha=0.7)

axs[1].set_title('Copper', fontsize='xx-large')
for bar, value in zip(Cu_norec, norec.iloc[1, :]):
    axs[1].text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{value:.2f}', ha='center', va='bottom', fontsize='x-large')

for bar, value in zip(Cu_rec, rec.iloc[1, :]):
    axs[1].text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{value:.2f}', ha='center', va='bottom', fontsize='x-large')

# Plot for Silicon
Si_norec = axs[2].bar(years - bar_width/2, norec.iloc[2, :], bar_width, label='Without recycling', color='#ff5c77', edgecolor='#ff5c77', alpha=0.9)
Si_rec = axs[2].bar(years + bar_width/2, rec.iloc[2, :], bar_width, label='With recycling', color='#ffad88', edgecolor='#ffad88', alpha=0.9)

axs[2].set_xticks(years)  # Show only these years on x-axis
axs[2].set_xticklabels(['2030', '2050', '2100'], fontsize='xx-large')
axs[2].yaxis.grid(True, linestyle='--', alpha=0.7)
axs[2].legend(fontsize = 'xx-large')
axs[2].set_title('Silicon', fontsize='xx-large')
for bar, value in zip(Si_norec, norec.iloc[2, :]):
    axs[2].text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{value:.2f}', ha='center', va='bottom', fontsize='x-large')

for bar, value in zip(Si_rec, rec.iloc[2, :]):
    axs[2].text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{value:.2f}', ha='center', va='bottom', fontsize='x-large')
plt.tight_layout()

fig = plt.gcf()

# Impostare una risoluzione elevata (dpi) per una migliore qualità
dpi = 300

# Esportare come PNG con alta risoluzione
fig.savefig('annual prod growth.png', dpi=dpi, bbox_inches='tight')

plt.show()
