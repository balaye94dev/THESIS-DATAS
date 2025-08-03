import pandas as pd
import matplotlib.pyplot as plt

# Charger les données
df_access_cm2 = pd.read_excel('cmip6-dakar/cmip6_access_cm2_dakar.xlsx')
df_canESM5 = pd.read_excel('cmip6-dakar/cmip6_canESM5_dakar.xlsx')
df_cams_cm1 = pd.read_excel('cmip6-dakar/cmip6_cams_csm1_dakar.xlsx')
df_cnrm_cm6 = pd.read_excel('cmip6-dakar/cmip6_cnrm_cm6_dakar.xlsx')


df_canESM5['datetime'] = pd.to_datetime(df_canESM5['time'])
df_access_cm2['datetime'] = pd.to_datetime(df_access_cm2['time']) 
df_cams_cm1['datetime'] = pd.to_datetime(df_cams_cm1['time']) 
df_cnrm_cm6['datetime'] = pd.to_datetime(df_cnrm_cm6['time']) 


# Extraire le jour et le mois uniquement
df_canESM5['jour_annee'] = df_canESM5['datetime'].dt.strftime('%m-%d')
df_access_cm2['jour_annee'] = df_access_cm2['datetime'].dt.strftime('%m-%d')
df_cams_cm1['jour_annee'] = df_cams_cm1['datetime'].dt.strftime('%m-%d')
df_cnrm_cm6['jour_annee'] = df_cnrm_cm6['datetime'].dt.strftime('%m-%d')

# Moyenne journalière sur 15 ans
df_canESM5_ssp585_tMY = df_canESM5.groupby('jour_annee')['tasmax_ssp585'].mean().reset_index()
df_access_cm2_ssp585_tMY = df_access_cm2.groupby('jour_annee')['tasmax_ssp585'].mean().reset_index()
df_access_cm2_ssp245_tMY = df_access_cm2.groupby('jour_annee')['tasmax_ssp245'].mean().reset_index()
df_cams_cm1_ssp245_tMY = df_cams_cm1.groupby('jour_annee')['tasmax_ssp245'].mean().reset_index()
df_cams_cm1_ssp585_tMY = df_cams_cm1.groupby('jour_annee')['tasmax_ssp585'].mean().reset_index()
df_cnrm_cm6_ssp245_tMY = df_cnrm_cm6.groupby('jour_annee')['tasmax_ssp245'].mean().reset_index()


# Conversion des températures
for df in [df_canESM5_ssp585_tMY, df_access_cm2_ssp585_tMY, df_access_cm2_ssp245_tMY, df_cnrm_cm6_ssp245_tMY, df_cams_cm1_ssp245_tMY, df_cams_cm1_ssp585_tMY]:
    for col in df.columns[1:]:
        df[col] = df[col] / 10


# Pour que matplotlib interprète correctement les dates fictives
for df in [df_canESM5_ssp585_tMY, df_access_cm2_ssp585_tMY, df_access_cm2_ssp245_tMY, df_cnrm_cm6_ssp245_tMY, df_cams_cm1_ssp245_tMY, df_cams_cm1_ssp585_tMY]:
    df['jour_annee'] = pd.to_datetime('2000-' + df['jour_annee'], format='%Y-%m-%d')


# Tracé
plt.figure(figsize=(12, 6))
plt.plot(df_access_cm2_ssp585_tMY['jour_annee'], df_access_cm2_ssp585_tMY['tasmax_ssp585'], label='access_cm2_ssp585')
plt.plot(df_access_cm2_ssp245_tMY['jour_annee'], df_access_cm2_ssp245_tMY['tasmax_ssp245'], label='access_cm2_ssp245')
plt.plot(df_canESM5_ssp585_tMY['jour_annee'], df_canESM5_ssp585_tMY['tasmax_ssp585'], label='canESM5_ssp585')
plt.plot(df_cnrm_cm6_ssp245_tMY['jour_annee'], df_cnrm_cm6_ssp245_tMY['tasmax_ssp245'], label='cnrm_cm6_ssp245')
plt.plot(df_cams_cm1_ssp245_tMY['jour_annee'], df_cams_cm1_ssp245_tMY['tasmax_ssp245'], label='cams_cm1_ssp245')
plt.plot(df_cams_cm1_ssp585_tMY['jour_annee'], df_cams_cm1_ssp585_tMY['tasmax_ssp585'], label='cams_cm1_ssp585')

# Xticks : un tick le 1er de chaque mois
xticks = pd.date_range(start='2000-01-01', end='2000-12-31', freq='MS')
xtick_labels = xticks.strftime('%b')  # Jan, Feb, ...

plt.xticks(ticks=xticks, labels=xtick_labels, rotation=45)

# Légende et titres
plt.title("Comparaison de plusieurs modèles climatiques pour les TJmax de Dakar (scénarios CMIP6 2035 - 2050)")
plt.xlabel("Jour de l'année")
plt.ylabel("Températures max Journalières (°C)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

