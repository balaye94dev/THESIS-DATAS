import xarray as xr
import pandas as pd

# Chemin vers ton fichier NetCDF 
fichier_nc = "Future/tasmax_day_CNRM-CM6-1_ssp245_r1i1p1f2_gr_20240101-20241231.nc"

# Charger le fichier NetCDF
ds = xr.open_dataset(fichier_nc)

# Coordonnées de Dakar
lat_dakar = 14.73
lon_dakar = -17.52

# Convertir longitude en 0–360 si nécessaire
if ds.coords['lon'].max() > 180:
  lon_dakar = lon_dakar % 360

# Trouver le point le plus proche de Dakar
point_dakar = ds.sel(lat=lat_dakar, lon=lon_dakar, method='nearest')

# Lister les variables disponibles
print("Variables disponibles :", list(ds.data_vars))

# Choisir une variable à extraire 
tas = list(ds.data_vars)[1] 
donnees = point_dakar[tas]

# Convertir en DataFrame
df = donnees.to_dataframe().reset_index()

# Sauvegarder en Excel
df.to_excel("cmip6_2024_dakar_cnrm_cm6_ssp245.xlsx", index=False)