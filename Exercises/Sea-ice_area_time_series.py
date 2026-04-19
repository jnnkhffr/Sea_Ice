import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



sia_obs_Sep = pd.read_csv("C:/Users\janni\Desktop\Studium\Master\Sea Ice\Exercises\SeaIceArea__NorthernHemisphere__September__UHH__v2025_fv0.01.csv", index_col='year')


# Plot all time series
sia_obs_Sep.plot()
plt.title("Sea Ice in September from four different satellite algorithms.")
plt.show()

# Select and plot only data from OSISAF
sia_obs_Sep['osisaf'].plot()
plt.title("Sea Ice just for the OSISAF algorithm.")
plt.show()

# Mean September sea-ice area over the entire dataset
print(sia_obs_Sep.mean())

# Mean sea-ice area across the four algorithms
print(sia_obs_Sep.mean(axis=1))

# Maximum September sea-ice area
print(sia_obs_Sep.max())

# Minimum September sea-ice area
print(sia_obs_Sep.min())

# Standard deviation over the entire time series
print(sia_obs_Sep.std())

# Standard deviation between the algorithms for each year
print(sia_obs_Sep.std(axis=1))

# Plot that standard deviation
sia_obs_Sep.std(axis=1).plot()
plt.title("Standard deviation for September Sea Ice Area")
plt.show()

# Running mean over 10 years
sia_obs_Sep.rolling(10).mean().plot()
plt.title("Running mean over 10 years for September Sea Ice extend.")
plt.show()

# Mean sea-ice area for 1979–1998
print(sia_obs_Sep.loc[1979:1998].mean())

# Change in sea-ice area relative to 1979
(sia_obs_Sep - sia_obs_Sep.loc[1979]).plot()
plt.title("Change in sea-ice area relative to 1979 for September")
plt.show()




##########
# EXERCISE 2

sia_obs_all = pd.read_csv("C:/Users\janni\Desktop\Studium\Master\Sea Ice\Exercises\SeaIceArea__NorthernHemisphere__monthly__UHH__v2025_fv0.01_all_months.csv")

# Create a pandas datetime object from the year and month and store in the first column
sia_obs_all['date'] = pd.to_datetime(
    {
        "year": sia_obs_all[sia_obs_all.columns[0]].astype(int),
        "month": sia_obs_all[sia_obs_all.columns[1]].astype(int),
        "day": 15,
    }
)

# Drop the now-obsolete columns with year and month
sia_obs_all = sia_obs_all.drop(columns=[sia_obs_all.columns[0], sia_obs_all.columns[1]])

# Set the date column as the index
sia_obs_all = sia_obs_all.set_index('date')

#All data
fig, ax = plt.subplots(figsize=(12, 6))  # Größe des Plots anpassen
sia_obs_all.plot(ax =ax, linewidth=1)
ax.set_title("Sea Ice for the Entire Timeseries from Four Satellite Algorithms")
ax.set_xlabel("Date")
ax.set_ylabel("Sea Ice Area in Million Square Kilometers")
plt.grid(True, linestyle="--", alpha=0.5)  # dezentes Grid
plt.tight_layout()
plt.show()

#All data for September
fig, ax = plt.subplots(figsize=(12, 6))
sia_obs_all[sia_obs_all.index.month == 9].plot(ax=ax, linewidth=1)
ax.set_title("Sea Ice from all data for September from Four Satellite Algorithms")
ax.set_xlabel("Date")
ax.set_ylabel("Sea Ice Area in Million Square Kilometers")
plt.grid(True, linestyle="--", alpha=0.5)  # dezentes Grid
plt.tight_layout()
plt.show()

#Seasonal cycle for one year
fig, ax = plt.subplots(figsize=(12, 6))
sia_obs_all.loc[sia_obs_all.index.year == 2012].plot(ax=ax, marker="o")
ax.set_title("Sea Ice from all data for 2012 from Four Satellite Algorithms")
ax.set_xlabel("Date")
ax.set_ylabel("Sea Ice Area in Million Square Kilometers")
plt.grid(True, linestyle="--", alpha=0.5)  # dezentes Grid
plt.tight_layout()
plt.show()



##########
#EXERCISE 3
#3.2


emissions = pd.read_excel(
    "C:/Users\janni\Desktop\Studium\Master\Sea Ice\Exercises\Global_Carbon_Budget_2025_v0.6.xlsx",
    sheet_name="Fossil Emissions by Category",
    header=8,
    index_col=0
)

# Kumulative CO2-Emissionen (in GtCO2) berechnen
cum_emissions = emissions["fossil.emissions.excluding.carbonation"].cumsum() * 3.67

# -> Warum der Faktor 3.67?
# Die Emissionen sind meist in GtC (Gigatonnen Kohlenstoff) angegeben.

# Massenverhältnis = M CO2 / M C = 44/12 ≈ 3,67

# Also: aus Kohlenstoffmasse → CO₂-Masse. (siehe Tabellen header)


#Die September-Meereseis-Daten gehen z.B. von 1979–2024. Also schneiden wir die kumulativen Emissionen auf denselben
# Zeitraum zu:
cum_emissions = cum_emissions.loc[1979:2024]

#September Meereisfläche:
# Mittel über alle Algorithmen pro Jahr (September)
sia_sep_mean = sia_obs_Sep.mean(axis=1)
sia_sep_mean = sia_sep_mean.loc[1979:2024]

x = cum_emissions.loc[sia_sep_mean.index]
y = sia_sep_mean

slope, intercept = np.polyfit(x, y, 1)

print("Steigung (slope):", slope, "Million km² pro GtCO₂")
print("Achsenabschnitt (intercept):", intercept, "Million km²")
loss_per_ton = slope / 1e9
print("Verlust an September-Meereis pro Tonne CO₂:", loss_per_ton, "Million km² pro Tonne CO₂")
# Verlust pro Tonne CO2 in km²
loss_per_ton_km2 = loss_per_ton * 1e6
print("Verlust pro Tonne CO2:", loss_per_ton_km2, "km² pro Tonne CO2 -> -27 cm^2 pro Tonne CO2")


target_sia = 1.0  # Million km²
cum_emissions_threshold = (target_sia - intercept) / slope
print("Kumulative Emissionen für 1 Mio km²:", cum_emissions_threshold, "GtCO₂")


# Jahr finden, in dem die kumulativen Emissionen den Schwellenwert überschreiten
# grobe Extrapolation
current_cum = cum_emissions.iloc[-1]
remaining = cum_emissions_threshold - current_cum
# z.B. mittlere jährliche Emissionen der letzten 5 Jahre
recent_mean_annual = emissions["fossil.emissions.excluding.carbonation"].iloc[-5:].mean() * 3.67
years_to_threshold = remaining / recent_mean_annual
year_estimate = cum_emissions.index[-1] + years_to_threshold
print("Geschätztes Jahr für praktisch eisfrei (linear, mit aktuellen Emissionen):", year_estimate)





#Exercise 3.3

#Text Datei als csv
df = pd.read_csv(
    r"C:\Users\janni\Desktop\Studium\Master\Sea Ice\Exercises\annual_global_temperature_anomalies.txt",
    delim_whitespace=True,
    header=None
)

df.to_csv(
    r"C:\Users\janni\Desktop\Studium\Master\Sea Ice\Exercises\annual_global_temperature_anomalies.csv",
    index=False
)


rows = []

with open("C:/Users\janni\Desktop\Studium\Master\Sea Ice\Exercises/annual_global_temperature_anomalies.csv", "r") as f:
    for line in f:
        line = line.strip()

        # Kommentarzeilen überspringen
        if line.startswith("%") or line == "":
            continue

        # Zeile in Werte splitten (Komma-getrennt)
        parts = line.split(",")

        # Nur Zeilen behalten, die mit einer Jahreszahl beginnen
        if parts[0].isdigit():
            rows.append(parts)

df = pd.DataFrame(rows)

df = df[[0, 1]]
df.columns = ["Year", "Annual Anomaly"]

# In Zahlen umwandeln
df["Year"] = df["Year"].astype(int)
df["Annual Anomaly"] = pd.to_numeric(df["Annual Anomaly"], errors="coerce")

# Index setzen
df = df.set_index("Year")

print(df.head())


# Temperaturdaten liegen jetzt in df
# -> Zeile mit Year = 0 entfernen
df = df[df.index != 0]

# Zeitraum 1979–2024 auswählen
temp = df.loc[1979:2024]

# September-Meereseis-Mittelwerte
sia_sep_mean = sia_obs_Sep.mean(axis=1)
sia_sep_mean = sia_sep_mean.loc[1979:2024]

# Regression vorbereiten
x = temp["Annual Anomaly"]          # Temperatur (°C)
y = sia_sep_mean                    # Sea Ice (Million km²)

# Lineare Regression
slope_T, intercept_T = np.polyfit(x, y, 1)

print("Steigung:", slope_T, "Million km² pro °C")
print("Achsenabschnitt:", intercept_T)

# Verlust pro °C in km²
loss_per_deg_km2 = slope_T * 1e6
print("Verlust pro °C:", loss_per_deg_km2, "km² pro °C")

# Schwelle für praktisch eisfrei (1 Mio km²)
target_sia = 1.0  # 1 Million km²
warming_threshold = (target_sia - intercept_T) / slope_T
print(f"Warming-Level für 1 Mio km²: {warming_threshold:.2f}, °C über 1951–1980")

# Umrechnung auf 1850–1900 (IPCC: +0.85°C)
warming_threshold_preindustrial = warming_threshold + 0.85
print(f"Warming-Level relativ zu 1850–1900: {warming_threshold_preindustrial:.2f} °C")

# Heutiges Warming-Level (2024)
current_temp_1951_1980 = temp.loc[2024, "Annual Anomaly"]
current_temp_preindustrial = current_temp_1951_1980 + 0.85
print(f"Heutiges Warming-Level (2024): {current_temp_preindustrial:.2f}, °C über 1850–1900")


