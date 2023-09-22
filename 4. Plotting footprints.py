#%% -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 2023

@authors: 
    Lorenzo Rinaldi, Department of Energy, Politecnico di Milano
    Nicolò Golinucci, PhD, Department of Energy, Politecnico di Milano
    Emanuele Mainardi, Department of Energy, Politecnico di Milano
    Prof. Matteo Vincenzo Rocco, PhD, Department of Energy, Politecnico di Milano
    Prof. Emanuela Colombo, PhD, Department of Energy, Politecnico di Milano
"""


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


user = "LR"
sN = slice(None)

paths = 'Paths.xlsx'

price_logics = ['Constant', 'IEA', 'EXIOHSUT']
years = range(2011,2020)
tech_performances = ['Worst','Average','Best']

#%%
sat_accounts = [
    'Energy Carrier Supply - Total', 
    'CO2 - combustion - air', 
    'CH4 - combustion - air', 
    'N2O - combustion - air',
    ]

units = {
    'Satellite account': {
        'Energy Carrier Supply - Total': {
            "raw": 'TJ',
            "new": 'GWh',
            "conv": 1/3.6,
            },
        'CO2 - combustion - air': {
            "raw": 'kg',
            "new": 'ton',
            "conv": 1/1000,
            }, 
        'CH4 - combustion - air': {
            "raw": 'kg',
            "new": 'ton',
            "conv": 1/1000,
            }, 
        'N2O - combustion - air': {
            "raw": 'kg',
            "new": 'ton',
            "conv": 1/1000,
            }, 
        'GHGs': {
            "raw": 'kg',
            "new": 'tonCO2eq',
            "conv": 1/1000,
            }, 
        },
    'Commodity': {
        "Offshore wind plants": {
            "raw": 'EUR',
            "new": 'MW',
            "conv": 3.19e6,
            }, 
        "Onshore wind plants": {
            "raw": 'EUR',
            "new": 'MW',
            "conv": 1.44e6,
            }, 
        "PV plants": {
            "raw": 'EUR',
            "new": 'MW',
            "conv": 1.81e6,
            }, 
        "Electricity by wind": {
            "raw": 'EUR',
            "new": 'GWh',
            "conv": 'price',
            }, 
        "Electricity by PV": {
            "raw": 'EUR',
            "new": 'GWh',
            "conv": 'price',
            }, 
        },
    }

GWP = {
       "CO2 - combustion - air": 1,
       "CH4 - combustion - air": 26,
       "N2O - combustion - air": 298,
    }

regions_to = ['EU27+UK']
activities_to = [
    "Offshore wind plants",
    "Onshore wind plants",
    "PV plants",
    'Electricity by wind',
    "Electricity by PV",
    ]

scemarios = ['baseline']
for y in years:
    for s in price_logics:
        for t in tech_performances:
            scemarios += [f"{s} - {y} - {t}"]

#%% Reading and rearranging footprints results
f = {}
for sa in sat_accounts:
    f[sa] = pd.DataFrame()
    for scem in scemarios:
        if scem != 'baseline':
            scen = scem.split(' - ')[0]
            year = scem.split(' - ')[1]
            tech = scem.split(' - ')[2]
            f_sa_scen = pd.read_csv(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Footprints - Monetary units\\{sa}\\{scen} - {year} - {tech}.csv", index_col=[0,1,2], header=[0,1,2], sep=',').loc[(sN,"Activity",sN),(sN,"Commodity",sN)]
            f_sa_scen = f_sa_scen.stack(level=[0,1,2])
            f_sa_scen = f_sa_scen.to_frame()
            f_sa_scen.columns = ['Value']
            f_sa_scen["Account"] = sa
            f_sa_scen["Scenario"] = f"{scen} - {year} - {tech}"
            f_sa_scen = f_sa_scen.droplevel(level=[1,4], axis=0)
            f_sa_scen.index.names = ["Region from", "Commodity", "Region to", "Activity to"]
            f_sa_scen = f_sa_scen.loc[(sN,sN,regions_to,activities_to),:]
            f_sa_scen.reset_index(inplace=True)
        else:
            f_sa_scen = pd.read_csv(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Footprints - Monetary units\\{sa}\\{scem}.csv", index_col=[0,1,2], header=[0,1,2], sep=',').loc[(sN,"Activity",sN),(sN,"Commodity",sN)]
            f_sa_scen = f_sa_scen.stack(level=[0,1,2])
            f_sa_scen = f_sa_scen.to_frame()
            f_sa_scen.columns = ['Value']
            f_sa_scen["Account"] = sa
            f_sa_scen["Scenario"] = f"{scem}"
            f_sa_scen = f_sa_scen.droplevel(level=[1,4], axis=0)
            f_sa_scen.index.names = ["Region from", "Commodity", "Region to", "Activity to"]
            f_sa_scen = f_sa_scen.loc[(sN,sN,regions_to,activities_to),:]
            f_sa_scen.reset_index(inplace=True)
        
        f[sa] = pd.concat([f[sa], f_sa_scen], axis=0)
    f[sa].replace("baseline", "Baseline", inplace=True)
    f[sa].set_index(["Region from", "Commodity", "Region to", "Activity to","Scenario","Account"], inplace=True)
    f[sa] = f[sa].groupby(level=f[sa].index.names).mean()
    
#%% Conversions to physical units
import time
start = time.time()

shockmaster = pd.read_excel(f"{pd.read_excel(paths, index_col=[0]).loc['ShockMaster',user]}", sheet_name=None, index_col=[0])
ee_prices = {i:x for i,x in shockmaster.items() if 'prices' in i}

for sa,footprint in f.items():
    counter = 0
    for i in footprint.index:
        footprint.loc[i,"Unit"] = f"{units['Satellite account'][sa]['new']}/{units['Commodity'][i[3]]['new']}"
        if i[4] != 'Baseline':
            if units['Commodity'][i[3]]['conv'] == 'price':
                price = ee_prices[f"{i[4].split(' - ')[0]}_Electricity prices"].loc[i[2],int(i[4].split(' - ')[1])]
                footprint.loc[i,"Value"] *= units['Satellite account'][sa]['conv']*price*1e6
            else:
                footprint.loc[i,"Value"] *= units['Satellite account'][sa]['conv']*units['Commodity'][i[3]]['conv']
        else:
            price = ee_prices["IEA_Electricity prices"].loc[i[2],2019]
            footprint.loc[i,"Value"] *= units['Satellite account'][sa]['conv']*price*1e6
            
    footprint.set_index(['Unit'], append=True, inplace=True)   

end = time.time()
print(round(end-start,2))

#%% Saving converted footprints
writer = pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Footprints - Physical units.xlsx", engine='openpyxl', mode='w')
for sa,footprint in f.items():
    footprint.to_excel(writer, sheet_name=sa, merge_cells=False)
writer.close()

#%% Read saved footprints in physical units
f = {}
for sa in sat_accounts:
    f[sa] = pd.read_excel(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Footprints - Physical units.xlsx", sheet_name=sa, index_col=[0,1,2,3,4,5,6])
    
#%% Calculation of total GHG emissions
f['GHGs'] = pd.DataFrame()
for sa,gwp in GWP.items():
    f['GHGs'] = pd.concat([f['GHGs'], f[sa]*gwp], axis=0)
f['GHGs'] = f['GHGs'].groupby(level=["Region from","Commodity","Region to","Activity to","Scenario"]).sum()
for i in f['GHGs'].index:
    f['GHGs'].loc[i,"Account"] = "GHG emmissions"
    f['GHGs'].loc[i,"Unit"] = f"{units['Satellite account']['GHGs']['new']}/{units['Commodity'][i[3]]['new']}"
f['GHGs'].set_index(['Account','Unit'], append=True, inplace=True)

#%% Split scemarios columns
sN = slice(None)
f_baseline = {i:x.loc[(sN,sN,sN,sN,'Baseline',sN,sN),:] for i,x in f.items()}
scenarios = sorted(list(set(f['GHGs'].index.get_level_values('Scenario'))))
scenarios.remove('Baseline')
f = {i:x.loc[(sN,sN,sN,sN,scenarios,sN,sN),:] for i,x in f.items()}

for sa,footprint in f.items():
    footprint.loc[:,'Scenario'] = [i.split(' - ')[0] for i in footprint.index.get_level_values("Scenario")]
    footprint.loc[:,'Year'] = [i.split(' - ')[1] for i in footprint.index.get_level_values("Scenario")]
    footprint.loc[:,'Performance'] = [i.split(' - ')[2] for i in footprint.index.get_level_values("Scenario")]
    footprint = footprint.droplevel("Scenario")
    footprint.reset_index(inplace=True)
    footprint.set_index(['Region from', 'Commodity', 'Region to', 'Activity to', 'Scenario', 'Year', 'Performance', 'Account', 'Unit'], inplace=True)
    f[sa] = footprint
        
#%% Aggregating
new_commodities = pd.read_excel(r"Aggregations\Aggregation_plots.xlsx", index_col=[0])
for sa,v in f.items():
    index_names = list(v.index.names)
    for i in v.index:
        v.loc[i,"Commodity"] = new_commodities.loc[i[1],"New"]
    v = v.droplevel("Commodity", axis=0)
    v.reset_index(inplace=True)
    v.set_index(index_names, inplace=True)
    v = v.groupby(level=index_names, axis=0).sum()
    f[sa] = v

for sa,v in f_baseline.items():
    index_names = list(v.index.names)
    for i in v.index:
        v.loc[i,"Commodity"] = new_commodities.loc[i[1],"New"]
    v = v.droplevel("Commodity", axis=0)
    v.reset_index(inplace=True)
    v.set_index(index_names, inplace=True)
    v = v.groupby(level=index_names, axis=0).sum()
    f_baseline[sa] = v

#%% Plot: ghgs footprints by region&commodity. Subplots by unit of measures
sat = 'GHGs'
year = 2019
scenario = 'IEA'
performance = 'Average'

query = f"Year=='{year}' & Scenario=='{scenario}' & Performance=='{performance}'"
# groupby = {
#     'Commodity': ["Commodity", "Region to", "Activity to", "Unit"],
#     'Region': ["Region from", "Region to", "Activity to", "Unit"],
#     }
groupby = ["Region from", "Commodity", "Region to", "Activity to", "Unit"]

f_ghg = f[sat].reset_index().query(query)
for region in list(set(f_ghg['Region from'])):
    if region not in ['EU27+UK','China']:
        f_ghg = f_ghg.replace(region,'RoW')
f_ghg = f_ghg.groupby(groupby).sum().reset_index()


fig = make_subplots(rows=1, cols=len(set(f_ghg['Unit'])), subplot_titles=["Electricity (gCO2eq/kWh)","Capacity (gCO2eq/W)"])

colors = {
    'Agriculture, cattling & fishering': '#54478c',
    'Chemicals': '#2c699a',
    'Electricity': '#048ba8',
    'Food': '#0db39e',
    'Fuels refinery': '#16db93',
    'Metals': '#83e377',
    'Mining & quarrying': '#b9e769',
    'Other manufacturing': '#efea5a',
    'Services': '#f1c453',
    'Transport': '#f29e4c',
    }

years_colors = {
    2011: '#e9ecef',
    2012: '#dee2e6',
    2013: '#ced4da',
    2014: '#adb5bd',
    2015: '#6c757d',
    2016: '#495057',
    2017: '#343a40',
    2018: '#212529',
    2019: '#000000',
    }

patterns = {
    'EU27+UK': '',
    'China': 'x',
    'RoW': '.',
    }

col = 1
legend_labels = []
for unit in sorted(list(set(f_ghg['Unit']))):   
    for commodity in sorted(list(set(f_ghg.query(f"Unit=='{unit}'")['Commodity']))):
        for region in sorted(list(set(f_ghg.query(f"Unit=='{unit}' & Commodity=='{commodity}'")['Region from']))):
            to_plot = f_ghg.query(f"Unit=='{unit}' & Commodity=='{commodity}' & `Region from` == '{region}'")                                            
            name = f"{commodity} - {region}"
            showlegend = False
            if name not in legend_labels:
                legend_labels += [name]
                showlegend = True
            
            fig.add_trace(go.Bar(
                x = to_plot['Activity to'],
                y = to_plot['Value'],
                name = name,
                marker_color = colors[commodity],
                marker_pattern_shape = patterns[region],
                marker_line = dict(color='black',width=1),
                legendgroup = name,
                showlegend = showlegend
                ),
                row = 1,
                col = col,
                )

    col += 1


col = 1
for unit in sorted(list(set(f_ghg['Unit']))): 
    for s in ['IEA']: #sorted(list(set(f[sat].index.get_level_values('Scenario')))):
        for y in sorted(list(set(f[sat].index.get_level_values('Year'))))[-1::]:
            for p in sorted(list(set(f[sat].index.get_level_values('Performance'))))[-1::]:
                
                tots = f[sat].reset_index().query(f"Unit=='{unit}' & Year=='{y}' & Scenario=='{s}' & Performance=='{p}'").groupby(['Activity to']).sum().reset_index()
                
                fig.add_trace(go.Scatter(
                    x = tots['Activity to'],
                    y = tots['Value'],
                    name = f'{s} - {y} - {p}',
                    showlegend = False,
                    mode = 'markers',
                    # marker_color = 'black',
                    marker = dict(
                        size = 7,
                        color = years_colors[int(y)],
                        ),
                    hovertemplate=f'Year: {y} <br>Performance: {p}',
                    ),
                    row = 1,
                    col= col,
                    )
    col += 1
            

fig.update_layout(
    barmode='stack',
    font_family='HelveticaNeue Light', 
    # font_size=10,
    title = 'GHGs footprints per unit of electricity produced by source (kWh) and technology capacity (W). Breakdown by region and commodity of origin',
    template = 'plotly_white',
    legend_tracegroupgap = 0.1,
    legend_traceorder = 'reversed',
    )

fig.write_html('Plots/GHGs emissions.html', auto_open=True)
    

#%% Plot baseline 
sat = 'GHGs'
year = 2019
scenario = 'IEA'
performance = 'Average'

sN = slice(None)
indices = list(f[sat].index.names)
indices.remove('Year')
indices.remove('Performance')

f_scen = f[sat].reset_index().query(f"Scenario=='{scenario}' & Year=='{year}' & Performance=='{performance}'")
f_scen.set_index(indices,inplace=True)
f_scen = f_scen.loc[:,"Value"].to_frame()

f_plot = f_baseline[sat].append(f_scen).reset_index().query("`Activity to`=='Electricity by PV' or `Activity to`=='Electricity by wind'")
f_delta = f_plot.query("Scenario!='Baseline'").set_index(indices).values - f_plot.query("Scenario=='Baseline'").set_index(indices).values
f_delta = pd.DataFrame(
    f_delta,
    index = f_plot.query("Scenario!='Baseline'").set_index(indices).index,
    columns = f_plot.query("Scenario!='Baseline'").set_index(indices).columns
    ).reset_index()
f_delta = f_delta.replace('IEA','Delta')
f_scen = f_plot.groupby(["Activity to","Account","Scenario","Unit"]).sum()
f_scen.reset_index(inplace=True)

for region in list(set(f_delta['Region from'])):
    if region not in ['EU27+UK','China']:
        f_delta = f_delta.replace(region,'RoW')
f_delta = f_delta.groupby(groupby).sum().reset_index()



fig = go.Figure()

legend_labels = []
for commodity in sorted(list(set(f_delta['Commodity'])))[-1::]:
    for region in sorted(list(set(f_delta.query(f"Commodity=='{commodity}'")['Region from'])))[-1::]:
        to_plot = f_delta.query(f"Commodity=='{commodity}' & `Region from` == '{region}'")                                            
        name = f"Delta: {commodity} - {region}"
        showlegend = False
        if name not in legend_labels:
            legend_labels += [name]
            showlegend = True
        
        fig.add_trace(go.Bar(
            x = to_plot['Activity to'].values,
            y = to_plot['Value'].values,
            name = name,
            marker_color = colors[commodity],
            marker_line = dict(color='black',width=1),
            marker_pattern_shape = patterns[region],
            legendgroup = name,
            showlegend = showlegend
            ))

fig.add_trace(go.Bar(
    x =  f_scen.query("Scenario=='Baseline'")['Activity to'].values,
    y =  f_scen.query("Scenario=='Baseline'")['Value'].values,
    name = 'Baseline',
    showlegend = True,
    marker_color = '#9a8c98',
    marker_line = dict(color='black',width=1),
    ))

fig.update_layout(
    barmode='stack',
    font_family='HelveticaNeue Light', 
    title = 'GHGs footprints per unit of electricity produced by source (kWh). Baseline Exiobase vs fixed Exiobase',
    template = 'plotly_white',
    legend_tracegroupgap = 0.1,
    legend_traceorder = 'reversed',
    )

fig.write_html('Plots/GHGs delta.html', auto_open=True)

#%%
# auto = True
# to_plot = {
#     'Capacity': {
#         'x': 'Year',
#         'y': 'Value',
#         # 'facet_row': 'Region from',
#         'facet_col': 'Region from',
#         'color': 'Commodity',
#         'title': 'installed capacity',
#         # 'animation_frame': 'Scenario',
#         'activities': ["Offshore wind plants","Onshore wind plants","PV plants"],
#         'satellite accounts': {
#             'GHGs': {
#                 'name': 'GHG emissions',
#                 },
#             'Energy Carrier Supply - Total': {
#                 'name': 'Primary energy',
#                 },
#             },
#         },
#     'Electricity': {
#         'x': 'Performance',
#         'y': 'Value',
#         'facet_row': 'Region from',
#         'facet_col': 'Year',
#         'color': 'Commodity',
#         'title': 'electricity produced',
#         'animation_frame': 'Scenario',
#         'activities': ["Electricity by wind","Electricity by PV"],
#         'satellite accounts': {
#             'GHGs': {
#                 'name': 'GHG emissions',
#                 },
#             'Energy Carrier Supply - Total': {
#                 'name': 'Primary energy',
#                 },
#             },
#         },
#     }

# colors = px.colors.qualitative.Pastel
# template = "seaborn"
# font = "HelveticaNeue Light"
# size = 16
# labels = {
#     'Activity to': False,   
#     # 'Scenario': False,
#     'Value': ':.2f',
#     }

# for plot,properties in to_plot.items():
#     for sa,name in properties['satellite accounts'].items():
#         for act in properties['activities']:

#             plot_df = f[sa].groupby(level=["Region from","Commodity","Activity to", "Scenario", "Year","Performance","Unit"]).sum() 

#             if plot == 'Capacity':
#                 plot_df = f[sa].groupby(level=["Region from","Commodity","Activity to", "Year","Performance","Unit"]).mean() 
#                 plot_df = f[sa].groupby(level=["Region from","Commodity","Activity to", "Year","Unit"]).mean() 
#                 plot_df = plot_df.loc[(sN,sN,act,sN,sN,sN),:].sort_values(['Region from','Commodity','Year'], ascending=[False,False,True])  
#             else:
#                 indexnames = plot_df.index.names
#                 plot_df.reset_index(inplace=True)
#                 plot_df.replace("Average", "Medium", inplace=True)
#                 plot_df.set_index(indexnames,inplace=True)
#                 plot_df = plot_df.loc[(sN,sN,act,sN,sN,sN),:].sort_values(['Region from','Commodity','Scenario','Year','Performance'], ascending=[False,False,True,True,True])  

#             plot_df.reset_index(inplace=True)
            
#             if plot == 'Capacity':
#                 fig = px.bar(
#                     plot_df, 
#                     x=properties['x'],
#                     y=properties['y'],
#                     color=properties['color'],
#                     facet_col=properties['facet_col'],
#                     # facet_row=properties['facet_row'],
#                     # animation_frame=properties['animation_frame'],
#                     color_discrete_sequence=colors,
#                     title=f"{name['name']} footprint per unit of {properties['title']} of {act} in EU27+UK, allocated by region and commodity [{list(set(plot_df['Unit']))[0]}]",
#                     template=template, 
#                     hover_data=labels,
#                     )
#             else:
#                 fig = px.bar(
#                     plot_df, 
#                     x=properties['x'],
#                     y=properties['y'],
#                     color=properties['color'],
#                     facet_col=properties['facet_col'],
#                     facet_row=properties['facet_row'],
#                     animation_frame=properties['animation_frame'],
#                     color_discrete_sequence=colors,
#                     title=f"{name['name']} footprint per unit of {act} in EU27+UK, allocated by region and commodity [{list(set(plot_df['Unit']))[0]}]",
#                     template=template, 
#                     hover_data=labels,
#                     )
    
#             fig.update_layout(
#                 legend=dict(
#                     title=None, 
#                     traceorder='reversed'
#                     ), 
#                 xaxis=dict(
#                     title=None
#                     ), 
#                 font_family=font, 
#                 font_size=size
#                 )    
    
#             fig.update_traces(marker_line_width=0)
#             fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
#             fig.for_each_yaxis(lambda axis: axis.update(title=None))
#             fig.for_each_xaxis(lambda axis: axis.update(title=None))
#             fig.write_html(f"{pd.read_excel(paths, index_col=[0]).loc['Plots',user]}\\{act}_{name['name']}.html", auto_open=auto)
    
    
# #%% Plotting general results
# import plotly.express as px

# Act_to = "Electricity by wind"
# Sat = "GHGs"

# df = f[Sat].reset_index().query(f"`Activity to` == '{Act_to}'")

# res = df.groupby(['Scenario','Year','Performance']).sum().reset_index()
# fig = px.line(res, x="Year", y="Value", color="Performance", facet_col="Scenario")
# fig.write_html('Plots/line.html', auto_open=True)
# fig.show()

# #%% One boxplot per Act_to
# import plotly.express as px

# df = f[Sat].groupby(['Scenario','Year','Performance','Unit','Activity to']).sum().reset_index()

# fig = px.box(df, x="Scenario", y="Value", color="Performance", facet_col="Activity to", facet_row="Unit")
# fig.show()
# fig.write_html('Plots/boxplot.html', auto_open=True)

# # %% Exploring one characteristic result

# Act_to = "Electricity by PV"
# Sat = "GHGs"
# Perf = "Average"
# Scenario = "IEA"
# Year = 2018

# df = f[Sat].reset_index().query(f"`Activity to` == '{Act_to}' & Performance == '{Perf}' & Year == '{Year}' & Scenario == '{Scenario}'")
# fig = px.bar(df, x="Region from", y="Value", color="Commodity")

# tot_fot = round(df.loc[:,'Value'].sum(),2)

# fig.update_layout(title=f"{Sat} footprint per unit of {Act_to} in {Scenario}, {Year}, {Perf}<br>{tot_fot} {df.loc[[df.index[0]],'Unit'].values[0]}")
# fig.show()
# fig.write_html('Plots/')

# # %%
