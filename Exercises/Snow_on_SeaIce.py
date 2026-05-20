import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np

arctic_data = pd.read_csv("C:/Users/janni/Desktop/Studium/Master/Sea Ice/Exercises/Exercise_205/2019S94_300234066081170_proc.csv")
antarctic_data = pd.read_csv("C:/Users/janni/Desktop/Studium/Master/Sea Ice/Exercises/Exercise_205/2021S114_300534061254970_proc.csv")

for df in [arctic_data, antarctic_data]:
    df["time"] = pd.to_datetime(df["time"])


snow_cols = [
    "distance_to_initial_snow_ice_interface_1 (m)",
    "distance_to_initial_snow_ice_interface_2 (m)",
    "distance_to_initial_snow_ice_interface_3 (m)",
    "distance_to_initial_snow_ice_interface_4 (m)"
]

def plot_region(df, region_name):
    fig, ax = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # Schneetiefen – alle vier Linien
    for col in snow_cols:
        ax[0].plot(df["time"], df[col], label=col)
    df["snow_mean"] = df[snow_cols].mean(axis=1)
    #ax[0].plot(df["time"], df["snow_mean"], color="black", linewidth=1, label="Mean snow depth")
    df_weekly = df.set_index("time").resample("W").mean()
    ax[0].plot(df_weekly.index, df_weekly["snow_mean"],
               color="black", linewidth=1,
               label="Daily mean snow depth")

    ax[0].set_ylabel("Snow depth (m)")
    ax[0].set_title(f"{region_name}: Snow–Ice Interfaces")
    ax[0].legend()

    ax[1].plot(df["time"], df["temperature_air (degC)"], color="red")
    ax[1].set_ylabel("Air temperature (°C)")
    ax[1].set_title(f"{region_name}: Air Temperature")

    ax[2].plot(df["time"], df["barometric_pressure (hPa)"], color="green")
    ax[2].set_ylabel("Pressure (hPa)")
    ax[2].set_title(f"{region_name}: Air Pressure")

    plt.xlabel("Time")
    plt.tight_layout()
    plt.show()

plot_region(arctic_data, "Arctic")
plot_region(antarctic_data, "Antarctic")
