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

user = "LR"
sN = slice(None)

paths = 'Paths.xlsx'

commodities = {
    "Electricity by nuclear": {
        'name':'Nuclear',
        'macrosource': 'Others',
        'color': '#936fac',
    },
    "Electricity by biomass and waste": {
        'name':'Biomass & waste',
        'macrosource': 'Others',
        'color': '#ff006e',
    },
    "Electricity by solar thermal": {
        'name':'Solar thermal',
        'macrosource': 'Others',
        'color': '#f4a261',
    },    
    "Electricity by Geothermal": {
        'name':'Geothermal',
        'macrosource': 'Others',
        'color': '#b5e48c',
    }, 
    "Electricity by hydro": {
        'name':'Hydro',
        'macrosource': 'Others',
        'color': '#90e0ef',
    },
    "Electricity by tide, wave, ocean": {
        'name':'Tide',
        'macrosource': 'Others',
        'color': '#0077b6',
    },
    "Electricity by coal": {
        'name':'Coal',
        'macrosource': 'Coal',
        'color': '#212529',
    },
    "Electricity by gas": {
        'name':'Natural gas',
        'macrosource': 'Natural gas',
        'color': '#6c757d',
    },
    "Electricity by petroleum and other oil derivatives": {
        'name':'Oil',
        'macrosource': 'Oil',
        'color': '#adb5bd',
    },
    "Electricity by solar photovoltaic": {
        'name':'PV',
        'macrosource': 'PV',
        'color': '#ffc24b',
    },
    "Electricity by wind": {
        'name':'Wind',
        'macrosource': 'Wind',
        'color': '#219ebc',
    },
}

patterns = {'Local':'','Foreign':'x'}

scenarios = ['Baseline','IEA']
years = list(range(2011,2020))
scope = 'Total'
direction = 'Backward'
region = 'EU27+UK'

scenarios_renaming = {
    'Baseline': 'Baseline',
    'IEA': 'Endogenous capital',
    }

#%% Importing saved linkages
linkages = pd.read_csv(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Linkages.csv")#¶, index_col=[0])

#%% Filtering linkages analyzable by commodity
linkages_plot = linkages.query("Scope==@scope & Item in @commodities & Direction==@direction & Scenario in @scenarios & Year in @years & Region==@region")
linkages_plot = linkages_plot.sort_values(['Region','Item','Year','Scenario','Performance','Origin'], ascending=[True,True,True,True,True,True])  

for old,new in scenarios_renaming.items():
    linkages_plot = linkages_plot.replace(old,new) 

#%% Plot

for year in years:
    
    fig = go.Figure()
    
    # x axis preparation
    x1 = []
    x2 = []
    
    for scenario in sorted(list(set(linkages_plot['Scenario']))):
        for c,props in commodities.items():
            if props['macrosource'] not in x1:
                x1 += [props['macrosource']]
                x2 += [scenario]
    
    x1 = x1*len(list(set(linkages_plot['Scenario'])))
    for scenario in sorted(list(set(linkages_plot['Scenario'])))[1:]:
        for ms in range(len(set(x1))):
            x2 += [scenario]
    
    x1 = [x1[0],x1[1],x1[2],x1[3],x1[4],x1[5],x1[-2],x1[-1]] #########
    x2 = [x2[0],x2[1],x2[2],x2[3],x2[4],x2[5],x2[-2],x2[-1]] #########
    
    
    # fake trace for legend title
    fig.add_trace(go.Scatter(
        x = [[f"<b>{i}<b>" for i in x2], [f"<b>{i}<b>" for i in x1]],
        y = [None],
        name = '<b>Total linkages<b>',
        legendgroup = 'Total linkages',
        mode = 'markers',
        marker_color = 'white',
        ))
    
    # scatters total bl for "others" sources
    for c,props in commodities.items():
        
        filtered_df = linkages_plot.query("Item==@c & Year==@year")
        
        if props['macrosource'] == 'Others':
    
            y = []
            for i in range(len(x1)):
                if props['macrosource'] == x1[i]:
                    y += [filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Average'")['Value'].sum().sum()]
                else:
                    y += [None]               
    
            fig.add_trace(go.Scatter(
                x = [[f"<b>{i}<b>" for i in x2], [f"<b>{i}<b>" for i in x1]],
                y = y,
                name = props['name'],
                legendgroup = props['name'],
                mode = 'markers',
                marker_color = props['color'],
                marker_line_width = 0.5,
                marker_line_color = 'black',
                marker_symbol = 'circle',
                marker_size = 9,
                ))
    
    # empty trace
    fig.add_trace(go.Scatter(
        x = [[f"<b>{i}<b>" for i in x2], [f"<b>{i}<b>" for i in x1]],
        y = [None],
        name = '',
        legendgroup = '',
        mode = 'markers',
        marker_color = 'white',
        ))
    
    # fake trace for legend title
    fig.add_trace(go.Scatter(
        x = [[f"<b>{i}<b>" for i in x2], [f"<b>{i}<b>" for i in x1]],
        y = [None],
        name = '<b>Linkages by origin<b>',
        legendgroup = 'Linkages by origin',
        mode = 'markers',
        marker_color = 'white',
        ))    
    
    
    # bar plots for non "others" sources with error bars
    for c,props in commodities.items():
    
        filtered_df = linkages_plot.query("Item==@c & Year==@year")
    
        if props['macrosource'] != 'Others':
            y = {'Foreign':[],'Local':[]}
            y_best = {'Foreign':[],'Local':[]}
            y_worst = {'Foreign':[],'Local':[]}
            
            for i in range(len(x1)):
                if props['macrosource'] == x1[i]:
                    links = filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Average'")
                    for origin in patterns.keys():
                        y[origin] += [links.query(f"Origin=='{origin}'")['Value'].values[0]]
                    if x2[i] == 'Baseline':
                        for origin in patterns.keys():
                            y_best[origin] += [None]  
                            y_worst[origin] += [None]  
                    else:
                        for origin in patterns.keys():
                            links_best = filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Best' & Origin=='{origin}'")['Value'].values[0]
                            links_worst = filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Worst' & Origin=='{origin}'")['Value'].values[0]
                            
                            y_best[origin] += [links.query(f"Origin=='{origin}'")['Value'].values[0]-links_best]  
                            y_worst[origin] += [links_worst - links.query(f"Origin=='{origin}'")['Value'].values[0]]  
                else:
                    for origin in patterns.keys():
                        y[origin] += [None]  
                        y_best[origin] += [None]  
                        y_worst[origin] += [None]  
            
            for origin,values in y.items():
    
                fig.add_trace(go.Bar(
                    x = [[f"<b>{i}<b>" for i in x2], [f"<b>{i}<b>" for i in x1]],
                    y = values,
                    error_y=dict(
                        type='data',
                        symmetric=False,
                        array=y_worst[origin],
                        arrayminus=y_best[origin],
                        thickness = 1,
                        ),
                    name = f"{props['name']}, {origin}",
                    legendgroup = props['name'],
                    marker_color = props['color'],
                    marker_line_color = 'black',
                    marker_line_width = 0.75,
                    opacity = 0.6,
                    marker_pattern_shape = patterns[origin],
                    marker_pattern_size = 6, 
                    ))


    # empty trace
    # fig.add_trace(go.Scatter(
    #     x = [[f"<b>{i}<b>" for i in x2], [f"<b>{i}<b>" for i in x1]],
    #     y = [None],
    #     name = '',
    #     legendgroup = '',
    #     mode = 'markers',
    #     marker_color = 'white',
    #     ))

    # fake trace for error bands
    fig.add_trace(go.Scatter(
        x = [[f"<b>{i}<b>" for i in x2], [f"<b>{i}<b>" for i in x1]],
        y = [None],
        name = 'Capacity factor <br> uncertainty',
        legendgroup = 'Errors',
        mode = 'markers',
        marker_symbol = 'line-ns',
        marker_size = 13,
        marker_line_color = '#8690A1',
        marker_line_width = 1,
        ))         
            # total error bars
            # y_best = []
            # y_worst = []
            # y_tot = []
            
            # for i in range(len(x1)):
            #     if props['macrosource'] == x1[i] and x2[i] != 'Baseline':
                    
            #         y_tot += [filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Average'")['Value'].sum().sum()]    
            #         y_best += [filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Average'")['Value'].sum().sum() - filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Best'")['Value'].sum().sum()]
            #         y_worst += [filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Worst'")['Value'].sum().sum() - filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Average'")['Value'].sum().sum()]
        
            #     else:
            #         y_tot += [None]
            #         y_best += [None]
            #         y_worst += [None]
    
            # fig.add_trace(go.Scatter(
            #     x = [[f"<b>{i}<b>" for i in x2], [f"<b>{i}<b>" for i in x1]],
            #     y = y_tot,
            #     error_y = dict(
            #         type='data',
            #         symmetric=False,
            #         array=y_worst,
            #         arrayminus=y_best,
            #         thickness = 1,
            #         ),
            #     name = "",
            #     legendgroup = "",
            #     marker_color = '#495057',
            #     showlegend=False,
            #     marker_size = 1,
            #     ))
        
    
                
    fig.update_layout(
        font_family='HelveticaNeue Light', 
        title = f'<b>{direction} linkages of electricity generation sources in {region}   |   Exiobase v3.8.2, reference year {year}<b>',
        template = 'plotly_white',
        legend_tracegroupgap=0.1,
        yaxis_title='<b>Backward linkage<b>',
        xaxis = dict(
            # title='Scenario',
            showline=True,
            linecolor='black',
            linewidth=1.4,
            ),
        barmode='stack',
        # bargap = 0.6
        )
    
    fig.write_html(f'Plots/Backward linkages - {region}, {year}.html', auto_open=True)
        