#%%

import plotly.express as px
import pandas as pd

file_path = 'C:\\Users\\carol\\OneDrive - Politecnico di Milano\\2022-23_WasteMARIO\\dMRWIO model\\dMRWIO\\Data Heatmap.xlsx'

custom_color_scale = ['#70d6ff', '#ff70a6']

# Read data and create heatmaps
dataDy = pd.read_excel(file_path, "Dy", index_col=[0])
fig1 = px.imshow(dataDy, color_continuous_scale='Rdbu', title='Dysprosium')
fig1.show()
fig1.write_image("plot1.png")

dataNd = pd.read_excel(file_path, "Nd (2)", index_col=[0])
fig2 = px.imshow(dataNd, color_continuous_scale=custom_color_scale, title='Neodymium')
fig2.show()
fig2.write_image("plot2.png")

dataCu = pd.read_excel(file_path, "Cu", index_col=[0])
fig3 = px.imshow(dataCu, color_continuous_scale='Rdbu', title='Copper')
fig3.show()
fig3.write_image("plot3.png")

dataSi = pd.read_excel(file_path, "Si", index_col=[0])
fig4 = px.imshow(dataSi, color_continuous_scale='Rdbu', title='Raw silicon')
fig4.show()
fig4.write_image("plot4.png")

dataDiff = pd.read_excel(file_path, "price min", index_col=[0])
fig5 = px.imshow(dataDiff, color_continuous_scale='Rdbu', title='Minimum price')
fig5.show()
fig5.write_image("plot5.png")
#%%
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd

file_path = 'C:\\Users\\carol\\OneDrive - Politecnico di Milano\\2022-23_WasteMARIO\\dMRWIO model\\dMRWIO\\Data Heatmap.xlsx'

# Read data
dataDy = pd.read_excel(file_path, "Dy", index_col=[0])
dataNd = pd.read_excel(file_path, "Nd", index_col=[0])
dataCu = pd.read_excel(file_path, "Cu", index_col=[0])
dataSi = pd.read_excel(file_path, "Si", index_col=[0])

# Create subplots
fig = make_subplots(rows=2, cols=2, subplot_titles=("Dysprosium", "Neodymium", "Copper", "Raw Silicon"))

# Add heatmaps to subplots
fig.add_trace(go.Heatmap(z=dataDy, colorscale='haline'), row=1, col=1)
fig.add_trace(go.Heatmap(z=dataNd, colorscale='orrd'), row=1, col=2)
fig.add_trace(go.Heatmap(z=dataCu, colorscale='orrd'), row=2, col=1)
fig.add_trace(go.Heatmap(z=dataSi, colorscale='orrd'), row=2, col=2)

# Update layout
fig.update_layout(height=600, width=800)

# Show the plot
fig.show()
fig.write_image("plot.png")

#%%

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = 'C:\\Users\\carol\\OneDrive - Politecnico di Milano\\2022-23_WasteMARIO\\dMRWIO model\\dMRWIO\\Data Heatmap.xlsx'
dataNd = pd.read_excel(file_path, "Nd", index_col=[0])
price_sens_Nd = dataNd.iloc[:, :]

# Creazione della figura e degli assi
fig, ax = plt.subplots(figsize=(10,6))

# Posizioni degli Years sull'asse y
Years = price_sens_Nd.index

# Larghezza delle barre
bar_width = 6.5

# Creazione degli istogrammi con stile
rects1 = ax.barh(Years, price_sens_Nd.iloc[:, 0], bar_width, label='Minimum price', color='#f78c6b', edgecolor='#f78c6b')
rects2 = ax.barh(Years, price_sens_Nd.iloc[:, 1], bar_width, label='Maximum price', color='#f9c74f', edgecolor='#f9c74f')

# Offset verticale per rects3 e rects4
offset_y = 6.5

rects3 = ax.barh(Years - offset_y, price_sens_Nd.iloc[:, 2], bar_width, label='Minimum lifetime', color='#f05006', edgecolor='#f05006')
rects4 = ax.barh(Years - offset_y, price_sens_Nd.iloc[:, 3], bar_width, label='Maximum lifetime', color='#ff9633', edgecolor='#ff9633')

# Aggiunta di una linea verticale per rappresentare le "Reserves"
plt.axvline(x=0, linestyle='--', color='gray', linewidth=1)

# Aggiunta di etichette e titoli
ax.set_xlabel('Valore')
ax.set_ylabel('Years')
ax.set_title('Price and Lifetime Sensitivity for Neodymium')
ax.set_yticks(Years)
ax.set_yticklabels(price_sens_Nd.index)
ax.legend()

# Aggiunta di griglie sia sull'asse x che sull'asse y
ax.xaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

plt.show()

#%%
dataDy = pd.read_excel(file_path, "Dy", index_col=[0])
price_sens_Dy = dataDy.iloc[:, :]

# Creazione della figura e degli assi
fig, ax = plt.subplots(figsize=(10,6))

# Posizioni degli Years sull'asse y
Years = price_sens_Dy.index

# Larghezza delle barre
bar_width = 6.5

# Creazione degli istogrammi con stile
rects1 = ax.barh(Years, price_sens_Dy.iloc[:, 0], bar_width, label='Minimum price', color='#f78c6b', edgecolor='#f78c6b')
rects2 = ax.barh(Years, price_sens_Dy.iloc[:, 1], bar_width, label='Maximum price', color='#f9c74f', edgecolor='#f9c74f')

# Offset verticale per rects3 e rects4
offset_y = 6.5

rects3 = ax.barh(Years - offset_y, price_sens_Dy.iloc[:, 2], bar_width, label='Minimum lifetime', color='#f05006', edgecolor='#f05006')
rects4 = ax.barh(Years - offset_y, price_sens_Dy.iloc[:, 3], bar_width, label='Minimum lifetime', color='#ff9633', edgecolor='#ff9633')

# Aggiunta di una linea verticale per rappresentare le "Reserves"
plt.axvline(x=0, linestyle='--', color='gray', linewidth=1)

# Aggiunta di etichette e titoli
ax.set_xlabel('Valore')
ax.set_ylabel('Years')
ax.set_title('Price and Lifetime Sensitivity for Dysprosium')
ax.set_yticks(Years)
ax.set_yticklabels(price_sens_Dy.index)
ax.legend()

# Aggiunta di griglie sia sull'asse x che sull'asse y
ax.xaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

plt.show()

#%%
dataCu = pd.read_excel(file_path, "Cu", index_col=[0])
price_sens_Cu = dataCu.iloc[:, :]

# Creazione della figura e degli assi
fig, ax = plt.subplots(figsize=(10,6))

# Posizioni degli Years sull'asse y
Years = price_sens_Cu.index

# Larghezza delle barre
bar_width = 6.5

# Creazione degli istogrammi con stile
rects1 = ax.barh(Years, price_sens_Cu.iloc[:, 0], bar_width, label='Minimum price', color='#f78c6b', edgecolor='#f78c6b')
rects2 = ax.barh(Years, price_sens_Cu.iloc[:, 1], bar_width, label='Maximum price', color='#f9c74f', edgecolor='#f9c74f')

# Offset verticale per rects3 e rects4
offset_y = 6.5

rects3 = ax.barh(Years - offset_y, price_sens_Cu.iloc[:, 2], bar_width, label='Minimum lifetime', color='#f05006', edgecolor='#f05006')
rects4 = ax.barh(Years - offset_y, price_sens_Cu.iloc[:, 3], bar_width, label='Minimum lifetime', color='#ff9633', edgecolor='#ff9633')

# Aggiunta di una linea verticale per rappresentare le "Reserves"
plt.axvline(x=0, linestyle='--', color='gray', linewidth=1)

# Aggiunta di etichette e titoli
ax.set_xlabel('Valore')
ax.set_ylabel('Years')
ax.set_title('Price and Lifetime Sensitivity for Copper')
ax.set_yticks(Years)
ax.set_yticklabels(price_sens_Cu.index)
ax.legend()

# Aggiunta di griglie sia sull'asse x che sull'asse y
ax.xaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

plt.show()

#%%
dataSi = pd.read_excel(file_path, "Si", index_col=[0])
price_sens_Si = dataSi.iloc[:, :]

# Creazione della figura e degli assi
fig, ax = plt.subplots(figsize=(10,6))

# Posizioni degli Years sull'asse y
Years = price_sens_Si.index

# Larghezza delle barre
bar_width = 6.5

# Creazione degli istogrammi con stile
rects1 = ax.barh(Years, price_sens_Si.iloc[:, 0], bar_width, label='Minimum price', color='#f78c6b', edgecolor='#f78c6b')
rects2 = ax.barh(Years, price_sens_Si.iloc[:, 1], bar_width, label='Maximum price', color='#f9c74f', edgecolor='#f9c74f')

# Offset verticale per rects3 e rects4
offset_y = 6.5

rects3 = ax.barh(Years - offset_y, price_sens_Si.iloc[:, 2], bar_width, label='Minimum lifetime', color='#f05006', edgecolor='#f05006')
rects4 = ax.barh(Years - offset_y, price_sens_Si.iloc[:, 3], bar_width, label='Minimum lifetime', color='#ff9633', edgecolor='#ff9633')

# Aggiunta di una linea verticale per rappresentare le "Reserves"
plt.axvline(x=0, linestyle='--', color='gray', linewidth=1)

# Aggiunta di etichette e titoli
ax.set_xlabel('Valore')
ax.set_ylabel('Years')
ax.set_title('Price and Lifetime Sensitivity for Raw silicon')
ax.set_yticks(Years)
ax.set_yticklabels(price_sens_Si.index)
ax.legend()

# Aggiunta di griglie sia sull'asse x che sull'asse y
ax.xaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

plt.show()

#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = 'C:\\Users\\carol\\OneDrive - Politecnico di Milano\\2022-23_WasteMARIO\\dMRWIO model\\dMRWIO\\Data Heatmap.xlsx'

# Load data for each element
dataNd = pd.read_excel(file_path, "Nd", index_col=[0])
dataDy = pd.read_excel(file_path, "Dy", index_col=[0])
dataCu = pd.read_excel(file_path, "Cu", index_col=[0])
dataSi = pd.read_excel(file_path, "Si", index_col=[0])

# Create a figure with 2x2 subplot layout
fig, axs = plt.subplots(2, 2, figsize=(15, 10), sharex=True)

# Flatten the 2x2 subplot array to simplify indexing
axs = axs.flatten()

# Define bar width
bar_width = 6.5
# Define offset for centering the year between bars
offset_y = 3.25

# Plot for Neodymium
Years_nd = dataNd.index
# rects1_nd = axs[0].barh(Years_nd + offset_y, dataNd.iloc[:, 0], bar_width, label='Minimum price', color='#d94165', edgecolor='#d94165',alpha=0.9)
# rects2_nd = axs[0].barh(Years_nd + offset_y, dataNd.iloc[:, 1], bar_width, label='Maximum price', color='#f78c6b', edgecolor='#f78c6b',alpha=0.9)
rects3_nd = axs[0].barh(Years_nd - offset_y, dataNd.iloc[:, 2], bar_width, label='Minimum lifetime', color='#0c637f', edgecolor='#0c637f',alpha=0.9)
rects4_nd = axs[0].barh(Years_nd - offset_y, dataNd.iloc[:, 3], bar_width, label='Maximum lifetime', color='#0cb0a9', edgecolor='#0cb0a9',alpha=0.9)
axs[0].axvline(x=0, linestyle='-', color='gray', linewidth=1)
axs[0].set_yticks(Years_nd)
axs[0].set_yticklabels(dataNd.index,fontsize='xx-large')

# axs[0].set_xlabel('Valore')
axs[0].set_ylabel('Years', fontsize = 'xx-large')
axs[0].margins( y=0)

axs[0].xaxis.grid(True, linestyle='-', linewidth=0.5, alpha=0.7)
# axs[0].yaxis.grid(True, linestyle='-', linewidth=0.5, alpha=0.7)
axs[0].set_title('Neodymium',fontsize='xx-large')

# Plot for Dysprosium
Years_dy = dataDy.index
# rects1_dy = axs[1].barh(Years_dy + offset_y, dataDy.iloc[:, 0], bar_width, label='Dysprosium Minimum price', color='#d94165', edgecolor='#d94165',alpha=0.9)
# rects2_dy = axs[1].barh(Years_dy + offset_y, dataDy.iloc[:, 1], bar_width, label='Dysprosium Maximum price', color='#f78c6b', edgecolor='#f78c6b',alpha=0.9)
rects3_dy = axs[1].barh(Years_dy - offset_y, dataDy.iloc[:, 2], bar_width, label='Dysprosium Minimum lifetime', color='#0c637f', edgecolor='#0c637f',alpha=0.9)
rects4_dy = axs[1].barh(Years_dy - offset_y, dataDy.iloc[:, 3], bar_width, label='Dysprosium Minimum lifetime', color='#0cb0a9', edgecolor='#0cb0a9',alpha=0.9)
axs[1].axvline(x=0, linestyle='-', color='gray', linewidth=1)
axs[1].set_yticks(Years_dy)
# axs[1].set_xlabel('Valore')
axs[1].set_ylabel('Years',fontsize = 'xx-large')
axs[1].set_yticklabels(dataDy.index,fontsize='xx-large')
axs[1].margins(y=0)

# axs[1].legend()
axs[1].xaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
# axs[1].yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
axs[1].set_title('Dysprosium',fontsize='xx-large')

# Plot for Copper
Years_cu = dataCu.index
# rects1_cu = axs[2].barh(Years_cu + offset_y, dataCu.iloc[:, 0], bar_width, label='Copper Minimum price', color='#d94165', edgecolor='#d94165',alpha=0.9)
# rects2_cu = axs[2].barh(Years_cu + offset_y, dataCu.iloc[:, 1], bar_width, label='Copper Maximum price', color='#f78c6b', edgecolor='#f78c6b',alpha=0.9)
rects3_cu = axs[2].barh(Years_cu - offset_y, dataCu.iloc[:, 2], bar_width, label='Copper Minimum lifetime', color='#0c637f', edgecolor='#0c637f',alpha=0.9)
rects4_cu = axs[2].barh(Years_cu - offset_y, dataCu.iloc[:, 3], bar_width, label='Copper Minimum lifetime', color='#0cb0a9', edgecolor='#0cb0a9',alpha=0.9)
axs[2].axvline(x=0, linestyle='-', color='gray', linewidth=1)
axs[2].set_yticks(Years_cu)
axs[2].set_yticklabels(dataCu.index,fontsize='xx-large')
axs[2].set_ylabel('Years',fontsize = 'xx-large')
# axs[2].legend()
axs[2].margins(y=0)

axs[2].xaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
# axs[2].yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
axs[2].set_title('Copper',fontsize='xx-large')
axs[2].set_xticks([-0.5,0, 0.5,1, 1.50])  # Customize as needed
axs[2].set_xticklabels(['-0.5','0', '0.5', '1', '1.5'], fontsize='xx-large')  # Customize as needed
axs[2].set_xlabel('%',fontsize = 'xx-large')

# Plot for Raw silicon
Years_si = dataSi.index
# rects1_si = axs[3].barh(Years_si + offset_y, dataSi.iloc[:, 0], bar_width, label='Minimum price', color='#d94165', edgecolor='#d94165',alpha=0.9)
# rects2_si = axs[3].barh(Years_si + offset_y, dataSi.iloc[:, 1], bar_width, label='Maximum price', color='#f78c6b', edgecolor='#f78c6b',alpha=0.9)
rects3_si = axs[3].barh(Years_si - offset_y, dataSi.iloc[:, 2], bar_width, label='Minimum lifetime', color='#0c637f', edgecolor='#0c637f',alpha=0.9)
rects4_si = axs[3].barh(Years_si - offset_y, dataSi.iloc[:, 3], bar_width, label='Maximum lifetime', color='#0cb0a9', edgecolor='#0cb0a9',alpha=0.9)
axs[3].axvline(x=0, linestyle='-', color='gray', linewidth=1)
axs[3].set_yticks(Years_si)
axs[3].set_ylabel('Years',fontsize = 'xx-large')
axs[3].set_yticklabels(dataSi.index, fontsize='xx-large')
axs[3].set_xticks([-0.5,0, 0.5,1, 1.50])  # Customize as needed
axs[3].set_xticklabels(['-50','0', '50', '100', '150'], fontsize='xx-large')  # Customize as needed
axs[3].set_xlabel('%',fontsize = 'xx-large')

axs[3].legend(fontsize='x-large')
axs[3].margins(y=0)

# axs[3].legend()
axs[3].xaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
# axs[3].yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
axs[3].set_title('Raw silicon',fontsize='xx-large')

plt.tight_layout()

ax.tick_params(axis='x', labelsize='xx-large')
plt.show()


#%%

import pandas as pd
import matplotlib.pyplot as plt

# Load data for each element
file_path = 'C:\\Users\\carol\\OneDrive - Politecnico di Milano\\2022-23_WasteMARIO\\dMRWIO model\\dMRWIO\\Data Heatmap.xlsx'
dataNd = pd.read_excel(file_path, "Nd", index_col=[0])
dataDy = pd.read_excel(file_path, "Dy", index_col=[0])
dataCu = pd.read_excel(file_path, "Cu", index_col=[0])
dataSi = pd.read_excel(file_path, "Si", index_col=[0])

# Create a figure with 2x2 subplot layout
fig, axs = plt.subplots(1, 3, figsize=(16,7), sharex=True,sharey =True)

# Flatten the 2x2 subplot array to simplify indexing
axs = axs.flatten()

# Define bar width
bar_width = 4
# Define offset for centering the year between bars
offset_y = 3.25

# Plot for Neodymium
# Years_nd = dataNd.index
# rects3_nd = axs[0].barh(Years_nd, dataNd.iloc[:, 0], bar_width, label='Minimum lifetime', color='#0c637f', edgecolor='#0c637f', alpha=0.9)
# rects4_nd = axs[0].barh(Years_nd, dataNd.iloc[:, 1], bar_width, label='Maximum lifetime', color='#0cb0a9', edgecolor='#0cb0a9', alpha=0.9)
# axs[0].axvline(x=0, linestyle='-', color='gray', linewidth=1)
# axs[0].set_yticks([2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100])  # Years every 10 years
# axs[0].set_yticklabels(['2011', '2020', '2030', '2040', '2050', '2060', '2070', '2080', '2090', '2100'], fontsize='xx-large')
# axs[0].set_ylabel('Years', fontsize='xx-large')
# axs[0].margins(y=0)
# axs[0].xaxis.grid(True, linestyle='-', linewidth=0.5, alpha=0.7)
# axs[0].set_title('Neodymium', fontsize='xx-large')

# Plot for Dysprosium
Years_dy = dataDy.index
rects3_dy = axs[0].barh(Years_dy, dataDy.iloc[:, 0], bar_width, label='Minimum', color='#ffad88', edgecolor='#ffad88', alpha=0.9)
rects4_dy = axs[0].barh(Years_dy, dataDy.iloc[:, 1], bar_width, label='Maximum', color='#ff5c77', edgecolor='#ff5c77', alpha=0.9)
axs[0].axvline(x=0, linestyle='-', color='gray', linewidth=1)
axs[0].set_yticks([2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100])  # Years every 10 years
axs[0].set_yticklabels(['2011', '2020', '2030', '2040', '2050', '2060', '2070', '2080', '2090', '2100'], fontsize='xx-large')
axs[0].set_ylabel('Years', fontsize='xx-large')
axs[0].margins(y=0)
axs[0].set_xticks([-0.075, -0.05, -0.025, 0, 0.025, 0.05, 0.075,0.1])  # Customize as needed
axs[0].set_xticklabels(['-7.5', '-5', '2.5', '0', '2.5', '5', '7.5','10'], fontsize='xx-large')  # Customize as needed
axs[0].set_title('REE', fontsize='xx-large')
axs[0].yaxis.grid(True, linestyle='--', alpha=0.7)

# Plot for Copper
Years_cu = dataCu.index
rects3_cu = axs[1].barh(Years_cu, dataCu.iloc[:, 0], bar_width, label='Copper Minimum lifetime', color='#ffad88', edgecolor='#ffad88', alpha=0.9)
rects4_cu = axs[1].barh(Years_cu, dataCu.iloc[:, 1], bar_width, label='Copper Minimum lifetime', color='#ff5c77', edgecolor='#ff5c77', alpha=0.9)
axs[1].axvline(x=0, linestyle='-', color='gray', linewidth=1)
axs[1].set_yticks([2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100])  # Years every 10 years
axs[1].set_yticklabels(['2011', '2020', '2030', '2040', '2050', '2060', '2070', '2080', '2090', '2100'], fontsize='xx-large')
axs[1].margins(y=0)
axs[1].set_title('Copper', fontsize='xx-large')
axs[1].set_xticks([-0.1, -0.25, 0, 0.25, 0.1])  # Customize as needed
axs[1].set_xticklabels(['-10', '-5', '0', '5', '10'], fontsize='xx-large')  # Customize as needed
axs[1].set_xlabel('Percentage', fontsize='xx-large')
axs[1].yaxis.grid(True, linestyle='--', alpha=0.7)

# Plot for Raw silicon
Years_si = dataSi.index
rects3_si = axs[2].barh(Years_si, dataSi.iloc[:, 0], bar_width, label='Minimum lifetime', color='#ffad88', edgecolor='#ffad88', alpha=0.9)
rects4_si = axs[2].barh(Years_si, dataSi.iloc[:, 1], bar_width, label='Maximum lifetime', color='#ff5c77', edgecolor='#ff5c77', alpha=0.9)
axs[2].axvline(x=0, linestyle='-', color='gray', linewidth=1)
axs[2].set_yticks([2011, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100])  # Years every 10 years
axs[2].set_yticklabels(['2011', '2020', '2030', '2040', '2050', '2060', '2070', '2080', '2090', '2100'], fontsize='xx-large')
axs[2].set_xticks([-0.075, -0.05, -0.025, 0, 0.025, 0.05, 0.075,0.1])  # Customize as needed
axs[2].set_xticklabels(['-7.5', '-5', '2.5', '0', '2.5', '5', '7.5','10'], fontsize='xx-large')  # Customize as needed
axs[0].legend(fontsize='xx-large',loc = 'lower right')
axs[2].margins(y=0)
axs[2].yaxis.grid(True, linestyle='--',  alpha=0.7)

axs[2].set_title('Raw silicon', fontsize='xx-large')

plt.tight_layout()

fig = plt.gcf()

# Impostare una risoluzione elevata (dpi) per una migliore qualità
dpi = 300

# Esportare come PNG con alta risoluzione
fig.savefig('lifetime sensitivity.png', dpi=dpi, bbox_inches='tight')
plt.show()
