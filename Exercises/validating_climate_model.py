import xarray as xr
import matplotlib.pyplot as plt
#exercise 10.06.2026

files = {
    "MPI-LR": ("C:/Users/janni/Desktop/Studium/Master/Sea Ice/Exercises/MPI-ESM1-2-LR_nh_all_fv0.03.nc",
               "MPI_ESM1_2_LR_hist_r1i1p1f1"),
    "MPI-HR": ("C:/Users/janni/Desktop/Studium/Master/Sea Ice/Exercises/MPI-ESM1-2-HR_nh_all_fv0.03.nc",
               "MPI_ESM1_2_HR_hist_r1i1p1f1"),
    "ICON-LR": ("C:/Users/janni/Desktop/Studium/Master/Sea Ice/Exercises/ICON-ESM-LR_nh_all_fv0.03.nc",
                "ICON_ESM_LR_hist_r1i1p1f1")
}

# Ergebnisse speichern
seasonal_magnitudes = {}
sept_std_values = {}
seasonal_cycles = {}
september_series = {}
sia2000_series = {}
sia2000_2010_cycles = {}


for model, (file, varname) in files.items():
    ds = xr.open_dataset(file)
    sic = ds[varname]
    time = ds["time_historical"]

    # September-Werte
    sept = sic.where(time.dt.month == 9, drop=True)
    september_series[model] = sept

    # Daten ab 2000
    sia2000 = sic.where(time.dt.year >= 2000, drop=True)
    sia2000_series[model] = sia2000

    # Mittelwert 2000–2010 pro Monat
    cycle_2000_2010 = sic.where(
        (time.dt.year >= 2000) & (time.dt.year <= 2010),
        drop=True
    ).groupby("time_historical.month").mean()
    sia2000_2010_cycles[model] = cycle_2000_2010

    # Saisonaler Zyklus
    seasonal_cycle = sic.groupby("time_historical.month").mean()
    seasonal_cycles[model] = seasonal_cycle

    # Magnitude
    seasonal_magnitudes[model] = float((seasonal_cycle.max() - seasonal_cycle.min()).values)

    # Interannual variability
    sept_std_values[model] = float(sept.std(dim="time_historical").values)

# Ergebnisse ausgeben
print("\n=== Magnitude of the saisonale Cycle ===")
for model, mag in seasonal_magnitudes.items():
    print(f"{model}: {mag:.3f}")

print("\n=== Interannual Variability (September STD) ===")
for model, std in sept_std_values.items():
    print(f"{model}: {std:.3f}")

# Welches Modell ist „am besten“?
# Kriterien:
# - Kleine saisonale Magnitude → realistischer
# - Kleine year-to-year STD → stabiler
best_magnitude = min(seasonal_magnitudes, key=seasonal_magnitudes.get)
best_stability = min(sept_std_values, key=sept_std_values.get)

print("\n=== Bewertung ===")
print(f"Modell with the most realistic seasonal Magnitude: {best_magnitude}")
print(f"Modell with the lowest interannual variability: {best_stability}")


# September-Zeitreihe
plt.figure(figsize=(10,5))
for model, data in september_series.items():
    data.plot(label=model)
plt.title("September Sea Ice Area (all years)")
plt.xlabel("Jahr")
plt.ylabel("Sea Ice Area [10⁶ km²]")
plt.grid(True)
plt.legend()
plt.show()

# Sea Ice ab 2000
plt.figure(figsize=(10,5))
for model, data in sia2000_series.items():
    data.plot(label=model)
plt.title("Sea Ice Area ab 2000")
plt.xlabel("Jahr")
plt.ylabel("Sea Ice Area [10⁶ km²]")
plt.grid(True)
plt.legend()
plt.show()

# Saisonaler Zyklus 2000–2010
plt.figure(figsize=(10,5))
for model, data in sia2000_2010_cycles.items():
    data.plot(label=model)
plt.title("Saisonaler Zyklus 2000–2010 (Monatsmittel)")
plt.xlabel("Monat")
plt.ylabel("Sea Ice Area [10⁶ km²]")
plt.grid(True)
plt.legend()
plt.show()
