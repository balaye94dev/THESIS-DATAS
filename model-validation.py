import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from scipy.stats import linregress

# Chargement des données
df_model = pd.read_excel('cmip6_2024_dakar_cnrm_cm6_ssp245.xlsx')
df_obs = pd.read_excel('observation_2024_dakar.xlsx')

# Prétraitement des dates 
df_model['datetime'] = pd.to_datetime(df_model['time'])
df_obs['datetime'] = pd.to_datetime(df_obs['datetime'])

# Renommage des colonnes et conversion
df_model = df_model.rename(columns={'tasmax_ssp245': 'T_model'})
df_obs = df_obs.rename(columns={'tempmax': 'T_obs'})

# Diviser par 10 si les températures sont en dixièmes de degrés
df_model['T_model'] = df_model['T_model'] / 10


# Arrondir à la journée (si données journalières)
df_model['datetime'] = df_model['datetime'].dt.floor('D')
df_obs['datetime'] = df_obs['datetime'].dt.floor('D')

# Fusion des données 
df_merged = pd.merge(df_model[['datetime', 'T_model']],
                     df_obs[['datetime', 'T_obs']],
                     on='datetime', how='inner')

# Nettoyage
df_merged.dropna(inplace=True)

# Évaluation statistique 
biais = np.mean(df_merged['T_model'] - df_merged['T_obs'])
rmse = np.sqrt(mean_squared_error(df_merged['T_obs'], df_merged['T_model']))
mae = mean_absolute_error(df_merged['T_obs'], df_merged['T_model'])
corr = df_merged['T_model'].corr(df_merged['T_obs'])


# Visualisation comparative temporelle 
plt.figure(figsize=(12, 6))
plt.plot(df_merged['datetime'], df_merged['T_obs'], label='Observation (2024)', color='black')
plt.plot(df_merged['datetime'], df_merged['T_model'], label='Modèle CNRM-CM6', color='blue', alpha=0.7)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Température [°C]", fontsize=12)
plt.title("Comparaison des températures journalières - Dakar 2024", fontsize=14)
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("comparaison_temp_cnrm_cm6_dakar2024.png", dpi=300)
plt.show()

# Calcul de la régression linéaire
slope, intercept, r_value, p_value, std_err = linregress(df_merged['T_obs'], df_merged['T_model'])
reg_line = slope * df_merged['T_obs'] + intercept
r_squared = r_value ** 2

# Création du graphique
plt.figure(figsize=(6, 6))
plt.scatter(df_merged['T_obs'], df_merged['T_model'], alpha=0.5, color='blue', label='Données')
plt.plot(df_merged['T_obs'], reg_line, color='red',
         label=f"Régression : y = {slope:.2f}x + {intercept:.2f}\n$R² = {r_squared:.2f}$")
plt.plot([df_merged['T_obs'].min(), df_merged['T_obs'].max()],
         [df_merged['T_obs'].min(), df_merged['T_obs'].max()],
         'k--', label='y=x')

# Mise en forme scientifique
plt.xlabel("Température observée [°C]", fontsize=12)
plt.ylabel("Température simulée [°C]", fontsize=12)
plt.title("Régression linéaire - Dakar 2024", fontsize=14)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("regression_temp_cnrm_cm6_dakar2024.png", dpi=300)
plt.show()

# Tableau Statistique
stat_table = pd.DataFrame({
    'Indicateur': [
        'Biais',
        'RMSE (Erreur quadratique moyenne)',
        'MAE (Erreur absolue moyenne)',
        'Corrélation (r)',
        'Coefficient de détermination (R²)',
        'Pente (a)',
        'Ordonnée à l’origine (b)'
    ],
    'Valeur': [
        round(biais, 2),
        round(rmse, 2),
        round(mae, 2),
        round(r_value, 2),
        round(r_squared, 2),
        round(slope, 2),
        round(intercept, 2)
    ],
    'Unité': ['°C', '°C', '°C', '-', '-', '-', '°C']
})

# Affichage dans la console
print("\n=== Résumé statistique : CNRM-CM6 vs Observations Dakar 2024 ===")
print(stat_table.to_string(index=False))