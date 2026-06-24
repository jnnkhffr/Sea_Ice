import xarray as xr

LAT_MIN = 66
LAT_MAX = 90
LON_MIN = -180
LON_MAX = 180

file = "C:/Users/janni/Desktop/Studium/Master/Sea Ice/Exercises/sithick_SImon_MPI-ESM1-2-HR_ssp370_r1i1p1f1_gn_201501-210012.nc"

df = xr.open_dataset(file)
print(list(df.data_vars)) #['time_bnds', 'sithick']