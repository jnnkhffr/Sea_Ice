import pandas as pd
import matplotlib.pyplot as plt



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
#Exercise 3