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
    "Electricity by hydro": {
        'name':'Hydro',
        'macrosource': 'Others',
        'color': '#0466c8',
    },
    "Electricity by Geothermal": {
        'name':'Geothermal',
        'macrosource': 'Others',
        'color': '#4cc9f0',
    },
    "Electricity by tide, wave, ocean": {
        'name':'Tide',
        'macrosource': 'Others',
        'color': '#2196f3',
    },
    "Electricity by nuclear": {
        'name':'Nuclear',
        'macrosource': 'Others',
        'color': '#b5179e',
    },
    "Electricity by solar thermal": {
        'name':'Solar thermal',
        'macrosource': 'Others',
        'color': '#f72585',
    },
    "Electricity by biomass and waste": {
        'name':'Biomass & waste',
        'macrosource': 'Others',
        'color': '#ffbf69',
    },
    "Electricity by coal": {
        'name':'Coal',
        'macrosource': 'Coal',
        'color': '#4a4e69',
    },
    "Electricity by gas": {
        'name':'Natural gas',
        'macrosource': 'Natural gas',
        'color': '#889696',
    },
    "Electricity by petroleum and other oil derivatives": {
        'name':'Oil',
        'macrosource': 'Oil',
        'color': '#b8bdb5',
    },
    "Electricity by solar photovoltaic": {
        'name':'PV',
        'macrosource': 'PV',
        'color': '#d9ed92',
    },
    "Electricity by wind": {
        'name':'Wind',
        'macrosource': 'Wind',
        'color': '#76c893',
    },
}

patterns = {'Local':'','Foreign':'x'}

scenarios = ['Baseline','IEA']
years = [2011,2015,2019]
scope = 'Total'
direction = 'Backward'
region = 'EU27+UK'

#%% Importing saved linkages
linkages = pd.read_csv(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Linkages.csv")#¶, index_col=[0])

#%% Filtering linkages analyzable by commodity
linkages_plot = linkages.query("Scope==@scope & Item in @commodities & Direction==@direction & Scenario in @scenarios & Year in @years & Region==@region")
linkages_plot = linkages_plot.sort_values(['Region','Item','Year','Scenario','Performance','Origin'], ascending=[True,True,True,True,True,True])  

linkages_plot = linkages_plot.replace('IEA','Endogenous capital') ##########

#%% New new plot

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
    
    x1 = [x1[0],x1[1],x1[2],x1[3],x1[4],x1[5],x1[-2],x1[-1]]
    x2 = [x2[0],x2[1],x2[2],x2[3],x2[4],x2[5],x2[-2],x2[-1]]
    
    
    fig.add_trace(go.Scatter(
        x = [[f"<b>{i}<b>" for i in x2], x1],
        y = [None],
        name = '<b>Total linkages<b>',
        legendgroup = 'Total linkages',
        mode = 'markers',
        marker_color = 'white',
        ))
    
    # plot
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
                x = [[f"<b>{i}<b>" for i in x2], x1],
                y = y,
                name = props['name'],
                legendgroup = props['name'],
                mode = 'markers',
                marker_color = props['color'],
                marker_symbol = 'diamond',
                marker_size = 10,
                ))
    
    
    fig.add_trace(go.Scatter(
        x = [[f"<b>{i}<b>" for i in x2], x1],
        y = [None],
        name = '',
        legendgroup = '',
        mode = 'markers',
        marker_color = 'white',
        ))
    fig.add_trace(go.Scatter(
        x = [[f"<b>{i}<b>" for i in x2], x1],
        y = [None],
        name = '<b>Linkages by origin<b>',
        legendgroup = 'Linkages by origin',
        mode = 'markers',
        marker_color = 'white',
        ))    
    
    for c,props in commodities.items():
    
        filtered_df = linkages_plot.query("Item==@c & Year==@year")
    
        if props['macrosource'] != 'Others':
            y = {'Foreign':[],'Local':[]}
            
            for i in range(len(x1)):
                if props['macrosource'] == x1[i]:
                    links = filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Average'")
                    for origin in patterns.keys():
                        y[origin] += [links.query(f"Origin=='{origin}'")['Value'].values[0]]
                else:
                    for origin in patterns.keys():
                        y[origin] += [None]  
            
            for origin,values in y.items():
    
                fig.add_trace(go.Bar(
                    x = [[f"<b>{i}<b>" for i in x2], x1],
                    y = values,
                    name = f"{props['name']}, {origin}",
                    legendgroup = props['name'],
                    marker_color = props['color'],
                    marker_pattern_shape = patterns[origin],
                    marker_pattern_size = 6, 
                    ))
        
            y_best = []
            y_worst = []
            y_tot = []
            
            for i in range(len(x1)):
                if props['macrosource'] == x1[i] and x2[i] != 'Baseline':
                    
                    y_tot += [filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Average'")['Value'].sum().sum()]    
                    y_best += [filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Average'")['Value'].sum().sum() - filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Best'")['Value'].sum().sum()]
                    y_worst += [filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Worst'")['Value'].sum().sum() - filtered_df.query(f"Scenario=='{x2[i]}' & Performance=='Average'")['Value'].sum().sum()]
        
                else:
                    y_tot += [None]
                    y_best += [None]
                    y_worst += [None]
    
            fig.add_trace(go.Scatter(
                x = [[f"<b>{i}<b>" for i in x2], x1],
                y = y_tot,
                error_y = dict(
                    type='data',
                    symmetric=False,
                    array=y_worst,
                    arrayminus=y_best,
                    thickness = 1,
                    ),
                name = "",
                legendgroup = "",
                marker_color = '#495057',
                showlegend=False,
                marker_size = 1,
                ))
        
    
                
    fig.update_layout(
        font_family='HelveticaNeue Light', 
        title = f'{scope} {direction.lower()} linkages of electricity generation sources in {region}   |   Exiobase v3.8.2, reference year {year}',
        template = 'plotly_white',
        legend_tracegroupgap=0.1,
        yaxis_title='Backward linkage',
        xaxis = dict(
            # title='Scenario',
            showline=True,
            linecolor='black'
            ),
        barmode='stack',
        # bargap = 0.6
        )
    
    fig.write_html(f'Plots/Linkages, final - {scenarios[-1]}, {year}.html', auto_open=True)
        



# #%% New plot
# fig = go.Figure()

# for c,props in commodities.items():
    
#     filtered_df = linkages_plot.query(f"Item=='{c}' & Year==2011")
#     y = []
#     x1 = []
#     x2 = []
#     row = 0
#     for i in filtered_df.index:
#         y  += [filtered_df.loc[i,"Backward"]]
#         x1 += [filtered_df.loc[i,"Performance"]]
#         x2 += [filtered_df.loc[i,"Scenario"]]
#         if i!=list(filtered_df.index)[-1]:
#             if filtered_df.loc[list(filtered_df.index)[row+1],"Scenario"] == 'Baseline':
#                 y  += [None]
#                 x1 += [filtered_df.loc[i,"Performance"]]
#                 x2 += [filtered_df.loc[i,"Scenario"]]
#         row += 1

#     if props['mode']['type'] == 'markers':
#         fig.add_trace(go.Scatter(
#             x = [x1, x2],
#             y = y,
#             name = props['name'],
#             legendgroup = props['name'],
#             mode = props['mode']['type'],
#             marker_color = props['mode']['color'],
#             marker_symbol = props['mode']['symbol'],
#             marker_size = 8,
#             )
#         )
#     if props['mode']['type'] == 'lines+markers':
#         fig.add_trace(go.Scatter(
#             x = [x1, x2],
#             y = y,
#             name = props['name'],
#             legendgroup = props['name'],
#             mode = props['mode']['type'],
#             marker_color = props['mode']['color'],
#             marker_symbol = props['mode']['symbol'],
#             marker_size = 8,
#             line_color = props['mode']['color'],
#             line_width = 1,
#             connectgaps=False
#             )
#         )

# fig.update_layout(
#     font_family='HelveticaNeue Light', 
#     title = 'Backward linkages of electricity generation sources. Baseline vs Adjusted Exiobase',
#     template = 'plotly_white',
#     legend_tracegroupgap=0.1,
#     yaxis_title='Backward linkage',
#     )

# fig.write_html(f'Plots/Linkages - Pre-Post - {scenarios[-1]}.html', auto_open=True)
# fig.show()

# #%%
# # auto=True
# # colors = px.colors.qualitative.Pastel
# # template = "seaborn"
# # font = "HelveticaNeue Light"
# # size = 16
# # labels = {
# #     'Forward': ':.3f',
# #     }

# # fig_linkages = px.scatter(
# #     linkages_plot,
# #     x='Forward',
# #     y='Backward',
# #     color = 'Item',
# #     animation_frame = 'Region',
# #     facet_col = "Performance",
# #     facet_row = "Year",
# #     color_discrete_sequence=colors,
# #     )

# # fig_linkages.update_layout(title="Forward & Backward Linkages", font_family=font, font_size=size, template=template)
# # fig_linkages.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
# # # fig_linkages.write_html(f"{pd.read_excel(paths, index_col=[0]).loc['Plots',user]}\\Linkages.html", auto_open=auto)
# # fig_linkages.show()


# # %%
