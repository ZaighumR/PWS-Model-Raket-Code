import numpy as np
import matplotlib.pyplot as plt

# Algemeen
g = 9.81  # Gravitatieversnelling (m/s^2)
rho = 1.225  # Luchtdichtheid op zeeniveau (kg/m^3)
Cd = 0.5  # Weerstandscoëfficiënt
A = 1.0  # Frontale oppervlakte van de raket (m^2)

# Raketparameters
thrust = 2250000  # Stuwkracht (N)
m0 = 110000  # Beginmassa inclusief brandstof (kg)
m_dot = 500  # Brandstofverbruik (kg/s)
dry_mass = 23000  # Droge massa zonder brandstof (kg)

# Simulatieparameters
dt = 0.1  # Tijdsinterval (s)
t_max = 600  # Maximum simulatieseconde (s) zodat we de daling ook kunnen zien
target_distance = 755000  # Doelafstand Kiev-Moskou (m)
theta_deg = 45  # Lanceerhoek in graden
theta = np.radians(theta_deg)  # Omzetten naar radialen

def current_mass(t):
    """Huidige massa van de raket op tijdstip t."""
    fuel_mass = max(0, m0 - dry_mass - m_dot * t)
    return dry_mass + fuel_mass

def drag_force(v):
    """Berekent de luchtweerstand."""
    return 0.5 * rho * Cd * A * v**2

def net_force(mass, velocity, angle):
    """Berekent de netto kracht op de raket."""
    F_drag = drag_force(velocity)
    F_gravity = mass * g
    F_thrust = thrust if mass > dry_mass else 0  # Geen stuwkracht na brandstofverbruik
    F_net = F_thrust - F_gravity - F_drag
    return F_net

# Tijdstappen
time = np.arange(0, t_max, dt)

# Arrays initialiseren
altitude = np.zeros(len(time))  # Hoogte y (m)
horizontal_position = np.zeros(len(time))  # Horizontale afstand x (m)
velocity_x = np.zeros(len(time))  # Snelheid in x-richting (m/s)
velocity_y = np.zeros(len(time))  # Snelheid in y-richting (m/s)
mass = np.zeros(len(time))  # Massa (kg)

# Startvoorwaarden
altitude[0] = 0
horizontal_position[0] = 0
velocity_x[0] = 0
velocity_y[0] = 0
mass[0] = m0

# Simulatie
for i in range(1, len(time)):
    # Massa berekenen op dit tijdstip
    mass[i] = current_mass(time[i])
    
    # Netto kracht en versnelling in de y-richting
    F_net_y = net_force(mass[i-1], velocity_y[i-1], theta)
    acceleration_y = F_net_y / mass[i-1]
    
    # Netto kracht en versnelling in de x-richting
    F_net_x = thrust * np.cos(theta) - drag_force(velocity_x[i-1])  # Voeg drag_force voor horizontaal toe
    acceleration_x = F_net_x / mass[i-1]
    
    # Update snelheden
    velocity_y[i] = velocity_y[i-1] + acceleration_y * dt
    velocity_x[i] = velocity_x[i-1] + acceleration_x * dt
    
    # Update posities
    altitude[i] = altitude[i-1] + velocity_y[i] * dt
    horizontal_position[i] = horizontal_position[i-1] + velocity_x[i] * dt
    
    # Stop simulatie als raket weer de grond raakt
    if altitude[i] < 0:
        break

# Controleer of het doel bereikt is
final_position = horizontal_position[np.argmax(altitude < 0)]  # Laatste horizontale positie voor landing
if final_position >= target_distance:
    print(f"Doel bereikt! Raket landt op een afstand van {final_position:.2f} meter.")
else:
    print(f"Doel niet bereikt. Raket landt op {final_position:.2f} meter.")

# Plot het traject
plt.figure(figsize=(10, 6))
plt.plot(horizontal_position, altitude, label='Traject van raket', color='blue')
plt.axhline(0, color='red', linestyle='--', label='Grondniveau')
plt.axvline(target_distance, color='green', linestyle='--', label='Doelafstand')
plt.title('Rakettraject')
plt.xlabel('Horizontale afstand (m)')
plt.ylabel('Hoogte (m)')
plt.legend()
plt.grid()
plt.show()
