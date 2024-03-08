# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.patches import Arrow

# user = 'CF'
# paths = 'Paths.xlsx'

# file_path = f"{pd.read_excel(paths, index_col=[0]).loc['Results', user]}\\Emissions\\RR\\Cumulative_Emission_target.xlsx"

# total = pd.read_excel(file_path, "Total", index_col=[0])
# effective = pd.read_excel(file_path, "Effective", index_col=[0])
# avoided = pd.read_excel(file_path, "Avoided", index_col=[0])
# primary = pd.read_excel(file_path, "Primary", index_col=[0])
# secondary = pd.read_excel(file_path, "Secondary", index_col=[0])

# total = total.loc[:, [2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]]
# effective = effective.loc[:, [2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]]
# avoided = avoided.loc[:, [2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]]
# primary = primary.loc[:, [2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]]
# secondary = secondary.loc[:, [2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]]

# total.columns = [1,2,3,4,5,6,7,8,9,10]
# effective.columns = [1,2,3,4,5,6,7,8,9,10]
# primary.columns = [1,2,3,4,5,6,7,8,9,10]
# secondary.columns = [1,2,3,4,5,6,7,8,9,10]

# fig, axs = plt.subplots(2, 2, figsize=(20, 11), sharex=True)
# bar_width = 0.45

# # Flatten the axs array
# axs = axs.flatten()

# years = effective.columns

# # Define color palette
# colors = ['#f36a6d', '#f1596e', '#ffd166', '#ff9f1c']

# # Plot data for each subplot
# for i, ax in enumerate(axs):
#     ax.bar(years - bar_width/2, total.iloc[i, :], bar_width, label='Total', color=colors[0], edgecolor=colors[0], alpha=0.9)
#     ax.bar(years - bar_width/2, effective.iloc[i, :], bar_width, label='Effective', color=colors[1], edgecolor=colors[1], alpha=0.9)
#     ax.bar(years + bar_width/2, primary.iloc[i, :], bar_width, label='Primary', color=colors[2], edgecolor=colors[2], alpha=0.9)
#     ax.bar(years + bar_width/2, secondary.iloc[i, :], bar_width, label='Secondary', color=colors[3], edgecolor=colors[3], alpha=0.9, bottom=primary.iloc[i, :])

#     ax.set_xticks(years)
#     ax.set_xticklabels(['2011', '2020', '2030', '2040', '2050', '2060', '2070', '2080', '2090', '2100'], fontsize='xx-large')
#     ax.xaxis.grid(True, linestyle='-', linewidth=0.5, alpha=0.7)
#     ax.yaxis.grid(True, linestyle='-', linewidth=0.5, alpha=0.7)
#     ax.set_title(['Nd', 'Dy', 'Cu', 'Si'][i], fontsize='xx-large')
#     ax.tick_params(axis='y', labelsize='xx-large')  # Increase y-axis label font size
#     ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0), useMathText=True)

# axs[2].set_xlabel('Years', fontsize='xx-large')
# axs[3].set_xlabel('Years', fontsize='xx-large')

# # Adjust layout and show plot
# plt.subplots_adjust(wspace=0.075, hspace = 0.125)
# #plt.tight_layout()
# plt.show()

#%%
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerPatch
from matplotlib.patches import Rectangle
from matplotlib.patches import Ellipse, Polygon

user = 'CF'
paths = 'Paths.xlsx'

file_path = f"{pd.read_excel(paths, index_col=[0]).loc['Results', user]}\\Emissions\\RR\\Cumulative_Emission_target.xlsx"

total = pd.read_excel(file_path, "Total", index_col=[0])
effective = pd.read_excel(file_path, "Effective", index_col=[0])
primary = pd.read_excel(file_path, "Primary", index_col=[0])
secondary = pd.read_excel(file_path, "Secondary", index_col=[0])
avoided = pd.read_excel(file_path, "Avoided", index_col=[0])

total = total.loc[:, [2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]]
effective = effective.loc[:, [2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]]
primary = primary.loc[:, [2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]]
secondary = secondary.loc[:, [2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]]
avoided = avoided.loc[:, [2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]]

total.columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
effective.columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
primary.columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
secondary.columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
avoided.columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

fig, axs = plt.subplots(2, 2, figsize=(16, 9), sharex=True)
bar_width = 0.45

# Flatten the axs array
axs = axs.flatten()

years = effective.columns

# Define color palette
colors = ['#a5caa8', '#0d5e4a', '#4c956c']

# Plot data for each subplot
for i, ax in enumerate(axs):
    # Plot bars
    ax.bar(years, primary.iloc[i, :], bar_width, label='Primary', color=colors[1], edgecolor=colors[1], alpha=0.9)
    ax.bar(years, secondary.iloc[i, :], bar_width, label='Secondary', color=colors[2], edgecolor=colors[2], alpha=0.9, bottom=primary.iloc[i, :])
    ax.bar(years, avoided.iloc[i, :], bar_width, label='Avoided', color=colors[0], edgecolor='white', alpha=0.9, bottom=primary.iloc[i, :] + secondary.iloc[i, :], hatch='//')
    
    ax.plot(years, effective.iloc[i, :], linestyle='None', marker='D',  label='Effective', color='black', markersize=5)
    ax.plot(years, total.iloc[i, :], marker='x',  markerfacecolor='none', markeredgecolor='black', color='black', label='No recycling', linestyle='None', markersize=7)
    ax.set_xticks(years)
    ax.set_xticklabels(['2011', '2020', '2030', '2040', '2050', '2060', '2070', '2080', '2090', '2100'], fontsize='xx-large')
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_title(['Neodymium', 'Dysprosium', 'Copper', 'Silicon'][i], fontsize='xx-large')
    ax.tick_params(axis='y', labelsize='xx-large')  # Increase y-axis label font size
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0), useMathText=True)

    # Add labels on top of the bars with specified decimal places
 
# Add Y-axis labels with specified decimal places and unit
for ax in axs[:2]:
    ax.set_ylabel('ton', fontsize='xx-large')
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,.0f}".format(x)))

# Add Y-axis labels with specified decimal places and unit for the last two subplots
for ax in axs[2:]:
    ax.set_ylabel('ton', fontsize='xx-large')
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,.0f}".format(x)))

axs[0].legend(fontsize='xx-large', loc='upper left')
# Adjust layout and show plot
plt.subplots_adjust(wspace=0.075, hspace=0.125)
plt.tight_layout()

fig = plt.gcf()

# Impostare una risoluzione elevata (dpi) per una migliore qualità
dpi = 300

# Esportare come PNG con alta risoluzione
fig.savefig('emissioni.png', dpi=dpi, bbox_inches='tight')

plt.show()

