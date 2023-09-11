#%%
import pandas as pd

# read the file excel LCI.xlsx as a dictionary of dataframes, one for each sheet
df = pd.read_excel(
    # 'Offshore wind.xlsx', 
    # 'Photovoltaics.xlsx', 
    'Onshore wind.xlsx', 
    sheet_name=None,
    )
# %% assign the keys of df to a list but drop all the keys that starts with "_"
keys = list(df.keys())
keys = [x for x in keys if not x.startswith('_')]
# %%
# I want to query df['Subcomponent'] for all the rows where Subcomponent == 'Tower' and get the value of column "Weight"
# df['Subcomponent'].query('Subcomponent == "Tower"')['Weight']
 

levels = ['Factor of production','Commodity']
highest = 'Technology'
input = {}
res = {}

for level in levels:
    lowest = level

    add_col = {1: {'below': lowest,    'above': 'Subcomponent',  'col_name':'wCOMMinSUBC'}, 
            2: {'below': 'Subcomponent', 'above': 'Component',     'col_name':'wSUBCinCOMP'},
            3: {'below': 'Component',    'above': 'Section',       'col_name':'wCOMPinSECT'},
            4: {'below': 'Section',      'above': 'Technology',    'col_name':'wSECTinTECH'} }

    for r in range(len(df[lowest])):

        input[1] = df[lowest].loc[r,'Subcomponent']
        input[2] = df['Subcomponent'].query(f'Subcomponent == "{input[1]}"')['Component'].values[0]
        input[3] = df['Component'].query(f'Component == "{input[2]}"')['Section'].values[0]
        input[4] = df['Section'].query(f'Section == "{input[3]}"')['Technology'].values[0]

        for a in [2,3,4]:
            below = add_col[a]['below']
            above = add_col[a]['above']


            df[lowest].loc[r, above] = input[a]
            df[lowest].loc[r, add_col[a]['col_name']] = df[below].query(f"{above} == '{input[a]}' & {below} == '{input[a-1]}'")['Weight'].values[0]

    df[lowest]['Coeff'] = df[lowest]['Weight']* df[lowest]['wSUBCinCOMP'] * df[lowest]['wCOMPinSECT'] * df[lowest]['wSECTinTECH']
    
    if lowest == 'Factor of production':
        res[level] = df[level].loc[:,(lowest,'Coeff')].groupby(['Factor of production']).sum()

    else:
        res[level] = df[level].loc[:,(lowest,'Region','Coeff')].groupby(['Commodity','Region']).sum()

    res[level].set_index([x for x in res[level].columns if x != 'Coeff'], inplace=True)



# %%
