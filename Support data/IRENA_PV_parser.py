import pandas as pd

path = "IRENA-Datafile-RenPwrGenCosts-in-2021-v1-0.xlsx"
sheet_names = {
    'cost_breakdown': 'Fig 3.5',
    'total_capex': 'Fig 3.3',
    }
ref_year = 2021

#%%
data = pd.read_excel(path,sheet_name=sheet_names['cost_breakdown'], skiprows=range(0,7), header=[1], index_col=[2,3]).iloc[:,2:]
data.reset_index(inplace=True)

data['Year'] = ref_year
data['Technology'] = 'Photovoltaic panels'

data.set_index(['Technology','Year','Category','Cost Component'], inplace=True)
data.index.names = ['Technology','Year','Parts of technology','Component']
data.columns.names = ['Scenario']

data = data.stack().to_frame()
data.columns = ['Component CAPEX']

#%%
# total_capex = pd.read_excel(path,sheet_name=sheet_names['total_capex'], skiprows=range(0,3), header=[0], index_col=[1]).iloc[:,1:]
# data['Technology CAPEX'] = total_capex.loc['Weighted average',ref_year]

data['Technology CAPEX'] = data.groupby(['Technology', 'Year', 'Scenario'])['Component CAPEX'].transform('sum')
data['Technology CAPEX'] = data.groupby(['Technology', 'Year', 'Scenario'])['Technology CAPEX'].transform('first')
data['Component CAPEX share'] = data['Component CAPEX'] / data['Technology CAPEX']

data.reset_index(inplace=True)
data.set_index(['Technology','Year','Scenario','Parts of technology','Component'], inplace=True)
data = data.sort_index(ascending=True)

#%%
data_germany = data.loc[(slice(None),slice(None),'Germany',slice(None),slice(None)),:]#.groupby(['Technology', 'Year', 'Scenario','Parts of technology']).sum()
