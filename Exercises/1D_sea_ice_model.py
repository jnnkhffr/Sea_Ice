import matplotlib.pyplot as plt
import numpy as np


DAYS = 30 # duration of simulation
Tbot = -1.8 # Temperature at the bottom [C]
Tsurf = -10
L = 334000 # Latent heat of freezing for water [ J/kg ]
RHO = 970 # d e n si t y o f i c e [ kg /mˆ 3]
K_ice = 2.2 # he a t c o n d u c ti vi t y o f i c e [W/ (m K) ]
K_snow = 0.3 # he a t c o n d u c ti vi t y o f snow [W/ (m K) ]
SEC_PER_DAY = 86400 # How many s e c o n d s i n one day
H_ice_initial = 0.1 # in meters
Q_ocean = 5  # W/m Ocean heat flux pos= Wärme aus Ocean nach oben


h_ice = np.zeros(DAYS)
h_ice[0] = H_ice_initial



for day in range(1,DAYS):
    h_prev = h_ice[day -1]
    #Wärmestrom durchs Eis
    Q = K_ice * (Tbot - Tsurf) / h_prev   # W/m²
    # Dickenänderung pro Tag
    dh = (Q / (RHO * L)) * SEC_PER_DAY
    # Neue Dicke
    h_ice[day] = h_prev + dh

# --- Analytische Stefan-Lösung ---
t = np.arange(DAYS) * SEC_PER_DAY
h_stefan = np.sqrt(H_ice_initial ** 2 +
                   2 * K_ice * (Tbot - Tsurf) / (RHO * L) * t)

# --- Plot ---
plt.figure(figsize=(8, 5))
plt.plot(h_ice, label="Numerische Lösung", marker="o")
plt.plot(h_stefan, label="Stefan-Lösung (analytisch)", linestyle="--")
plt.xlabel("Tage")
plt.ylabel("Eisdicke (m)")
plt.title("Eisdickenentwicklung über 30 Tage")
plt.grid(True)
plt.legend()
plt.show()

# --- Ergebnisse ---
print("Enddicke numerisch:  ", h_ice[-1], "m")
print("Enddicke analytisch: ", h_stefan[-1], "m")


h_ice = np.zeros(DAYS)
h_ice[0] = H_ice_initial
#with Ocean
for day in range(1, DAYS):
    h_prev = h_ice[day - 1]

    # Wärmeleitung durch das Eis
    Q_cond = K_ice * (Tbot - Tsurf) / h_prev  # W/m²

    # Netto-Wärmefluss (Ozean liefert Wärme nach oben → reduziert Wachstum)
    Q_net = Q_cond - Q_ocean

    # Dickenänderung
    dh = (Q_net / (RHO * L)) * SEC_PER_DAY

    h_ice[day] = h_prev + dh

# --- Plot ---
plt.figure(figsize=(8, 5))
plt.plot(h_ice, marker="o", label="Numerische Lösung (mit 5 W/m² Ozeanwärme)")
plt.xlabel("Tage")
plt.ylabel("Eisdicke (m)")
plt.title("Eisdickenentwicklung mit ozeanischem Wärmestrom")
plt.grid(True)
plt.legend()
plt.show()

print("Enddicke nach 30 Tagen (mit 5 W/m²):", h_ice[-1], "m")