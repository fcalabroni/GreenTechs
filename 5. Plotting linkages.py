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

commodities = {
    "Electricity by coal": {
        'name':'Coal',
        'mode': {
            'type': 'markers',
            'color': '#001219',
            'symbol': 'circle',
        }
    },
    "Electricity by gas": {
        'name':'Natural gas',
        'mode': {
            'type': 'markers',
            'color': '#979dac',
            'symbol': 'circle',
        }
    },
    "Electricity by hydro": {
        'name':'Hydro',
        'mode': {
            'type': 'markers',
            'color': '#0466c8',
            'symbol': 'circle',
        }
    },
    "Electricity by nuclear": {
        'name':'Nuclear',
        'mode': {
            'type': 'markers',
            'color': '#b5179e',
            'symbol': 'circle',
        }
    },
    "Electricity by petroleum and other oil derivatives": {
        'name':'Oil',
        'mode': {
            'type': 'markers',
            'color': '#005f73',
            'symbol': 'circle',
        }
    },
    "Electricity by biomass and waste": {
        'name':'Biomass & waste',
        'mode': {
            'type': 'markers',
            'color': '#ff4d6d',
            'symbol': 'circle',
        }
    },
    "Electricity by solar photovoltaic": {
        'name':'PV',
        'mode': {
            'type': 'lines+markers',
            'color': '#f9c74f',
            'symbol': 'x',
        }
    },
    "Electricity by wind": {
        'name':'Wind',
        'mode': {
            'type': 'lines+markers',
            'color': '#2dc653',
            'symbol': 'x',
        }
    },
    "Electricity by Geothermal": {
        'name':'Geothermal',
        'mode': {
            'type': 'markers',
            'color': '#4cc9f0',
            'symbol': 'circle',
        }
    },
    "Electricity by solar thermal": {
        'name':'Solar thermal',
        'mode': {
            'type': 'markers',
            'color': '#ff8500',
            'symbol': 'circle',
        }
    },
    "Electricity by tide, wave, ocean": {
        'name':'Tide',
        'mode': {
            'type': 'markers',
            'color': '#2196f3',
            'symbol': 'circle',
        }
    },
}

scenarios = ['Baseline','IEA']
years = [2011,2015,2019]

#%% Importing saved linkages
linkages = pd.read_csv(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Linkages.csv")#¶, index_col=[0])

#%% Plotting Linkages analyzable by commodity
linkages_plot = linkages.query("Scope=='Total' & Item in @commodities & Scenario in @scenarios & Year in @years & Region=='EU27+UK'")
linkages_plot = linkages_plot.sort_values(['Region','Item','Year','Scenario','Performance'], ascending=[True,True,True,True,True])  

#%% New plot
fig = go.Figure()

for c,props in commodities.items():
    
    filtered_df = linkages_plot.query(f"Item=='{c}' & Performance=='Average'")
    y = []
    x1 = []
    x2 = []
    row = 0
    for i in filtered_df.index:
        y  += [filtered_df.loc[i,"Backward"]]
        x1 += [filtered_df.loc[i,"Year"]]
        x2 += [filtered_df.loc[i,"Scenario"]]
        if i!=list(filtered_df.index)[-1]:
            if filtered_df.loc[list(filtered_df.index)[row+1],"Scenario"] == 'Baseline':
                y  += [None]
                x1 += [filtered_df.loc[i,"Year"]]
                x2 += [filtered_df.loc[i,"Scenario"]]
        row += 1

    if props['mode']['type'] == 'markers':
        fig.add_trace(go.Scatter(
            x = [x1, x2],
            y = y,
            name = props['name'],
            legendgroup = props['name'],
            mode = props['mode']['type'],
            marker_color = props['mode']['color'],
            marker_symbol = props['mode']['symbol'],
            marker_size = 8,
            )
        )
    if props['mode']['type'] == 'lines+markers':
        fig.add_trace(go.Scatter(
            x = [x1, x2],
            y = y,
            name = props['name'],
            legendgroup = props['name'],
            mode = props['mode']['type'],
            marker_color = props['mode']['color'],
            marker_symbol = props['mode']['symbol'],
            marker_size = 8,
            line_color = props['mode']['color'],
            line_width = 1,
            connectgaps=False
            )
        )

fig.update_layout(
    font_family='HelveticaNeue Light', 
    title = 'Backward linkages of electricity generation sources. Baseline vs Adjusted Exiobase',
    template = 'plotly_white',
    legend_tracegroupgap=0.1,
    yaxis_title='Backward linkage',
    )

fig.write_html(f'Plots/Linkages - Pre-Post - {scenarios[-1]}.html', auto_open=True)
fig.show()

#%%
# auto=True
# colors = px.colors.qualitative.Pastel
# template = "seaborn"
# font = "HelveticaNeue Light"
# size = 16
# labels = {
#     'Forward': ':.3f',
#     }

# fig_linkages = px.scatter(
#     linkages_plot,
#     x='Forward',
#     y='Backward',
#     color = 'Item',
#     animation_frame = 'Region',
#     facet_col = "Performance",
#     facet_row = "Year",
#     color_discrete_sequence=colors,
#     )

# fig_linkages.update_layout(title="Forward & Backward Linkages", font_family=font, font_size=size, template=template)
# fig_linkages.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
# # fig_linkages.write_html(f"{pd.read_excel(paths, index_col=[0]).loc['Plots',user]}\\Linkages.html", auto_open=auto)
# fig_linkages.show()


# %%
