import xarray as xr
import matplotlib.pyplot as plt
from cdo import Cdo

cdo = Cdo()

# Input NetCDF file
input_file = "siconc_Global_ensemble_historical_r1i1p1f1_mean.nc"

# Define the output file for the northern hemisphere sea-ice area time series
output_file = "sea_ice_area_september_nh.nc"

# Use CDO to extract the northern hemisphere sea-ice area for September
cdo.gridarea(input=input_file, output="gridarea.nc")
cdo.mul(input="gridarea.nc siconc_Global_ensemble_historical_r1i1p1f1_mean.nc", output="sea_ice_area_per_cell.nc")
cdo.selmon(9, input="sea_ice_area_per_cell.nc", output="sea_ice_area_per_cell_september.nc")
cdo.sellonlatbox("-180,180,0,90", input="sea_ice_area_per_cell_september.nc", output="sea_ice_area_per_cell_nh.nc")
cdo.fldsum(input="sea_ice_area_per_cell_nh.nc", output=output_file)

ds = xr.open_dataset(output_file)

# Extract the time series data
time = range(1850,2015)
sea_ice_area = ds['cell_area'].values.flatten()

# Plot the time series
plt.figure(figsize=(10, 6))
plt.plot(time, sea_ice_area/1e14, label="Sea Ice Area (September, NH)")
plt.xlabel("Time")
plt.ylabel("Sea Ice Area (million km²)")
plt.title("Northern Hemisphere Sea Ice Area (September)")
plt.legend()
plt.grid()
plt.show()