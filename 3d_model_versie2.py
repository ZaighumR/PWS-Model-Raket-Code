import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Aarde parameters
earth_radius = 6371000  # Radius van de aarde in meters
kiev_coords = (50.4501, 30.5234)  # Kiev: (latitude, longitude)
moscow_coords = (55.7558, 37.6173)  # Moskou: (latitude, longitude)

# Functie om breedte-/lengtegraad om te zetten in 3D Cartesische coördinaten
def lat_lon_to_cartesian(latitude, longitude, radius):
    lat_rad = np.radians(latitude)
    lon_rad = np.radians(longitude)
    x = radius * np.cos(lat_rad) * np.cos(lon_rad)
    y = radius * np.cos(lat_rad) * np.sin(lon_rad)
    z = radius * np.sin(lat_rad)
    return np.array([x, y, z])

kiev_position = lat_lon_to_cartesian(*kiev_coords, earth_radius)
moscow_position = lat_lon_to_cartesian(*moscow_coords, earth_radius)
target_distance = np.linalg.norm(moscow_position - kiev_position)  # Hemelsbreed afstand

# Raketparameters
initial_mass = 500000  # Startmassa van de raket (kg)
fuel_burn_rate = 2000  # Brandstofverbruik (kg/s)
thrust = 20000000  # Stuwkracht van de motor (N)
g = 9.81  # Zwaartekrachtsversnelling (m/s²)
time_step = 0.1  # Tijdstap (s)
angle_deg = 45  # Lanceringhoek in graden

# Berekeningen voor initialisatie
angle_rad = np.radians(angle_deg)

# Variabelen voor beweging
trajectory_positions = [kiev_position]
velocities = [np.array([0.0, 0.0, 0.0])]  # Start snelheid
mass = initial_mass
time = [0]

# Willekeurige zijwaartse kracht (bijvoorbeeld door wind)
lateral_force = 500000  # Zijwaartse kracht (N)

# Simuleren van het opstijgen (met stuwkracht)
while mass > 100000:  # Simuleer terwijl er brandstof is
    # Bepaal netto kracht en versnellingen
    net_force = thrust - (mass * g)  # Netto kracht (exclusief luchtweerstand)
    if net_force < 0:
        print("De raket heeft niet genoeg stuwkracht om verder te gaan!")
        break

    # Richtingsversnellingen
    acceleration_magnitude = net_force / mass
    acceleration_vector = np.array([
        acceleration_magnitude * np.cos(angle_rad),  # Vooruit
        acceleration_magnitude * np.sin(angle_rad),  # Verticaal
        lateral_force / mass  # Zijwaarts
    ])
    
    # Snelheid update
    new_velocity = velocities[-1] + acceleration_vector * time_step

    # Positie update
    new_position = trajectory_positions[-1] + new_velocity * time_step

    # Update massa
    mass -= fuel_burn_rate * time_step

    # Check of de raket nog boven aarde is
    altitude = np.linalg.norm(new_position) - earth_radius
    if altitude < 0:
        break

    # Opslaan in traject
    trajectory_positions.append(new_position)
    velocities.append(new_velocity)
    time.append(time[-1] + time_step)

# Vrije val: simuleren zodra de brandstof op is
while True:
    # Alleen zwaartekracht werkt
    gravity_vector = -g * trajectory_positions[-1] / np.linalg.norm(trajectory_positions[-1])

    # Snelheid en positie updates
    new_velocity = velocities[-1] + gravity_vector * time_step
    new_position = trajectory_positions[-1] + new_velocity * time_step

    # Controleer als de raket de aarde raakt
    if np.linalg.norm(new_position) <= earth_radius:
        break

    # Opslaan in traject
    trajectory_positions.append(new_position)
    velocities.append(new_velocity)
    time.append(time[-1] + time_step)

# 3D traject plotten
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Teken de aarde
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = earth_radius * np.outer(np.cos(u), np.sin(v))
y = earth_radius * np.outer(np.sin(u), np.sin(v))
z = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, color='blue', alpha=0.3)

# Teken het rakettraject
trajectory_positions = np.array(trajectory_positions)
ax.plot(trajectory_positions[:, 0], trajectory_positions[:, 1], trajectory_positions[:, 2], color="red", label="Rakettraject")

# Teken Kiev en Moskou
ax.scatter(*kiev_position, color="green", label="Kiev", s=100)
ax.scatter(*moscow_position, color="orange", label="Moskou", s=100)

# Labels en titel
ax.set_title("3D Raketbaan over de Aarde")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
ax.legend()
plt.show()
