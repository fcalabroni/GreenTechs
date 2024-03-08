import matplotlib.pyplot as plt
import pandas as pd 

from matplotlib.gridspec import GridSpec

user = 'CF'
paths = 'Paths.xlsx'
#%%cumulativa baseline con i tre RR

AIC_divided = {}
lifetime = ['Min','Max','Avg']
AIC_divided_sum = {}
for l in lifetime:
    AIC_divided[l] = {}
    AIC_divided_sum[l] = {}

    for y in range(2000,2101):
        AIC_divided[l][y] = {}
        AIC_divided_sum[l][y] = {}

for l in lifetime:
    fileAIC = f"{pd.read_excel(paths, index_col=[0]).loc['AIC',user]}\\AIC_{l}.xlsx"
    for y in range(2000,2101):
        AIC_divided[l][y] = pd.read_excel(fileAIC, f'{y}',header =[0,1,2],index_col=[0,1,2])
        AIC_divided_sum[l][y] = AIC_divided[l][y].groupby(level=1,axis=1).sum()
        

regions =  AIC_divided['Min'][2000].index.get_level_values(0)
sector = AIC_divided['Min'][2000].index.get_level_values(1)
techs = AIC_divided['Min'][2000].index.get_level_values(2)
AIC_regions = {}
AIC_world = {}
for l in lifetime:
    AIC_regions[l] = pd.DataFrame(0,index= pd.MultiIndex.from_arrays([regions, sector , techs]), columns = range(2000,2101))
    AIC_world[l] = {}  
        
for l in lifetime:
    for y in range(2000,2101):
        AIC_regions[l].loc[:, y] = AIC_divided_sum[l][y].loc[:, :].values
        AIC_world[l] = AIC_regions[l].groupby(level=2).sum()
met_rec_world = {}
met_rec_cumulative = {}

#%%
years = range(2000,2101)
with plt.style.context('fivethirtyeight'):
    plt.figure(figsize=(12, 8))

    plt.plot(years, AIC_world['Max'].loc[('Onshore wind plants'), :], label='Max', linestyle='-', markersize=8)
    plt.plot(years, AIC_world['Min'].loc[('Onshore wind plants'), :], label='Min', linestyle='--', markersize=8)
    plt.plot(years, AIC_world['Avg'].loc[('Onshore wind plants'), :], label='Avg', linestyle='-.', markersize=8)
    # plt.plot(years, [16000000] * len(years), label='Reserves', linestyle='--', color='gray')

     # Adding labels, title, and legend
    plt.legend(fontsize='xx-large')
    plt.xlabel('Year',fontsize='xx-large')
    plt.ylabel('Million € ',fontsize='xx-large')
    plt.title('Technologies',fontsize='xx-large')

    # Adding grid
    plt.grid(True, linestyle='-', alpha=0.7)

    # Adding a background color
 #   plt.axhspan(0, max(res_base_RR['full'].loc[('World', 'Sector', 'Neodymium'), :]), facecolor='#f2f2f2', alpha=0.2)
    #sns.set_palette('husl')
    plt.tick_params(axis='both', which='major', labelsize='xx-large')

    plt.tight_layout()
    plt.show()