import numpy as np
import matplotlib.pyplot as plt

# Raketparameters
initial_speed = 3000  # m/s
angle_deg = 45  # hoek in graden
g = 9.81  # zwaartekrachtsversnelling in m/s^2
time_step = 0.1  # tijdstap in seconden
target_distance = 755000  # afstand Kiev naar Moskou in meter

# Berekeningen voor initialisatie
angle_rad = np.radians(angle_deg)  # hoek in radialen
initial_horizontal_speed = initial_speed * np.cos(angle_rad)
initial_vertical_speed = initial_speed * np.sin(angle_rad)

# Lijsten voor opslag van traject
horizontal_position = [0]
vertical_position = [0]
horizontal_speed = initial_horizontal_speed
vertical_speed = initial_vertical_speed
time = [0]

# Simuleer omhooggaande beweging
while vertical_speed >= 0 or vertical_position[-1] > 0:
    # Bereken nieuwe posities en snelheden
    new_horizontal_position = horizontal_position[-1] + horizontal_speed * time_step
    new_vertical_position = vertical_position[-1] + vertical_speed * time_step
    new_vertical_speed = vertical_speed - g * time_step
    
    # Update lijsten
    horizontal_position.append(new_horizontal_position)
    vertical_position.append(new_vertical_position)
    vertical_speed = new_vertical_speed
    time.append(time[-1] + time_step)
    
    # Stop simulatie zodra we de grond raken
    if new_vertical_position <= 0:
        break

# Extra stap om te landen precies op target_distance
if horizontal_position[-1] < target_distance:
    horizontal_position[-1] = target_distance  # Forceer exact de eindpositie
    vertical_position[-1] = 0  # Land exact op grond

# Plot het traject
plt.figure(figsize=(10, 6))
plt.plot(horizontal_position, vertical_position, label="Traject van raket", color="blue")
plt.axhline(0, color="red", linestyle="--", label="Grondniveau")
plt.axvline(target_distance, color="green", linestyle="--", label="Doelafstand")
plt.title("Rakettraject")
plt.xlabel("Horizontale afstand (m)")
plt.ylabel("Hoogte (m)")
plt.legend()
plt.grid()
plt.show()
