import numpy as np
import matplotlib.pyplot as plt

# Constanten
G = 6.67430e-11  # Gravitatieconstante (m^3/kg/s^2)
M_earth = 5.972e24  # Massa van de aarde (kg)
R_earth = 6371000  # Straal van de aarde (m)
rho = 1.225  # Luchtdichtheid op zeeniveau (kg/m^3)
Cd = 0.5  # Weerstandscoëfficiënt
A = 1.0  # Frontale oppervlakte van de raket (m^2)

# Raketparameters
thrust = 750000 # Stuwkracht (N)
m0 = 23000 # Beginmassa inclusief brandstof (kg)
m_dot = 500  # Brandstofverbruik (kg/s)
dry_mass = 2400  # Droge massa zonder brandstof (kg)

# Simulatieparameters
dt = 0.05  # Tijdsinterval (s)
t_max = 600  # Maximum simulatieseconde (s)
target_distance = 755000  # Doelafstand (m)
theta_deg = 45  # Lanceerhoek in graden
theta = np.radians(theta_deg)  # Omzetten naar radialen

def current_mass(t):
    """Huidige massa van de raket op tijdstip t."""
    fuel_mass = max(0, m0 - dry_mass - m_dot * t)
    return dry_mass + fuel_mass

def gravity_force(mass, altitude):
    """Berekent de zwaartekracht op een bepaalde hoogte."""
    return (G * M_earth * mass) / (R_earth + altitude) ** 2

def air_density(altitude):
    """Schat de luchtdichtheid afnemend met hoogte (exponentieel model)."""
    return rho * np.exp(-altitude / 8000)  # 8000 m is typische schaalhoogte

def drag_force(v, altitude):
    """Berekent de luchtweerstand op basis van snelheid en hoogte."""
    return 0.5 * air_density(altitude) * Cd * A * v**2

# Tijdstappen
time = np.arange(0, t_max, dt)

# Arrays initialiseren
altitude = np.zeros(len(time))  
horizontal_position = np.zeros(len(time))  
velocity_x = np.zeros(len(time))  
velocity_y = np.zeros(len(time))  
mass = np.zeros(len(time))  

# Startvoorwaarden
altitude[0] = 0
horizontal_position[0] = 0
velocity_x[0] = 0
velocity_y[0] = 0
mass[0] = m0

# Simulatie
for i in range(1, len(time)):
    # Massa berekenen
    mass[i] = current_mass(time[i])
    
    # Krachten in de y-richting
    F_gravity = gravity_force(mass[i-1], altitude[i-1])
    F_drag_y = drag_force(velocity_y[i-1], altitude[i-1])
    F_thrust = thrust if mass[i] > dry_mass else 0  # Geen stuwkracht na brandstofverbruik
    F_net_y = F_thrust * np.sin(theta) - F_gravity - F_drag_y

    # Krachten in de x-richting
    F_drag_x = drag_force(velocity_x[i-1], altitude[i-1])
    F_net_x = (F_thrust * np.cos(theta)) - F_drag_x

    # Versnellingen
    acceleration_y = F_net_y / mass[i-1]
    acceleration_x = F_net_x / mass[i-1]

    # Update snelheden
    velocity_y[i] = velocity_y[i-1] + acceleration_y * dt
    velocity_x[i] = velocity_x[i-1] + acceleration_x * dt

    # Update posities
    altitude[i] = altitude[i-1] + velocity_y[i] * dt
    horizontal_position[i] = horizontal_position[i-1] + velocity_x[i] * dt
    
    # Controle of de raket de grond raakt
    if altitude[i] <= 0:
        altitude[i] = 0  # Zorg ervoor dat de raket niet onder de grond gaat
        velocity_y[i] = 0  # De snelheid wordt nul bij impact
        break  # Stop simulatie zodra de raket de grond raakt

# Bepaal de uiteindelijke landingspositie
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
plt.title('Rakettraject met zwaartekracht en luchtweerstand')
plt.xlabel('Horizontale afstand (m)')
plt.ylabel('Hoogte (m)')
plt.legend()
plt.grid()
plt.show()
