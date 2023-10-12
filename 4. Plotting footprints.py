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
import plotly.graph_objects as go
from plotly.subplots import make_subplots


user = "LR"
sN = slice(None)

paths = 'Paths.xlsx'

price_logics = ['IEA']
years = range(2011,2020)
tech_performances = ['Worst','Average','Best']
scenarios_renaming = {
    'Baseline': 'Baseline',
    'IEA': 'Endogenous capital',
    }

sat_accounts = [
    'Energy Carrier Supply - Total', 
    'CO2 - combustion - air', 
    'CH4 - combustion - air', 
    'N2O - combustion - air',
    'Employment - High-skilled female',
    'Employment - High-skilled male',
    'Employment - Low-skilled female',
    'Employment - Low-skilled male',
    'Employment - Medium-skilled female',
    'Employment - Medium-skilled male',
    # 'Employment - Vulnerable employment',
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
        'Employment - High-skilled female': {
            "raw": '1000 p',
            "new": 'p',
            "conv": 1000,
            }, 
        'Employment - High-skilled male': {
            "raw": '1000 p',
            "new": 'p',
            "conv": 1000,
            }, 
        'Employment - Low-skilled female': {
            "raw": '1000 p',
            "new": 'p',
            "conv": 1000,
            }, 
        'Employment - Low-skilled male': {
            "raw": '1000 p',
            "new": 'p',
            "conv": 1000,
            }, 
        'Employment - Medium-skilled female': {
            "raw": '1000 p',
            "new": 'p',
            "conv": 1000,
            }, 
        'Employment - Medium-skilled male': {
            "raw": '1000 p',
            "new": 'p',
            "conv": 1000,
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


cf = {
      'Average': {
          'PV': 0.16,
          'Onshore wind': 0.35,
          'Offshore wind': 0.4,
          },
      'Worst': {
          'PV': 0.15,
          'Onshore wind': 0.3,
          'Offshore wind': 0.35,
          },
      'Best': {
          'PV': 0.17,
          'Onshore wind': 0.4,
          'Offshore wind': 0.45,
          },
      }

scemarios = []
for y in years:
    for s in price_logics+['Baseline']:
        for t in tech_performances:
            if s == 'Baseline': 
                scemarios += [f"{s} - {y} - Average"]
            else:
                scemarios += [f"{s} - {y} - {t}"]

#%% Reading and rearranging footprints results
# f = {}
# for sa in sat_accounts:
#     f[sa] = pd.DataFrame()
#     for scem in scemarios:
#         if scem != 'baseline':
#             scen = scem.split(' - ')[0]
#             year = scem.split(' - ')[1]
#             tech = scem.split(' - ')[2]
#             f_sa_scen = pd.read_csv(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Footprints - Monetary units\\{sa}\\{scen} - {year} - {tech}.csv", index_col=[0,1,2], header=[0,1,2], sep=',').loc[(sN,"Activity",sN),(sN,"Commodity",sN)]
#             f_sa_scen = f_sa_scen.stack(level=[0,1,2])
#             f_sa_scen = f_sa_scen.to_frame()
#             f_sa_scen.columns = ['Value']
#             f_sa_scen["Account"] = sa
#             f_sa_scen["Scenario"] = f"{scen} - {year} - {tech}"
#             f_sa_scen = f_sa_scen.droplevel(level=[1,4], axis=0)
#             f_sa_scen.index.names = ["Region from", "Commodity", "Region to", "Activity to"]
#             f_sa_scen = f_sa_scen.loc[(sN,sN,regions_to,activities_to),:]
#             f_sa_scen.reset_index(inplace=True)
#         f[sa] = pd.concat([f[sa], f_sa_scen], axis=0)
#     f[sa].set_index(["Region from", "Commodity", "Region to", "Activity to","Scenario","Account"], inplace=True)
#     f[sa] = f[sa].groupby(level=f[sa].index.names).mean()
    
#%% Conversions to physical units
# import time
# start = time.time()

# shockmaster = pd.read_excel(f"{pd.read_excel(paths, index_col=[0]).loc['ShockMaster',user]}", sheet_name=None, index_col=[0])
# ee_prices = {i:x for i,x in shockmaster.items() if 'prices' in i}

# for sa,footprint in f.items():
#     counter = 0
#     for i in footprint.index:
#         footprint.loc[i,"Unit"] = f"{units['Satellite account'][sa]['new']}/{units['Commodity'][i[3]]['new']}"
#         if 'Baseline' not in i[4]:
#             if units['Commodity'][i[3]]['conv'] == 'price':
#                 price = ee_prices[f"{i[4].split(' - ')[0]}_Electricity prices"].loc[i[2],int(i[4].split(' - ')[1])]
#                 footprint.loc[i,"Value"] *= units['Satellite account'][sa]['conv']*price*1e6
#             else:
#                 footprint.loc[i,"Value"] *= units['Satellite account'][sa]['conv']*units['Commodity'][i[3]]['conv']
#         else:
#             price = ee_prices["IEA_Electricity prices"].loc[i[2],2019]
#             footprint.loc[i,"Value"] *= units['Satellite account'][sa]['conv']*price*1e6
            
#     footprint.set_index(['Unit'], append=True, inplace=True)   

# end = time.time()
# print(round(end-start,2))

#%% Saving converted footprints
# writer = pd.ExcelWriter(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Footprints - Physical units.xlsx", engine='openpyxl', mode='w')
# for sa,footprint in f.items():
#     footprint.to_excel(writer, sheet_name=sa, merge_cells=False)
# writer.close()

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

#%% Plot: ghgs footprints by region&commodity. Subplots by unit of measures
sat = 'GHGs'
scenario = 'IEA'
performance = 'Average'

colors = {
    'Agriculture & food': '#f94144',
    'Mining & quarrying': '#f8961e',
    'Metals': '#f9c74f',
    'Petrochemicals': '#d9ed92',
    'Other manufacturing': '#74c69d',
    'Electricity': '#048ba8',
    'Services': '#184e77',
    'Transport': '#815ac0',
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
    'EU27+UK': "\\",
    'China': '/',
    'RoW': '',
    }

for year in years:
    query = f"Year=='{year}' & Scenario=='{scenario}' & Performance=='{performance}'"
    groupby = ["Region from", "Commodity", "Region to", "Activity to", "Unit"]
    
    f_ghg = f[sat].reset_index().query(query)
    for region in list(set(f_ghg['Region from'])):
        if region not in ['EU27+UK','China']:
            f_ghg = f_ghg.replace(region,'RoW')
    f_ghg = f_ghg.groupby(groupby).sum().reset_index()
    
    
    fig = make_subplots(rows=1, cols=len(set(f_ghg['Unit'])), subplot_titles=["<b>Electricity produced (tonCO2eq/GWh)<b>","<b>Capacity (tonCO2eq/MW)<b>"])

    # scatters
    col = 1
    showlegend = False
    for unit in sorted(list(set(f_ghg['Unit']))): 
        for s in sorted(list(set(f[sat].index.get_level_values('Scenario'))))[1:]:
            for y in sorted(list(set(f[sat].index.get_level_values('Year')))):
                for p in sorted(list(set(f[sat].index.get_level_values('Performance')))):
                    
                    tots = f[sat].reset_index().query(f"Unit=='{unit}' & Year=='{y}' & Scenario=='{s}' & Performance=='{p}'").groupby(['Activity to']).sum().reset_index()
    
                    if unit==sorted(list(set(f_ghg['Unit'])))[-1] and s==sorted(list(set(f[sat].index.get_level_values('Scenario'))))[-1] and y==sorted(list(set(f[sat].index.get_level_values('Year'))))[-1] and p==sorted(list(set(f[sat].index.get_level_values('Performance'))))[-1]:
                        showlegend=True
                    
                    fig.add_trace(go.Scatter(
                        x = [f"<b>{i}<b>" for i in  tots['Activity to']],
                        y = tots['Value'],
                        name = f'Sensitivity on other Exiobase<br>reference years ({years[0]}-{years[-1]})<br>and technology capacity factors<br>',
                        showlegend = showlegend,
                        mode = 'markers',
                        legendgroup = 'sensitivity',
                        # marker_color = 'black',
                        marker = dict(
                            size = 7,
                            color = years_colors[int(y)],
                            
                            ),
                        marker_line_width = 0.25,
                        marker_line_color = 'black',
                        # hovertemplate=f'Year: {y} <br>Performance: {p}',
                        ),
                        row = 1,
                        col= col,
                        )
                
        col += 1
    
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        name='',
        mode = 'markers',
        marker_color = 'white',
        ))
    
    # bars
    col = 1
    legend_labels = []
    for unit in sorted(list(set(f_ghg['Unit']))):   
        for commodity in list(colors.keys())[::-1]:
            for region in ['RoW','China','EU27+UK']:#sorted(list(set(f_ghg.query(f"Unit=='{unit}' & Commodity=='{commodity}'")['Region from']))):
                to_plot = f_ghg.query(f"Unit=='{unit}' & Commodity=='{commodity}' & `Region from` == '{region}'")                                            
                name = f"{commodity} - {region}"
                showlegend = False
                if name not in legend_labels:
                    legend_labels += [name]
                    showlegend = True
                
                fig.add_trace(go.Bar(
                    x = [f"<b>{i}<b>" for i in  to_plot['Activity to']],
                    y = to_plot['Value'],
                    name = name,
                    marker_color = colors[commodity],
                    marker_pattern_shape = patterns[region],
                    marker_line_color = 'black',
                    marker_line_width = 0.75,
                    marker_pattern_size = 6, 
                    legendgroup = name,
                    showlegend = showlegend,
                    # opacity=0.7,
                    ),
                    row = 1,
                    col = col,
                    )
    
        col += 1

    fig.update_layout(
        barmode='stack',
        font_family='HelveticaNeue Light', 
        # font_size=10,
        title = f"<b>GHGs footprints of electricity produced and capacity of PV and wind technologies</b><br>Exiobase v3.8.2 {year}, refined with MARIO | Capacity factors: PV={cf[performance]['PV']}, Onshore wind={cf[performance]['Onshore wind']}, Offshore wind={cf[performance]['Offshore wind']}",
        template = 'plotly_white',
        legend_tracegroupgap = 0.1,
        legend_title = "<b>Breakdown by origin commodity-region",
        legend_title_font_size = 13,
        legend_traceorder = 'reversed',
        xaxis1 = dict(
            showline=True,
            linecolor = 'black',
            linewidth = 1.4
            ),
        xaxis2 = dict(
            showline=True,
            linecolor = 'black',
            linewidth = 1.4
            ),
    
        )
    fig.update_annotations(font_size=13)
    fig.write_html(f'Plots/{sat} footprints, {year}.html', auto_open=True)
    

#%% Plot delta vs baseline 
sat = 'GHGs'
scenarios = ['Baseline','IEA']
performance = 'Average'

for year in years:
    sN = slice(None)
    indices = list(f[sat].index.names)
    indices.remove('Year')
    indices.remove('Performance')
    
    f_scen = f[sat].reset_index().query(f"Scenario in @scenarios & Year=='{year}' & Performance=='{performance}'")
    f_scen.set_index(indices,inplace=True)
    f_scen = f_scen.loc[:,"Value"].to_frame()
    
    f_plot = f_scen.reset_index().query("`Activity to`=='Electricity by PV' or `Activity to`=='Electricity by wind'")
    f_delta = f_plot.query("Scenario!='Baseline'").set_index(indices).values - f_plot.query("Scenario=='Baseline'").set_index(indices).values
    f_delta = pd.DataFrame(
        f_delta,
        index = f_plot.query("Scenario!='Baseline'").set_index(indices).index,
        columns = f_plot.query("Scenario!='Baseline'").set_index(indices).columns
        ).reset_index()
    f_delta = f_delta.replace(f'{scenarios[-1]}','Delta')
    f_scen = f_plot.groupby(["Activity to","Account","Scenario","Unit"]).sum()
    f_scen.reset_index(inplace=True)
    
    for region in list(set(f_delta['Region from'])):
        if region not in ['EU27+UK','China']:
            f_delta = f_delta.replace(region,'RoW')
    f_delta = f_delta.groupby(groupby).sum().reset_index()
    
    
    
    fig = go.Figure()
    
    # baseline
    fig.add_trace(go.Bar(
        x =  [f"<b>{i}" for i in f_scen.query("Scenario=='Baseline'")['Activity to'].values],
        y =  f_scen.query("Scenario=='Baseline'")['Value'].values,
        name = '<b>Baseline',
        showlegend = True,
        marker_color = '#343a40',
        marker_line_color = 'black',
        marker_line_width = 0.75,
        # texttemplate = 'Baseline',
        # marker_line = dict(color='black',width=1),
        ))
    
    # empty trace
    fig.add_trace(go.Scatter(
        x = [f"<b>{i}" for i in f_scen.query("Scenario=='Baseline'")['Activity to'].values],
        y = [None],
        name = '',
        mode = 'markers',
        marker_color = 'white',
        ))
            
    # deltas
    legend_labels = []
    for commodity in list(colors.keys())[::-1]:#sorted(list(set(f_delta['Commodity']))):
        for region in ['RoW','China','EU27+UK']:#sorted(list(set(f_delta.query(f"Commodity=='{commodity}'")['Region from']))):
            to_plot = f_delta.query(f"Commodity=='{commodity}' & `Region from` == '{region}'")                                            
            name = f"{commodity} - {region}"
            showlegend = False
            if name not in legend_labels:
                legend_labels += [name]
                showlegend = True
            
            fig.add_trace(go.Bar(
                x = [f"<b>{i}" for i in to_plot['Activity to'].values],
                y = to_plot['Value'].values,
                name = name,
                marker_color = colors[commodity],
                # marker_line = dict(color='black',width=1),
                marker_pattern_shape = patterns[region],
                marker_pattern_size = 6,
                legendgroup = name,
                showlegend = showlegend,
                marker_line_color = 'black',
                marker_line_width = 0.75,
                # opacity = 0.75,
                ))
    
    # # fake trace for legend title
    # fig.add_trace(go.Scatter(
    #     x = [f"<b>{i}" for i in f_scen.query("Scenario=='Baseline'")['Activity to'].values],
    #     y = [None],
    #     name = '<b>Variation from baseline by origin commodity-region',
    #     mode = 'markers',
    #     marker_color = 'white',
    #     ))

    f_scen_best = f[sat].reset_index().query(f"Scenario==@scenario & Year=='{year}' & Performance=='Best' & `Activity to`=='Electricity by PV' or `Activity to`=='Electricity by wind'")
    f_scen_worst = f[sat].reset_index().query(f"Scenario=='{scenario}' & Year=='{year}' & Performance=='Worst' & `Activity to`=='Electricity by PV' or `Activity to`=='Electricity by wind'")

    fig.update_layout(
        barmode='stack',
        font_family='HelveticaNeue Light', 
        title = f"<b>GHGs footprints of electricity produced by PV and wind technologies</b><br>Exiobase v3.8.2 {year}, refined with MARIO | Capacity factors: PV={cf[performance]['PV']}, Onshore wind={cf[performance]['Onshore wind']}, Offshore wind={cf[performance]['Offshore wind']}",
        template = 'plotly_white',
        yaxis_title="<b>gCO2eq/kWh",
        legend_tracegroupgap = 0.1,
        legend_title = '<b>Delta from Baseline by origin commodity-region',
        legend_title_font_size = 13,
        legend_traceorder = 'reversed',
        bargap = 0.5,
        xaxis=dict(
            showline=True,
            linecolor = 'black',
            linewidth = 1.4
            )
        )
    
    fig.write_html(f'Plots/GHGs footprints vs Baseline, {year}.html', auto_open=True)
    

#%% Plot employment
import plotly.express as px

empl_sats = [sa for sa in sat_accounts if "Employment" in sa]
performance = 'Average'

for year in years:

    color_map={
        "High-skilled": "#023047",
        "Medium-skilled": "#0096c7",
        "Low-skilled": "#caf0f8",
        }
    
    f_plot = pd.DataFrame()
    for sa in empl_sats:
        f_plot = pd.concat([f_plot,f[sa]], axis=0)
        
    f_plot.reset_index(inplace=True)
    f_plot = f_plot.query("`Activity to`=='Electricity by PV' or `Activity to`=='Electricity by wind'")
    f_plot = f_plot.query(f"Year=='{year}' & Performance=='{performance}'")
    
    
    f_plot['Gender'] = [i.split(" ")[-1].capitalize() for i in f_plot['Account']]
    f_plot['Skill'] = [i.split(" - ")[-1].split(" ")[0].capitalize() for i in f_plot['Account']]
    
    f_plot = f_plot.replace('USA','RoW')
    
    f_plot = f_plot.drop("Account",axis=1)
    f_plot = f_plot.groupby(["Region from","Activity to","Scenario","Year","Unit","Skill"]).sum().reset_index()
    
    for old,new in scenarios_renaming.items():
        f_plot = f_plot.replace(old,f"<b>{new}")
    
    f_plot = f_plot.sort_values(['Scenario'],ascending=[True])
    f_plot = f_plot.sort_values(by="Skill", key=lambda column: column.map(lambda e: ["Low-skilled","Medium-skilled","High-skilled"].index(e)))
    
    fig = px.bar(
        f_plot, 
        x='Scenario',
        y='Value',
        facet_col='Activity to',
        color='Skill',
        pattern_shape='Region from',
        color_discrete_map = color_map,
        )
    
    fig.update_traces(
        marker=dict(
            line_color="black", 
            pattern_size=6,
            line_width = 0.75
            ),
    )
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.for_each_annotation(lambda a: a.update(text=""))
    
        
    fig.update_layout(
        font_family='HelveticaNeue Light', 
        title = f"<b>Employment footprints of electricity produced by PV and wind technologies</b><br>Exiobase v3.8.2 {year}, refined with MARIO | Capacity factors: PV={cf[performance]['PV']}, Onshore wind={cf[performance]['Onshore wind']}, Offshore wind={cf[performance]['Offshore wind']}",
        template = 'plotly_white',
        yaxis_title="<b>Employed people/GWh",
        xaxis1 = dict(
            title='<b>Electricity by PV',
            title_font_size = 13,
            showline=True,
            linecolor = 'black',
            linewidth = 1.4
            ),
        xaxis2 = dict(
            title='<b>Electricity by wind',
            title_font_size = 13,
            showline=True,
            linecolor = 'black',
            linewidth = 1.4
            ),
        legend = dict(
            title = "<b>Breakdown by skill level and origin<b>",
            title_font_size = 13,
            traceorder = 'reversed',    
            )
        # bargap = 0.5,
        )
    
    fig.write_html(f'Plots/Employment footprints vs Baseline, {year}.html', auto_open=True)
    
