import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Raketparameters
initial_mass = 500000  # Startmassa van de raket (kg)
fuel_burn_rate = 2000  # Brandstofverbruik (kg/s)
thrust = 20000000  # Stuwkracht van de motor (N)
initial_speed = 0  # Begin snelheid is nul (rust)
angle_deg = 45  # Lanceringhoek in graden
g = 9.81  # Zwaartekrachtsversnelling in m/s^2
time_step = 0.1  # Tijdstap in seconden
target_distance = 755000  # Doelafstand in meter (Kiev naar Moskou)

# Berekeningen voor initialisatie
angle_rad = np.radians(angle_deg)  # Hoek in radialen

# Variabelen voor beweging
horizontal_position = [0]
vertical_position = [0]
z_position = [0]  # Voor zijwaartse beweging
horizontal_speed = [0]  # Geen snelheid bij aanvang
vertical_speed = [0]
z_speed = [0]  # Zijwaartse snelheid
mass = initial_mass
time = [0]

# Willekeurige zijwaartse kracht (bijvoorbeeld door wind)
lateral_force = 500000  # Zijwaartse kracht (N)

# Simuleren van het traject (opstijgen met stuwkracht)
while mass > 100000:  # Stop als bijna alle brandstof op is (100.000 kg massa voor structuur)
    # Netto kracht: stuwkracht - zwaartekracht
    net_force = thrust - (mass * g)
    if net_force < 0:
        print("Raket heeft niet genoeg stuwkracht om op te stijgen!")
        break

    # Versnellingen
    acceleration = net_force / mass
    vertical_acceleration = acceleration * np.sin(angle_rad)
    horizontal_acceleration = acceleration * np.cos(angle_rad)
    z_acceleration = lateral_force / mass

    # Snelheid update
    new_vertical_speed = vertical_speed[-1] + vertical_acceleration * time_step
    new_horizontal_speed = horizontal_speed[-1] + horizontal_acceleration * time_step
    new_z_speed = z_speed[-1] + z_acceleration * time_step

    # Positie update
    new_vertical_position = vertical_position[-1] + new_vertical_speed * time_step
    new_horizontal_position = horizontal_position[-1] + new_horizontal_speed * time_step
    new_z_position = z_position[-1] + new_z_speed * time_step

    # Update massa door brandstofverbruik
    mass -= fuel_burn_rate * time_step

    # Stop simulatie als hoogte onder nul komt
    if new_vertical_position < 0:
        break

    # Opslaan in lijsten
    vertical_position.append(new_vertical_position)
    horizontal_position.append(new_horizontal_position)
    z_position.append(new_z_position)
    vertical_speed.append(new_vertical_speed)
    horizontal_speed.append(new_horizontal_speed)
    z_speed.append(new_z_speed)
    time.append(time[-1] + time_step)

# Raket daalt neer na bereiken van de maximale hoogte (vrij val)
while vertical_position[-1] > 0:
    # Geen stuwkracht meer -> alleen zwaartekracht
    new_vertical_speed = vertical_speed[-1] - g * time_step
    new_horizontal_speed = horizontal_speed[-1]  # Horizontale snelheid blijft constant
    new_z_speed = z_speed[-1]  # Zijwaartse snelheid blijft constant

    # Positie update
    new_vertical_position = vertical_position[-1] + new_vertical_speed * time_step
    new_horizontal_position = horizontal_position[-1] + new_horizontal_speed * time_step
    new_z_position = z_position[-1] + new_z_speed * time_step

    # Stop simulatie als hoogte onder nul komt
    if new_vertical_position < 0:
        break

    # Opslaan in lijsten
    vertical_position.append(new_vertical_position)
    horizontal_position.append(new_horizontal_position)
    z_position.append(new_z_position)
    vertical_speed.append(new_vertical_speed)
    horizontal_speed.append(new_horizontal_speed)
    z_speed.append(new_z_speed)
    time.append(time[-1] + time_step)

# Zorg ervoor dat de raket precies landt op target_distance
if horizontal_position[-1] < target_distance:
    horizontal_position[-1] = target_distance  # Exact doel
    vertical_position[-1] = 0  # Precies op de grond

# Plot het 3D-traject
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

ax.plot(horizontal_position, z_position, vertical_position, label="Traject van raket", color="blue")
ax.set_title("3D Rakettraject")
ax.set_xlabel("Horizontale afstand (m)")
ax.set_ylabel("Zijwaartse beweging (m)")
ax.set_zlabel("Hoogte (m)")
ax.legend()
plt.show()
