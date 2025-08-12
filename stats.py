import pandas as pd
import numpy as np

# Fonction pour lire la température depuis un fichier EPW
def read_epw_temperature(filepath):
    with open(filepath, 'r', encoding='ISO-8859-1') as f:
        lines = f.readlines()
    # On saute les 8 lignes d'en-tête puis on découpe en colonnes
    data = [line.strip().split(',') for line in lines[8:]]
    df = pd.DataFrame(data)
    # Colonne 6 (index 6) = Température sèche (Dry Bulb Temperature en °C)
    df[6] = pd.to_numeric(df[6], errors='coerce')
    return df[6]

# Chargement des trois fichiers
temp_actual = read_epw_temperature("SIMUL/Ziguinchor.epw")
temp_2050 = read_epw_temperature("SIMUL/Ziguinchor2050.epw")
temp_2080 = read_epw_temperature("SIMUL/Ziguinchor2080.epw")

# Fonction pour calculer les statistiques
def temperature_stats(series):
    return {
        "Mean (°C)": np.mean(series),
        "Min (°C)": np.min(series),
        "Max (°C)": np.max(series),
        "Std Dev (°C)": np.std(series),
        "5th Percentile (°C)": np.percentile(series, 5),
        "95th Percentile (°C)": np.percentile(series, 95)
    }

# Calcul des statistiques pour chaque fichier
stats_actual = temperature_stats(temp_actual)
stats_2050 = temperature_stats(temp_2050)
stats_2080 = temperature_stats(temp_2080)

# Affichage des résultats
print("=== Actuel ===")
print(stats_actual)
print("\n=== Projection 2050 ===")
print(stats_2050)
print("\n=== Projection 2080 ===")
print(stats_2080)
