import numpy as np
#import OD_sea_ice_model
import matplotlib.pyplot as plt


# Nr. 2.1
def shortwave(doy):
    return 314.0 * np.exp(-(doy - 164)**2 / 4608.0)

def otherfluxes(doy):
    return 118.0 * np.exp(-0.5 * (doy - 206)**2 / (53**2)) + 179.0

def albedo():
    albice = 0.64  # bare ice albedo
    return albice


days = np.arange(1, 366)  # 1..365

sw = shortwave(days)
of = otherfluxes(days)

plt.figure(figsize=(10, 5))
plt.plot(days, sw, label="Shortwave radiation", color="orange")
plt.plot(days, of, label="Other fluxes (latent + sensible + longwave)", color="blue")

plt.xlabel("Day of Year")
plt.ylabel("Flux [W/m²]")
plt.title("Seasonal Cycle of Surface Energy Fluxes")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()