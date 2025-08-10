import pandas as pd
import matplotlib.pyplot as plt
import os

# Fichiers EPW
files = {
    "Référence (présente)": "kolda.epw",
    "Projection 2050": "kolda2050.epw",
    "Projection 2080": "kolda2080.epw"
}

def load_epw_temp(path):
    df = pd.read_csv(path, header=None, skiprows=8)
    df = df[[0,1,2,3,4,6]].copy()
    df.columns = ["year","month","day","hour","minute","drybulb"]
    df["hour"] = df["hour"] - 1  # EPW hours: 1..24 -> 0..23
    df["dt"] = pd.to_datetime(df[["year","month","day","hour","minute"]], errors="coerce")
    df = df.dropna(subset=["dt"])
    df["drybulb"] = pd.to_numeric(df["drybulb"], errors="coerce")
    return df

def semaine_type_ete(df, summer_months=(6,7,8)):
    df_summer = df[df["month"].isin(summer_months)].copy()
    df_summer["weekday"] = df_summer["dt"].dt.weekday
    df_summer["hour_of_day"] = df_summer["dt"].dt.hour
    grp = df_summer.groupby(["weekday","hour_of_day"])["drybulb"].mean().unstack(level=1)
    grp = grp.reindex(columns=range(24))
    grp = grp.interpolate(axis=1, limit_direction="both")
    week_series = pd.concat([grp.loc[wd] for wd in range(7)], ignore_index=True)
    week_series.index = pd.Index(range(168), name="hour_of_week")
    return week_series

# Traitement
results = {}
for label, path in files.items():
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    df = load_epw_temp(path)
    week_series = semaine_type_ete(df)
    results[label] = week_series

# Tracé
plt.rcParams.update({'font.size': 10})
fig, ax = plt.subplots(figsize=(10,4.5))

label_map = {
    "Référence (présente)": "actual",
    "Projection 2050": "projection 2050",
    "Projection 2080": "projection 2080"
}

for label, series in results.items():
    lbl = label_map.get(label, label)
    ax.plot(series.index, series.values, linewidth=1.4, label=lbl)

ax.set_xlabel("Hour of the week (0 = Monday 00:00)", fontsize=11)
ax.set_ylabel("Dry-bulb Temperature (°C)", fontsize=11)
ax.set_title("Typical Summer Week — Hourly Temperature Evolution\n(average of June–July–August)", fontsize=12)
ax.set_xlim(0, 167)
ax.set_xticks([0, 24, 48, 72, 96, 120, 144, 167])
ax.set_xticklabels(
    ["Mon 00:00","Tue 00:00","Wed 00:00","Thu 00:00","Fri 00:00","Sat 00:00","Sun 00:00","Sun 23:00"],
    rotation=0
)
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Légende sur une seule ligne
ax.legend(frameon=False, fontsize=9, ncol=3, loc='upper center', bbox_to_anchor=(0.5, -0.15))
fig.tight_layout()

plt.savefig("typical_summer_week_dakar_one_line_legend.png", dpi=300, bbox_inches="tight")
plt.show()
