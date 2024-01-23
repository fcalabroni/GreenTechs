# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 12:15:53 2024

@author: carol
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
import pandas as pd
from scipy.interpolate import interp1d

#%% Off Eur

#Dati noti
known_years = np.array([2018,2023, 2030,2050,2100])
perc_off_eur = np.array([0.104683397, 0.137148367,0.27895, 0.449755, 0.716086132])

# Rimuovi i valori vuoti (NaN)
known_years_non_nan = known_years[~np.isnan(perc_off_eur)]
perc_off_eur_knwon_non_nan = perc_off_eur[~np.isnan(perc_off_eur)]

# Crea la funzione di interpolazione monotona
pchip_interp_off_eur = PchipInterpolator(known_years_non_nan, perc_off_eur_knwon_non_nan)

# Crea un array di valori x per l'interpolazione
years_interp = np.linspace(2018, 2100, 83)

# Calcola i valori interpolati
interp_off_eur = pchip_interp_off_eur(years_interp)

# Visualizza i risultati
plt.scatter(known_years_non_nan, perc_off_eur_knwon_non_nan, label='Known data', color='red')
plt.plot(years_interp, interp_off_eur, label='Interpolation', linestyle='--')
plt.legend()
plt.xlabel('Year')
plt.ylabel('Offshore percentage in Europe')
plt.title('% offshore Eur')
plt.show()

# Creare un DataFCu con i dati interpolati
interpolated_data_off_eur = pd.DataFrame({
    'Year': years_interp,
    'Offshore % - Europe': interp_off_eur
})
#%% Chn

#Dati noti
known_years = np.array([2018,2023, 2030,2050,2100])
perc_off_chn = np.array([0.024845006,0.089886989,0.1237, 0.26734,0.647834733
])

# Rimuovi i valori vuoti (NaN)
known_years_non_nan = known_years[~np.isnan(perc_off_chn)]
perc_off_chn_knwon_non_nan = perc_off_chn[~np.isnan(perc_off_chn)]

# Crea la funzione di interpolazione monotona
pchip_interp_off_chn = PchipInterpolator(known_years_non_nan, perc_off_chn_knwon_non_nan)

# Crea un array di valori x per l'interpolazione
years_interp = np.linspace(2018, 2100, 83)

# Calcola i valori interpolati
interp_off_chn = pchip_interp_off_chn(years_interp)

# Visualizza i risultati
plt.scatter(known_years_non_nan, perc_off_chn_knwon_non_nan, label='Known data', color='red')
plt.plot(years_interp, interp_off_chn, label='Interpolation', linestyle='--')
plt.legend()
plt.xlabel('Year')
plt.ylabel('Offshore percentage in China')
plt.title('% offshore China')
plt.show()

# Creare un DataFCu con i dati interpolati
interpolated_data_off_chn = pd.DataFrame({
    'Year': years_interp,
    'Offshore % - China': interp_off_chn
})
#%% USA

#Dati noti
known_years = np.array([2018,2023, 2030,2050,2100])
perc_off_usa = np.array([0.000309509,0.000335041382247631,0.10299,0.21284,0.379696864])

# Rimuovi i valori vuoti (NaN)
known_years_non_nan = known_years[~np.isnan(perc_off_usa)]
perc_off_usa_knwon_non_nan = perc_off_usa[~np.isnan(perc_off_usa)]

# Crea la funzione di interpolazione monotona
pchip_interp_off_usa = PchipInterpolator(known_years_non_nan, perc_off_usa_knwon_non_nan)

# Crea un array di valori x per l'interpolazione
years_interp = np.linspace(2018, 2100, 83)

# Calcola i valori interpolati
interp_off_usa = pchip_interp_off_usa(years_interp)

# Visualizza i risultati
plt.scatter(known_years_non_nan, perc_off_usa_knwon_non_nan, label='Known data', color='red')
plt.plot(years_interp, interp_off_usa, label='Interpolation', linestyle='--')
plt.legend()
plt.xlabel('Year')
plt.ylabel('Offshore percentage in USA')
plt.title('% offshore USA')
plt.show()

# Creare un DataFCu con i dati interpolati
interpolated_data_off_usa = pd.DataFrame({
    'Year': years_interp,
    'Offshore % - USA': interp_off_usa
})

#%% RoW

#Dati noti
known_years = np.array([2018,2023, 2030,2050,2100])
perc_off_RoW = np.array([0.066230235,0.088638392,0.24684,0.2821021,0.322864064
])

# Rimuovi i valori vuoti (NaN)
known_years_non_nan = known_years[~np.isnan(perc_off_RoW)]
perc_off_RoW_knwon_non_nan = perc_off_RoW[~np.isnan(perc_off_RoW)]

# Crea la funzione di interpolazione monotona
pchip_interp_off_RoW = PchipInterpolator(known_years_non_nan, perc_off_RoW_knwon_non_nan)

# Crea un array di valori x per l'interpolazione
years_interp = np.linspace(2018, 2100, 83)

# Calcola i valori interpolati
interp_off_RoW = pchip_interp_off_RoW(years_interp)

# Visualizza i risultati
plt.scatter(known_years_non_nan, perc_off_RoW_knwon_non_nan, label='Known data', color='red')
plt.plot(years_interp, interp_off_RoW, label='Interpolation', linestyle='--')
plt.legend()
plt.xlabel('Year')
plt.ylabel('Offshore percentage in RoW')
plt.title('% offshore RoW')
plt.show()

# Creare un DataFCu con i dati interpolati
interpolated_data_off_RoW = pd.DataFrame({
    'Year': years_interp,
    'Offshore % - RoW': interp_off_RoW
})