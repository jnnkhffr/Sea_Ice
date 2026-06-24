import xarray as xr
import matplotlib.pyplot as plt

LAT_MIN = 66
LAT_MAX = 90
LON_MIN = -180
LON_MAX = 180

file = "C:/Users/janni/Desktop/Studium/Master/Sea Ice/Exercises/sithick_SImon_MPI-ESM1-2-HR_ssp370_r1i1p1f1_gn_201501-210012.nc"

df = xr.open_dataset(file)
print(list(df.data_vars)) #['time_bnds', 'sithick']

df_arctic = df.sel(lat=slice(LAT_MIN, LAT_MAX))
sithick_arctic_mean = df_arctic["sithick"].mean(dim=["lat", "lon"])

plt.figure(figsize=(10,5))
plt.plot(df["time"], sithick_arctic_mean, label= "Sea ice thickness")

plt.title("Arctic Sea Ice thickness")
plt.xlabel("Years")
plt.ylabel("Sea Ice Thickness (m)")
plt.grid(True)
plt.legend()
plt.show()