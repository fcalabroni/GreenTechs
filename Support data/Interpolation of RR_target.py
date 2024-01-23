import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
import pandas as pd
#%% Copper

#Dati noti
known_years = np.array([2023, 2030,2050,2100])
Cu_RR_knwon = np.array([0.5,0.6, 0.798338412,1.0])

# Rimuovi i valori vuoti (NaN)
known_years_non_nan = known_years[~np.isnan(Cu_RR_knwon)]
Cu_RR_knwon_non_nan = Cu_RR_knwon[~np.isnan(Cu_RR_knwon)]

# Crea la funzione di interpolazione monotona
pchip_interp_Cu = PchipInterpolator(known_years_non_nan, Cu_RR_knwon_non_nan)

# Crea un array di valori x per l'interpolazione
years_interp = np.linspace(2023, 2100, 78)

# Calcola i valori interpolati
RR_interp_Cu = pchip_interp_Cu(years_interp)

# Visualizza i risultati
plt.scatter(known_years_non_nan, Cu_RR_knwon_non_nan, label='Known data', color='red')
plt.plot(years_interp, RR_interp_Cu, label='Interpolation', linestyle='--')
plt.legend()
plt.xlabel('Year')
plt.ylabel('Cu concentration')
plt.title('Copper')
plt.show()

# Creare un DataFCu con i dati interpolati
interpolated_data_Cu = pd.DataFrame({
    'Year': years_interp,
    'RR Cu': RR_interp_Cu
})

#%% Plot for RR of Dysprosium
# Dati noti
known_years = np.array([2023, 2030, 2050, 2100])
Dy_RR_knwon = np.array([0, 0.15, 0.16, 0.9])

# Rimuovi i valori vuoti (NaN)
known_years_non_nan = known_years[~np.isnan(Dy_RR_knwon)]
Dy_RR_knwon_non_nan = Dy_RR_knwon[~np.isnan(Dy_RR_knwon)]

# Crea la funzione di interpolazione monotona
pchip_interp_Dy = PchipInterpolator(known_years_non_nan, Dy_RR_knwon_non_nan)

# Crea un array di valori x per l'interpolazione
years_interp = np.linspace(2023, 2100, 78)

# Calcola i valori interpolati
RR_interp_Dy = pchip_interp_Dy(years_interp)

# Visualizza i risultati
plt.scatter(known_years_non_nan, Dy_RR_knwon_non_nan, label='Known data', color='red')
plt.plot(years_interp, RR_interp_Dy, label='Interpolation', linestyle='--')
plt.legend()
plt.xlabel('Years')
plt.ylabel('Dysprosium RR')
plt.title('Interpolation of Dysprosium Recycling Rate')
plt.show()

# Creare un DataFrame con i dati interpolati
interpolated_data_Dy = pd.DataFrame({
    'Year': years_interp,
    'RR Dysprosium': RR_interp_Dy
})

#%% Plot for RR of Nd
#Dati noti
known_years = np.array([2023, 2030, 2050,2100])
Nd_RR_knwon = np.array([0, 0.15, 0.21,0.9])

# Rimuovi i valori vuoti (NaN)
known_years_non_nan = known_years[~np.isnan(Nd_RR_knwon)]
Nd_RR_knwon_non_nan = Nd_RR_knwon[~np.isnan(Nd_RR_knwon)]

# Crea la funzione di interpolazione monotona
pchip_interp_Nd = PchipInterpolator(known_years_non_nan, Nd_RR_knwon_non_nan)

# Crea un array di valori x per l'interpolazione
years_interp = np.linspace(2023, 2100, 78)

# Calcola i valori interpolati
RR_interp_Nd = pchip_interp_Nd(years_interp)

# Visualizza i risultati
plt.scatter(known_years_non_nan, Nd_RR_knwon_non_nan, label='Known data', color='red')
plt.plot(years_interp, RR_interp_Nd, label='Interpolation', linestyle='--')
plt.legend()
plt.xlabel('Years')
plt.ylabel('Nd RR')
plt.title('Interpolation of Neodymium Recycling Rate')
plt.show()

# Creare un DataFrame con i dati interpolati
interpolated_data_Nd = pd.DataFrame({
    'Years': years_interp,
    'RR interp Nd': RR_interp_Nd
})

#%% Plot for RR of Si
# Dati noti
known_years = np.array([2023, 2030, 2050, 2100])
Si_RR_knwon = np.array([0.01, 0.15, 0.345187847, 0.9])

# Rimuovi i valori vuoti (NaN)
known_years_non_nan = known_years[~np.isnan(Si_RR_knwon)]
Si_RR_knwon_non_nan = Si_RR_knwon[~np.isnan(Si_RR_knwon)]

# Crea la funzione di interpolazione monotona
pchip_interp_Si = PchipInterpolator(known_years_non_nan, Si_RR_knwon_non_nan)

# Crea un array di valori x per l'interpolazione
years_interp = np.linspace(2023, 2100, 78)

# Calcola i valori interpolati
RR_interp_Si = pchip_interp_Si(years_interp)

# Visualizza i risultati
plt.scatter(known_years_non_nan, Si_RR_knwon_non_nan, label='Known data', color='red')
plt.plot(years_interp, RR_interp_Si, label='Interpolation', linestyle='--')
plt.legend()
plt.xlabel('Years')
plt.ylabel('Si RR')
plt.title('Interpolation of Silicon Recycling Rate')
plt.show()

# Creare un DataFrame con i dati interpolati
interpolated_data_Si = pd.DataFrame({
    'Years': years_interp,
    'RR interp Si': RR_interp_Si
})