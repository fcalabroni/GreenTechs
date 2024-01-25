import matplotlib.pyplot as plt
import pandas as pd 
from matplotlib.gridspec import GridSpec

user = 'CF'
paths = 'Paths.xlsx'
#%%
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
#%%
# with plt.style.context('fivethirtyeight'):
#     fig, ax = plt.subplots(figsize=(12, 6))

#     for s, label, color in zip(sens, ['Full', 'Hist', 'Target'], ['blue', 'red', 'green']):
#         # Selezioniamo i dati dal 2011 al 2100
#         met_rec_data = met_rec_cumulative[s].loc['Neodymium', 2011:2100].values
#         years_subset = range(2011, 2101)
#         ax.bar(years_subset, met_rec_data, alpha=0.7, label=f'{label} Met Rec Cumulative', color=color, edgecolor='black')

#     # Adding labels, title, and legend
#     ax.legend(fontsize='xx-large')
#     ax.set_xlabel('Year', fontsize='xx-large')
#     ax.set_ylabel('Cumulative Metal Recovery', fontsize='xx-large')
#     ax.set_title('Cumulative Metal Recovery - Neodymium', fontsize='xx-large')

#     # Adding grid
#     ax.grid(True, linestyle='-', alpha=0.7)

#     # Inversione dell'asse y
#     ax.invert_yaxis()

#     plt.tight_layout()
#     plt.show()
    
#%% cumulative + met rec Nd
years_subset = range(2011, 2101)

with plt.style.context('default'):  # Utilizzo dello stile di base di Matplotlib
    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(2, 1, height_ratios=[3, 2], hspace=0.1)

    # Main plot with lines
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Neodymium'), :], label='Cumulative with Full RR', linestyle='-.', linewidth=3, markersize=8, color='limegreen')
    ax1.plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Neodymium'), :], label='Cumulative with Target RR', linestyle='-', linewidth=3, markersize=8, color='orangered')
    ax1.plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Neodymium'), :], label='Cumulative with Hist RR', linestyle='--', linewidth=3, markersize=8, color='deepskyblue')

    # Add labels, title, and legend
    # ax1.legend(fontsize='x-large')
    ax1.set_xlabel('Year', fontsize='x-large')
    ax1.set_title('Cumulative Neodymium and recycled metal', fontsize='xx-large')

    # Add grid
    ax1.yaxis.grid(True, linestyle='-', alpha=0.7)

    # Add a background color
    ax1.axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Neodymium'), :]), facecolor='#f2f2f2', alpha=0.2)
    ax1.tick_params(axis='both', which='major', labelsize='x-large')
    # Create the second y-axis (positive downward)
    ax2 = fig.add_subplot(gs[1])
    ax2.yaxis.grid(True,linestyle='-', alpha=0.7)
    # Add histogram for the 'Target' sensitivity to the second y-axis (positive downward) and invert the y-axis
    met_rec_data_target_Nd = met_rec_cumulative['target'].loc['Neodymium', 2011:2100].values
    met_rec_data_full_Nd = met_rec_cumulative['full'].loc['Neodymium', 2011:2100].values
    met_rec_data_hist_Nd = met_rec_cumulative['hist'].loc['Neodymium', 2011:2100].values

    # Add histogram for the 'Target' sensitivity to the second y-axis (positive downward) and invert the y-axis
    ax2.bar(years_subset, met_rec_data_full_Nd, alpha=0.7, label='Full Met Rec Cumulative', color='limegreen', edgecolor='limegreen')
    ax2.bar(years_subset, met_rec_data_target_Nd, alpha=0.7, label='Target Met Rec Cumulative', color='orangered', edgecolor='orangered')
    ax2.bar(years_subset, met_rec_data_hist_Nd, alpha=0.7, label='Hist Met Rec Cumulative', color='deepskyblue', edgecolor='deepskyblue')

    ax2.invert_yaxis()

    # Set the y-axis tick labels to be the same size in both subplots
    ax1.tick_params(axis='y', labelsize='x-large')
    ax2.tick_params(axis='y', labelsize='x-large')
    ax2.set_xticks([]) 
    # Add a single legend for both subplots
    handles, labels = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles += handles2
    labels += labels2
    ax2.legend(handles, labels, fontsize='x-large', loc='lower left')

    plt.tight_layout()
    plt.show()
#%% cumulative + met rec Dy
with plt.style.context('default'):  # Utilizzo dello stile di base di Matplotlib
    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(2, 1, height_ratios=[3, 2], hspace=0.1)

    # Main plot with lines
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Dysprosium'), :], label='Cumulative with Full RR', linestyle='-.', linewidth=3, markersize=8, color='limegreen')
    ax1.plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Dysprosium'), :], label='Cumulative with Target RR', linestyle='-', linewidth=3, markersize=8, color='orangered')
    ax1.plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Dysprosium'), :], label='Cumulative with Hist RR', linestyle='--', linewidth=3, markersize=8, color='deepskyblue')

    # Add labels, title, and legend
    # ax1.legend(fontsize='x-large')
    ax1.set_xlabel('Year', fontsize='x-large')
    ax1.set_title('Cumulative Dysprosium and recycled metal', fontsize='xx-large')

    # Add grid
    ax1.yaxis.grid(True, linestyle='-', alpha=0.7)

    # Add a background color
    ax1.axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Dysprosium'), :]), facecolor='#f2f2f2', alpha=0.2)
    ax1.tick_params(axis='both', which='major', labelsize='x-large')
    # Create the second y-axis (positive downward)
    ax2 = fig.add_subplot(gs[1])
    ax2.yaxis.grid(True,linestyle='-', alpha=0.7)
    # Add histogram for the 'Target' sensitivity to the second y-axis (positive downward) and invert the y-axis
    met_rec_data_target_Dy = met_rec_cumulative['target'].loc['Dysprosium', 2011:2100].values
    met_rec_data_full_Dy = met_rec_cumulative['full'].loc['Dysprosium', 2011:2100].values
    met_rec_data_hist_Dy = met_rec_cumulative['hist'].loc['Dysprosium', 2011:2100].values

    # Add histogram for the 'Target' sensitivity to the second y-axis (positive downward) and invert the y-axis
    ax2.bar(years_subset, met_rec_data_full_Dy, alpha=0.7, label='Full Met Rec Cumulative', color='limegreen', edgecolor='limegreen')
    ax2.bar(years_subset, met_rec_data_target_Dy, alpha=0.7, label='Target Met Rec Cumulative', color='orangered', edgecolor='orangered')
    ax2.bar(years_subset, met_rec_data_hist_Dy, alpha=0.7, label='Hist Met Rec Cumulative', color='deepskyblue', edgecolor='deepskyblue')

    ax2.invert_yaxis()

    # Set the y-axis tick labels to be the same size in both subplots
    ax1.tick_params(axis='y', labelsize='x-large')
    ax2.tick_params(axis='y', labelsize='x-large')
    ax2.set_xticks([]) 
    # Add a single legend for both subplots
    handles, labels = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles += handles2
    labels += labels2
    ax2.legend(handles, labels, fontsize='x-large', loc='lower left')
  
    plt.tight_layout()
    plt.show()
    
#%% cumulative + met rec Cu
with plt.style.context('default'):  # Utilizzo dello stile di base di Matplotlib
    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(2, 1, height_ratios=[3, 2], hspace=0.1)

    # Main plot with lines
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Copper'), :], label='Cumulative with Full RR', linestyle='-.', linewidth=3, markersize=8, color='limegreen')
    ax1.plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Copper'), :], label='Cumulative with Target RR', linestyle='-', linewidth=3, markersize=8, color='orangered')
    ax1.plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Copper'), :], label='Cumulative with Hist RR', linestyle='--', linewidth=3, markersize=8, color='deepskyblue')

    # Add labels, title, and legend
    # ax1.legend(fontsize='x-large')
    ax1.set_xlabel('Year', fontsize='x-large')
    ax1.set_title('Cumulative Copper and recycled metal', fontsize='xx-large')

    # Add grid
    ax1.yaxis.grid(True, linestyle='-', alpha=0.7)

    # Add a background color
    ax1.axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Copper'), :]), facecolor='#f2f2f2', alpha=0.2)
    ax1.tick_params(axis='both', which='major', labelsize='x-large')
    # Create the second y-axis (positive downward)
    ax2 = fig.add_subplot(gs[1])
    ax2.yaxis.grid(True,linestyle='-', alpha=0.7)
    # Add histogram for the 'Target' sensitivity to the second y-axis (positive downward) and invert the y-axis
    met_rec_data_target_Cu = met_rec_cumulative['target'].loc['Copper', 2011:2100].values
    met_rec_data_full_Cu = met_rec_cumulative['full'].loc['Copper', 2011:2100].values
    met_rec_data_hist_Cu = met_rec_cumulative['hist'].loc['Copper', 2011:2100].values

    # Add histogram for the 'Target' sensitivity to the second y-axis (positive downward) and invert the y-axis
    ax2.bar(years_subset, met_rec_data_full_Cu, alpha=0.7, label='Full Met Rec Cumulative', color='limegreen', edgecolor='limegreen')
    ax2.bar(years_subset, met_rec_data_target_Cu, alpha=0.7, label='Target Met Rec Cumulative', color='orangered', edgecolor='orangered')
    ax2.bar(years_subset, met_rec_data_hist_Cu, alpha=0.7, label='Hist Met Rec Cumulative', color='deepskyblue', edgecolor='deepskyblue')

    ax2.invert_yaxis()

    # Set the y-axis tick labels to be the same size in both subplots
    ax1.tick_params(axis='y', labelsize='x-large')
    ax2.tick_params(axis='y', labelsize='x-large')
    ax2.set_xticks([]) 
    # Add a single legend for both subplots
    handles, labels = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles += handles2
    labels += labels2
    ax2.legend(handles, labels, fontsize='x-large', loc='lower left')

    plt.tight_layout()
    plt.show()

#%% cumulative + met rec Si
with plt.style.context('default'):  # Utilizzo dello stile di base di Matplotlib
    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(2, 1, height_ratios=[3, 2], hspace=0.1)

    # Main plot with lines
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Raw silicon'), :], label='Cumulative with Full RR', linestyle='-.', linewidth=3, markersize=8, color='limegreen')
    ax1.plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Raw silicon'), :], label='Cumulative with Target RR', linestyle='-', linewidth=3, markersize=8, color='orangered')
    ax1.plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Raw silicon'), :], label='Cumulative with Hist RR', linestyle='--', linewidth=3, markersize=8, color='deepskyblue')

    # Add labels, title, and legend
    # ax1.legend(fontsize='x-large')
    ax1.set_xlabel('Year', fontsize='x-large')
    ax1.set_title('Cumulative Raw silicon and recycled metal', fontsize='xx-large')

    # Add grid
    ax1.yaxis.grid(True, linestyle='-', alpha=0.7)

    # Add a background color
    ax1.axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Raw silicon'), :]), facecolor='#f2f2f2', alpha=0.2)
    ax1.tick_params(axis='both', which='major', labelsize='x-large')
    # Create the second y-axis (positive downward)
    ax2 = fig.add_subplot(gs[1])
    ax2.yaxis.grid(True,linestyle='-', alpha=0.7)
    # Add histogram for the 'Target' sensitivity to the second y-axis (positive downward) and invert the y-axis
    met_rec_data_target_Si = met_rec_cumulative['target'].loc['Raw silicon', 2011:2100].values
    met_rec_data_full_Si = met_rec_cumulative['full'].loc['Raw silicon', 2011:2100].values
    met_rec_data_hist_Si = met_rec_cumulative['hist'].loc['Raw silicon', 2011:2100].values

    # Add histogram for the 'Target' sensitivity to the second y-axis (positive downward) and invert the y-axis
    ax2.bar(years_subset, met_rec_data_full_Si, alpha=0.7, label='Full Met Rec Cumulative', color='limegreen', edgecolor='limegreen')
    ax2.bar(years_subset, met_rec_data_target_Si, alpha=0.7, label='Target Met Rec Cumulative', color='orangered', edgecolor='orangered')
    ax2.bar(years_subset, met_rec_data_hist_Si, alpha=0.7, label='Hist Met Rec Cumulative', color='deepskyblue', edgecolor='deepskyblue')

    ax2.invert_yaxis()

    # Set the y-axis tick labels to be the same size in both subplots
    ax1.tick_params(axis='y', labelsize='x-large')
    ax2.tick_params(axis='y', labelsize='x-large')
    ax2.set_xticks([]) 
    # Add a single legend for both subplots
    handles, labels = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles += handles2
    labels += labels2
    ax2.legend(handles, labels, fontsize='x-large', loc='lower left')

    plt.tight_layout()
    plt.show()

#%%

#%%  Unione plot
# with plt.style.context('default'):  # Utilizzo dello stile di base di Matplotlib
#     fig, axs = plt.subplots(4, 2, figsize=(30, 25),gridspec_kw={'height_ratios': [3, 2, 3, 2], 'hspace': 0.3})

#     # Plot per Neodymium
#     axs[0, 0].plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Neodymium'), :], label='Full RR', linestyle='-.', linewidth=3, markersize=8, color='limegreen')
#     axs[0, 0].plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Neodymium'), :], label='Target RR', linestyle='-', linewidth=3, markersize=8, color='orangered')
#     axs[0, 0].plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Neodymium'), :], label='Hist RR', linestyle='--', linewidth=3, markersize=8, color='deepskyblue')
#     axs[0, 0].set_xlabel('Year', fontsize='x-large')
#     axs[0, 0].set_title('Neodymium', fontsize='xx-large')
#     axs[0, 0].yaxis.grid(True, linestyle='-', alpha=0.7)
#     axs[0, 0].axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Neodymium'), :]), facecolor='#f2f2f2', alpha=0.2)
#     axs[0, 0].tick_params(axis='both', which='major', labelsize='x-large')

#     # Plot per il grafico dell'istogramma di Neodymium
#     axs[1, 0].bar(years_subset, met_rec_data_full_Nd, alpha=0.7, label='Full Met Rec Cumulative', color='limegreen', edgecolor='limegreen')
#     axs[1, 0].bar(years_subset, met_rec_data_target_Nd, alpha=0.7, label='Target Met Rec Cumulative', color='orangered', edgecolor='orangered')
#     axs[1, 0].bar(years_subset, met_rec_data_hist_Nd, alpha=0.7, label='Hist Met Rec Cumulative', color='deepskyblue', edgecolor='deepskyblue')
#     axs[1, 0].invert_yaxis()
#     axs[1, 0].tick_params(axis='y', labelsize='x-large')
#     axs[1, 0].set_xticks([])

#     # Plot per Dysprosium
#     axs[0, 1].plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Dysprosium'), :], label='Full RR', linestyle='-.', linewidth=3, markersize=8, color='limegreen')
#     axs[0, 1].plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Dysprosium'), :], label='Target RR', linestyle='-', linewidth=3, markersize=8, color='orangered')
#     axs[0, 1].plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Dysprosium'), :], label='Hist RR', linestyle='--', linewidth=3, markersize=8, color='deepskyblue')
#     axs[0, 1].set_xlabel('Year', fontsize='x-large')
#     axs[0, 1].set_title('Dysprosium', fontsize='xx-large')
#     axs[0, 1].yaxis.grid(True, linestyle='-', alpha=0.7)
#     axs[0, 1].axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Dysprosium'), :]), facecolor='#f2f2f2', alpha=0.2)
#     axs[0, 1].tick_params(axis='both', which='major', labelsize='x-large')

#     # Plot per il grafico dell'istogramma di Dysprosium
#     axs[1, 1].bar(years_subset, met_rec_data_full_Dy, alpha=0.7, label='Full Met Rec Cumulative', color='limegreen', edgecolor='limegreen')
#     axs[1, 1].bar(years_subset, met_rec_data_target_Dy, alpha=0.7, label='Target Met Rec Cumulative', color='orangered', edgecolor='orangered')
#     axs[1, 1].bar(years_subset, met_rec_data_hist_Dy, alpha=0.7, label='Hist Met Rec Cumulative', color='deepskyblue', edgecolor='deepskyblue')
#     axs[1, 1].invert_yaxis()
#     axs[1, 1].tick_params(axis='y', labelsize='x-large')
#     axs[1, 1].set_xticks([])

#     # Plot per Copper
#     axs[2, 0].plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Copper'), :], label='Full RR', linestyle='-.', linewidth=3, markersize=8, color='limegreen')
#     axs[2, 0].plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Copper'), :], label='Target RR', linestyle='-', linewidth=3, markersize=8, color='orangered')
#     axs[2, 0].plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Copper'), :], label='Hist RR', linestyle='--', linewidth=3, markersize=8, color='deepskyblue')
#     axs[2, 0].set_xlabel('Year', fontsize='x-large')
#     axs[2, 0].set_title('Copper', fontsize='xx-large')
#     axs[2, 0].yaxis.grid(True, linestyle='-', alpha=0.7)
#     axs[2, 0].axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Copper'), :]), facecolor='#f2f2f2', alpha=0.2)
#     axs[2, 0].tick_params(axis='both', which='major', labelsize='x-large')

#     # Plot per il grafico dell'istogramma di Copper
#     axs[3,0].bar(years_subset, met_rec_data_full_Cu, alpha=0.7, label='Full Met Rec Cumulative', color='limegreen', edgecolor='limegreen')
#     axs[3,0].bar(years_subset, met_rec_data_target_Cu, alpha=0.7, label='Target Met Rec Cumulative', color='orangered', edgecolor='orangered')
#     axs[3,0].bar(years_subset, met_rec_data_hist_Cu, alpha=0.7, label='Hist Met Rec Cumulative', color='deepskyblue', edgecolor='deepskyblue')
#     axs[3,0].invert_yaxis()
#     axs[3,0].tick_params(axis='y', labelsize='x-large')
#     axs[3,0].set_xticks([])

#     # Plot per Silicon
#     axs[2,1].plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Raw silicon'), :], label='Full RR', linestyle='-.', linewidth=3, markersize=8, color='limegreen')
#     axs[2,1].plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Raw silicon'), :], label='Target RR', linestyle='-', linewidth=3, markersize=8, color='orangered')
#     axs[2,1].plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Raw silicon'), :], label='Hist RR', linestyle='--', linewidth=3, markersize=8, color='deepskyblue')
#     axs[2,1].set_xlabel('Year', fontsize='x-large')
#     axs[2,1].set_title('Raw silicon', fontsize='xx-large')
#     axs[2,1].yaxis.grid(True, linestyle='-', alpha=0.7)
#     axs[2,1].axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Raw silicon'), :]), facecolor='#f2f2f2', alpha=0.2)
#     axs[2,1].tick_params(axis='both', which='major', labelsize='x-large')

#     # Plot per il grafico dell'istogramma di Silicon
#     axs[3,1].bar(years_subset, met_rec_data_full_Si, alpha=0.7, label='Full Met Rec Cumulative', color='limegreen', edgecolor='limegreen')
#     axs[3,1].bar(years_subset, met_rec_data_target_Si, alpha=0.7, label='Target Met Rec Cumulative', color='orangered', edgecolor='orangered')
#     axs[3,1].bar(years_subset, met_rec_data_hist_Si, alpha=0.7, label='Hist Met Rec Cumulative', color='deepskyblue', edgecolor='deepskyblue')
#     axs[3,1].invert_yaxis()
#     axs[3,1].tick_params(axis='y', labelsize='x-large')
#     axs[3,1].set_xticks([])

#     # Aggiungi una singola legenda per tutti i sottoplot
#     handles, labels = axs[0, 0].get_legend_handles_labels()
#     axs[1, 0].legend(handles, labels, fontsize='x-large', loc='lower left')
#     plt.subplots_adjust(hspace=[0.1, 15, 0.1, 0.1])  # Regola il secondo valore (0.3) per aumentare o diminuire la distanza tra la seconda e la terza riga
#     ax2.yaxis.grid(True,linestyle='-', alpha=0.7)

#     plt.tight_layout()
#     plt.show()

#    ATTENZIONE CHE E' DIVISO PER 1E6!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from matplotlib.ticker import FuncFormatter

with plt.style.context('default'):  # Utilizzo dello stile di base di Matplotlib
    fig, axs = plt.subplots(2, 4, figsize=(34, 15),gridspec_kw={'height_ratios': [2, 1], 'hspace': 0.1})

    # Plot per Neodymium
    axs[0, 0].plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Neodymium'), :], label='Full RR', linestyle='-.', linewidth=3, markersize=8, color='limegreen')
    axs[0, 0].plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Neodymium'), :], label='Target RR', linestyle='-', linewidth=3, markersize=8, color='orangered')
    axs[0, 0].plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Neodymium'), :], label='Hist RR', linestyle='--', linewidth=3, markersize=8, color='deepskyblue')
   # axs[0, 0].set_xlabel('Year', fontsize='x-large')
    axs[0, 0].set_title('Neodymium', fontsize='25')
    axs[0, 0].yaxis.grid(True, linestyle='-', alpha=0.7)
    axs[0, 0].axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Neodymium'), :]), facecolor='#f2f2f2', alpha=0.2)
    axs[0, 0].tick_params(axis='both', which='major', labelsize='x-large')

    # Plot per il grafico dell'istogramma di Neodymium
    axs[1, 0].bar(years_subset, met_rec_data_full_Nd, alpha=0.7, label='Full Met Rec Cumulative', color='limegreen', edgecolor='limegreen')
    axs[1, 0].bar(years_subset, met_rec_data_target_Nd, alpha=0.7, label='Target Met Rec Cumulative', color='orangered', edgecolor='orangered')
    axs[1, 0].bar(years_subset, met_rec_data_hist_Nd, alpha=0.7, label='Hist Met Rec Cumulative', color='deepskyblue', edgecolor='deepskyblue')
    axs[1, 0].invert_yaxis()
    axs[1, 0].tick_params(axis='y', labelsize='x-large')
    axs[1, 0].set_xticks([])

    # Plot per Dysprosium
    axs[0, 1].plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Dysprosium'), :], label='Full RR', linestyle='-.', linewidth=3, markersize=8, color='limegreen')
    axs[0, 1].plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Dysprosium'), :], label='Target RR', linestyle='-', linewidth=3, markersize=8, color='orangered')
    axs[0, 1].plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Dysprosium'), :], label='Hist RR', linestyle='--', linewidth=3, markersize=8, color='deepskyblue')
   # axs[0, 1].set_xlabel('Year', fontsize='x-large')
    axs[0, 1].set_title('Dysprosium', fontsize='25')
    axs[0, 1].yaxis.grid(True, linestyle='-', alpha=0.7)
    axs[0, 1].axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Dysprosium'), :]), facecolor='#f2f2f2', alpha=0.2)
    axs[0, 1].tick_params(axis='both', which='major', labelsize='x-large')

    # Plot per il grafico dell'istogramma di Dysprosium
    axs[1, 1].bar(years_subset, met_rec_data_full_Dy, alpha=0.7, label='Full Met Rec Cumulative', color='limegreen', edgecolor='limegreen')
    axs[1, 1].bar(years_subset, met_rec_data_target_Dy, alpha=0.7, label='Target Met Rec Cumulative', color='orangered', edgecolor='orangered')
    axs[1, 1].bar(years_subset, met_rec_data_hist_Dy, alpha=0.7, label='Hist Met Rec Cumulative', color='deepskyblue', edgecolor='deepskyblue')
    axs[1, 1].invert_yaxis()
    axs[1, 1].tick_params(axis='y', labelsize='x-large')
    axs[1, 1].set_xticks([])

    # Plot per Copper
    axs[0, 2].plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Copper'), :], label='Full RR', linestyle='-.', linewidth=3, markersize=8, color='limegreen')
    axs[0, 2].plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Copper'), :], label='Target RR', linestyle='-', linewidth=3, markersize=8, color='orangered')
    axs[0, 2].plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Copper'), :], label='Hist RR', linestyle='--', linewidth=3, markersize=8, color='deepskyblue')
   # axs[0, 2].set_xlabel('Year', fontsize='x-large')
    axs[0, 2].set_title('Copper', fontsize='25')
    axs[0, 2].yaxis.grid(True, linestyle='-', alpha=0.7)
    axs[0, 2].axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Copper'), :]), facecolor='#f2f2f2', alpha=0.2)
    axs[0, 2].tick_params(axis='both', which='major', labelsize='x-large')

    # Plot per il grafico dell'istogramma di Copper
    axs[1, 2].bar(years_subset, met_rec_data_full_Cu, alpha=0.7, label='Full Met Rec Cumulative', color='limegreen', edgecolor='limegreen')
    axs[1, 2].bar(years_subset, met_rec_data_target_Cu, alpha=0.7, label='Target Met Rec Cumulative', color='orangered', edgecolor='orangered')
    axs[1, 2].bar(years_subset, met_rec_data_hist_Cu, alpha=0.7, label='Hist Met Rec Cumulative', color='deepskyblue', edgecolor='deepskyblue')
    axs[1, 2].invert_yaxis()
    axs[1, 2].tick_params(axis='y', labelsize='x-large')
    axs[1, 2].set_xticks([])

    # Plot per Silicon
    axs[0, 3].plot(years, res_base_RR['full'].loc[('World', 'Sector', 'Raw silicon'), :], label='Full RR', linestyle='-.', linewidth=3, markersize=8, color='limegreen')
    axs[0, 3].plot(years, res_base_RR['target'].loc[('World', 'Sector', 'Raw silicon'), :], label='Target RR', linestyle='-', linewidth=3, markersize=8, color='orangered')
    axs[0, 3].plot(years, res_base_RR['hist'].loc[('World', 'Sector', 'Raw silicon'), :], label='Hist RR', linestyle='--', linewidth=3, markersize=8, color='deepskyblue')
  #  axs[0, 3].set_xlabel('Year', fontsize='x-large')
    axs[0, 3].set_title('Raw silicon', fontsize='25')
    axs[0, 3].yaxis.grid(True, linestyle='-', alpha=0.7)
    axs[0, 3].axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Raw silicon'), :]), facecolor='#f2f2f2', alpha=0.2)
    axs[0, 3].tick_params(axis='both', which='major', labelsize='x-large')

    # Plot per il grafico dell'istogramma di Silicon
    axs[1, 3].bar(years_subset, met_rec_data_full_Si, alpha=0.7, label='Full Met Rec Cumulative', color='limegreen', edgecolor='limegreen')
    axs[1, 3].bar(years_subset, met_rec_data_target_Si, alpha=0.7, label='Target Met Rec Cumulative', color='orangered', edgecolor='orangered')
    axs[1, 3].bar(years_subset, met_rec_data_hist_Si, alpha=0.7, label='Hist Met Rec Cumulative', color='deepskyblue', edgecolor='deepskyblue')
    axs[1, 3].invert_yaxis()
    axs[1, 3].tick_params(axis='y', labelsize='x-large')
    axs[1, 3].set_xticks([])

   
    for ax in axs.flat:
       
        # Formatta le etichette dell'asse y in formato scientifico con "1e6"
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:g}'.format(x / 1e6) if x != 0 else '0'))
    handles_hist, labels_hist = axs[1, 0].get_legend_handles_labels()
    handles, labels = axs[0, 0].get_legend_handles_labels()

        # Valori degli anni da mostrare sull'asse x del primo grafico
    custom_xticks_first_plot = [2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080,  2090, 2100]
    
# Crea manualmente la legenda per gli istogrammi
    handles_hist, labels_hist = axs[1, 0].get_legend_handles_labels()
    handles, labels = axs[0, 0].get_legend_handles_labels()

    # Unisci le leggende
    handles.extend(handles_hist)
    labels.extend(labels_hist)

    axs[1, 0].legend(handles, labels, fontsize='x-large', loc='lower left')

    # Add a general title
    plt.suptitle('Cumulative production of metals and cumulative recycled metal [Mtons/year]', fontsize='40')
    
    # Etichetta esplicita per il primo valore sull'asse x del primo grafico e impostazione dei ticks personalizzati
    axs[0, 0].set_xlabel('Year', fontsize='x-large')
  
    axs[0, 0].set_xticks(custom_xticks_first_plot)
    axs[0, 1].set_xticks(custom_xticks_first_plot)
    axs[0, 2].set_xticks(custom_xticks_first_plot)
    axs[0, 3].set_xticks(custom_xticks_first_plot)

    axs[0, 0].set_xticklabels(custom_xticks_first_plot)
    
    plt.tight_layout()
    plt.show()