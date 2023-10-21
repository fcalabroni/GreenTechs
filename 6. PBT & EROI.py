import mario
import pandas as pd
import numpy as np
import plotly.express as px

user = "LR"
sN = slice(None)

paths = 'Paths.xlsx'

years = range(2011,2020)

satellite_accounts = ['GHGs','Energy Carrier Supply - Total']
price_logics = ['Constant']
region = 'EU27+UK'

caps = {
    'Production of photovoltaic plants': 'PV',
    'Production of onshore wind plants': 'Onshore wind',
    'Production of offshore wind plants': 'Offshore wind',
    }
    
ee = [
    'Production of electricity by Geothermal',
    'Production of electricity by biomass and waste',
    'Production of electricity by coal',
    'Production of electricity by gas',
    'Production of electricity by hydro',
    'Production of electricity by nuclear',
    'Production of electricity by petroleum and other oil derivatives',
    'Production of electricity by solar photovoltaic',
    'Production of electricity by solar thermal',
    'Production of electricity by tide, wave, ocean',
    'Production of electricity by wind',
    'Production of electricity nec',                
  ]

conv_factors = {
    'GHGs':1e-3,
    'Energy Carrier Supply - Total': 1e-3,
    }

lifetime = {
      'Average': {'PV': 25,'Onshore wind': 20,'Offshore wind': 20,},
      'Worst': {'PV': 20,'Onshore wind': 15,'Offshore wind': 15,},
      'Best': {'PV': 30,'Onshore wind': 25,'Offshore wind': 25,},
      }

cf = {
      'Average': {'PV': 0.16,'Onshore wind': 0.35,'Offshore wind': 0.4,},
      'Worst': {'PV': 0.15,'Onshore wind': 0.3,'Offshore wind': 0.35,},
      'Best': {'PV': 0.17,'Onshore wind': 0.4,'Offshore wind': 0.45,},
      }

#%% Payback time
for satellite_account in satellite_accounts:
    
    print(f"\n{satellite_account}")
    
    print("   read and aggregate footprints")
    f = pd.read_csv(
        f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Footprints - Physical units\\{satellite_account}.csv",
        index_col=[0,1,2,3,4],
        )
    f['Scenario'] = [i.split(' - ')[0] for i in f.index.get_level_values('Scenario')]
    f = f.query("Scenario==@price_logics")
    f = f.drop('Scenario',axis=1)
    
    f = f.groupby(['Activity to','Scenario']).sum()
    f['Scenario'] = [i.split(' - ')[0] for i in f.index.get_level_values('Scenario')]
    f['Year'] = [i.split(' - ')[1] for i in f.index.get_level_values('Scenario')]
    f['Performance'] = [i.split(' - ')[2] for i in f.index.get_level_values('Scenario')]
    
    scenarios = sorted(list(set(f.index.get_level_values('Scenario'))))
    f = f.droplevel('Scenario')
    f.reset_index(inplace=True)

    print("   parse tables")
    world = {}
    for scenario in scenarios:
        if scenario.split(' - ')[0] in price_logics:
            world[scenario] = mario.parse_from_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\d. Shock - Endogenization of capital\\{scenario}\\coefficients", table='SUT', mode="coefficients")

    print("   calc numerator")
    IN = {}
    
    for tech in caps:
        IN[tech] = pd.DataFrame()
        for scenario in scenarios:
            
            s = scenario.split(' - ')[0]
            y = scenario.split(' - ')[1]
            p = scenario.split(' - ')[2]
            
            value = f.query(f"`Activity to`=='{tech}' & Scenario==@s & Year==@y & Performance==@p")
            value.set_index(['Activity to','Scenario','Year','Performance'],inplace=True)
            
            IN[tech] = pd.concat([IN[tech],value],axis=0)
       
    print("   calc denominator")
    OUT = pd.DataFrame()
    for scenario in scenarios:
        
        s = scenario.split(' - ')[0]
        y = scenario.split(' - ')[1]
        p = scenario.split(' - ')[2]
            
        prod = world[scenario].X.loc[(region,sN,ee),'production']
        prod /= prod.sum().sum()
        prod = prod.to_frame()
        
        prod.index = prod.index.get_level_values(2)
        
        value = f.query("`Activity to`==@ee & Scenario==@s & Year==@y & Performance==@p")
        value.set_index(['Activity to','Scenario','Year','Performance'],inplace=True)
        value.index = value.index.get_level_values(0)
        
        prod.index.names = value.index.names
        
        OUT = pd.concat([
            OUT,
            pd.DataFrame(
                np.multiply(value,prod).sum().sum()*conv_factors[satellite_account],
                index = pd.MultiIndex.from_arrays([[s],[y],[p]], names=['Scenario','Year','Performance']),
                columns = ['Value'],
                )],
            axis=0,
            )
   
    print("   calc pbt")
    from copy import deepcopy as dc
    PBT = dc(IN)
    PBT_merged = pd.DataFrame()
    
    for tech in caps:
        for scenario in scenarios:
        
            s = scenario.split(' - ')[0]
            y = scenario.split(' - ')[1]
            p = scenario.split(' - ')[2]
        
            PBT[tech].loc[(tech,s,y,p),'Value'] /= OUT.loc[(s,y,p),'Value']
            
        PBT[tech] /= 8760/12  # in months
        PBT_merged = pd.concat([PBT_merged,PBT[tech]],axis=0)


    print("   export csvs")
    for tech in caps:
        PBT[tech].to_csv(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Payback-time\\{satellite_account}\\{tech}.csv")
    PBT_merged.to_csv(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Payback-time\\{satellite_account}\\All.csv")

    print("   plot")
    color_map = {
        '<b>PV': '#ffc24b',
        '<b>Onshore wind': '#219ebc',
        '<b>Offshore wind': '#219ebc', 
        }
    
    to_plot = PBT_merged.reset_index()
    for tech,name in caps.items():
        to_plot = to_plot.replace(tech,f"<b>{name}")
    
    fig = px.box(
        to_plot,
        x = 'Activity to',
        y = 'Value',
        color = 'Activity to',
        color_discrete_map = color_map,
        points='all'
        )
    
    if satellite_account == 'GHGs':
        title = '<b>GHG payback time of PV, onshore and offshore wind technology <br>Sensitivity on Exiobase v3.8.2 2011-2019 and capacity factors | Refined with MARIO into Endogenous capital model'
    if satellite_account == 'Energy Carrier Supply - Total':
        title = '<b>Energy payback time of PV, onshore and offshore wind technology <br>Sensitivity on Exiobase v3.8.2 2011-2019 and capacity factors | Refined with MARIO into Endogenous capital model'
    
    fig.update_layout(
        title = title,
        showlegend=False,
        yaxis_range=[0,max(to_plot['Value']*1.2)],
        yaxis_title='<b>Months',
        xaxis_title=None,
        template = 'plotly_white',
        font_family = 'HelveticaNeue Light',
        )
    
    if satellite_account == 'GHGs':
        fig.write_html('Plots/GHGPBT.html', auto_open=True)
    if satellite_account == 'Energy Carrier Supply - Total':
        fig.write_html('Plots/EPBT.html', auto_open=True)

    
#%% EROI
satellite_account = 'Energy Carrier Supply - Total'
    
print(f"\n{satellite_account}")

print("   read and aggregate footprints")
f = pd.read_csv(
    f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\Footprints - Physical units\\{satellite_account}.csv",
    index_col=[0,1,2,3,4],
    )
f['Scenario'] = [i.split(' - ')[0] for i in f.index.get_level_values('Scenario')]
f = f.query("Scenario==@price_logics")
f = f.drop('Scenario',axis=1)

f = f.groupby(['Activity to','Scenario']).sum()
f['Scenario'] = [i.split(' - ')[0] for i in f.index.get_level_values('Scenario')]
f['Year'] = [i.split(' - ')[1] for i in f.index.get_level_values('Scenario')]
f['Performance'] = [i.split(' - ')[2] for i in f.index.get_level_values('Scenario')]

scenarios = sorted(list(set(f.index.get_level_values('Scenario'))))
f = f.droplevel('Scenario')
f.reset_index(inplace=True)

print("   parse tables")
world = {}
for scenario in scenarios:
    if scenario.split(' - ')[0] in price_logics:
        world[scenario] = mario.parse_from_txt(f"{pd.read_excel(paths, index_col=[0]).loc['Database',user]}\\d. Shock - Endogenization of capital\\{scenario}\\coefficients", table='SUT', mode="coefficients")

print("   calc denominator")
IN = {}

for tech in caps:
    IN[tech] = pd.DataFrame()
    for scenario in scenarios:
        
        s = scenario.split(' - ')[0]
        y = scenario.split(' - ')[1]
        p = scenario.split(' - ')[2]
        
        value = f.query(f"`Activity to`=='{tech}' & Scenario==@s & Year==@y & Performance==@p")
        value.set_index(['Activity to','Scenario','Year','Performance'],inplace=True)
        
        IN[tech] = pd.concat([IN[tech],value],axis=0)
   
    
print("   calc numerator")
OUT = {}

for tech in caps:
    OUT[tech] = pd.DataFrame()
    for scenario in scenarios:
        
        s = scenario.split(' - ')[0]
        y = scenario.split(' - ')[1]
        p = scenario.split(' - ')[2]
        
        value = pd.DataFrame(
            8760*lifetime[p][caps[tech]]*cf[p][caps[tech]]/1000,
            index=pd.MultiIndex.from_arrays([[tech],[s],[y],[p]], names=['Activity to','Scenario','Year','Performance']),
            columns=['Value']
            )
        
        OUT[tech] = pd.concat([OUT[tech],value],axis=0)


print("   calc EROI")
from copy import deepcopy as dc
EROI = dc(OUT)
EROI_merged = pd.DataFrame()

for tech in caps:
    for scenario in scenarios:
    
        s = scenario.split(' - ')[0]
        y = scenario.split(' - ')[1]
        p = scenario.split(' - ')[2]
    
        EROI[tech].loc[(tech,s,y,p),'Value'] /= IN[tech].loc[(tech,s,y,p),'Value']
        
    EROI_merged = pd.concat([EROI_merged,EROI[tech]],axis=0)


print("   export csvs")
for tech in caps:
    EROI[tech].to_csv(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\EROI\\{tech}.csv")
EROI_merged.to_csv(f"{pd.read_excel(paths, index_col=[0]).loc['Results',user]}\\EROI\\All.csv")


print("   plot")
color_map = {
    '<b>PV': '#ffc24b',
    '<b>Onshore wind': '#219ebc',
    '<b>Offshore wind': '#219ebc', 
    }

to_plot = EROI_merged.reset_index()
for tech,name in caps.items():
    to_plot = to_plot.replace(tech,f"<b>{name}")

fig = px.box(
    to_plot,
    x = 'Activity to',
    y = 'Value',
    color = 'Activity to',
    color_discrete_map = color_map,
    points='all'
    )

title = '<b>Energy Return on Investment (EROI) of PV, onshore and offshore wind technology <br>Sensitivity on Exiobase v3.8.2 2011-2019, capacity factors and lifetime | Refined with MARIO into Endogenous capital model'

fig.update_layout(
    title = title,
    showlegend=False,
    yaxis_range=[0,max(to_plot['Value']*1.2)],
    yaxis_title=None,
    xaxis_title=None,
    template = 'plotly_white',
    font_family = 'HelveticaNeue Light',
    )

fig.write_html('Plots/EROI.html', auto_open=True)



        