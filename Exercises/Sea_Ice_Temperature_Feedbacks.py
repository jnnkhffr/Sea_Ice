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


#2.2

H =0.5 #ice thickness
Tbot = -1.8 + 273.15 #bottom Temperature in Kelvin
K =2.2 #thermische conductivity of ice
SIGMA = 5.67e-8 #Stefan Boltzmann constante'
EPS = 0.95 #emissivity

#arrays fore result
days = np.arange(1,365)
Ttop = np.zeros_like(days, dtype=float)

#loop over all days
for i, day in enumerate(days):
    Fsw= shortwave(day)
    Fother = otherfluxes(day)
    alpha = albedo()

    # Equation:
    # -(1 - α) Fsw - Fother + ε σ T^4 = -k (T - Tbot)/h
    #
    # Rearranged into:
    # εσ T^4 + (k/h) T + [ (1-α)Fsw + Fother - (k/h)Tbot ] = 0

    a = EPS * SIGMA
    b = 0.0
    c = 0.0
    d = K / H
    e = (1 - alpha) * Fsw + Fother - (K / H) * Tbot

    roots = np.roots([a,b,c,d,e])
    print(roots)

    # Select real roots
    real_roots = roots[np.isreal(roots)].real

    # Physical root = larger real root
    Tphys = np.max(real_roots)

    # Cap at melting point
    if Tphys > 273.15:
        Tphys = 273.15

    Ttop[i] = Tphys