import numpy as np
import matplotlib.pyplot as plt


#Simulation parameters
g = 9.8                   #Gravity (m/s^2)
b = 0.1                   #Quadratic drag coefficient (kg/m)
k = 0.1                   #Linear drag coefficient (kg/s)
angle = 45                #Launch angle (degrees)
v0 = 20                   #Initial velocity (m/s)
flight_time = 10          #Maximum simulation time (s)
dt = 0.001                #Time step (s)
mass = 1                  #Projectile mass (kg)


#Initial velocity components
vx0 = v0 * np.cos(np.radians(angle))
vy0 = v0 * np.sin(np.radians(angle))


#Remove errors
if abs(vx0) < 1e-12:
    vx0 = 0.0

if abs(vy0) < 1e-12:
    vy0 = 0.0


#1-Projectile without air resistance
x = 0
y = 0
t = 0

x_values = [x]
y_values = [y]
time_values = [0]
kinetic_energy_values = [0.5 * mass * v0**2]

while t <= flight_time:

    #Analytical position
    x = vx0 * t
    y = -0.5 * g * t**2 + vy0 * t

    #Velocity
    vx = vx0
    vy = vy0 - g * t

    if y < 0: #Stop the simulation when the projectile reaches the ground.
        break

    #Kinetic energy
    kinetic_energy = 0.5 * mass * (vx**2 + vy**2)

    x_values.append(x)
    y_values.append(y)
    kinetic_energy_values.append(kinetic_energy)
    time_values.append(t)

    #Advance time
    t += dt


#2-Projectile with linear air resistance
x_linear = 0
y_linear = 0
t = 0

x_linear_values = [x_linear]
y_linear_values = [y_linear]
time_linear_values = [0]
kinetic_energy_linear_values = [0.5 * mass * v0**2]

while t <= flight_time:

    #Position
    x_linear = ((vx0 / k) * (1 - np.exp(-k * t)))

    y_linear = (((vy0 + g / k) / k) * (1 - np.exp(-k * t)) - (g / k) * t)

    #Velocity
    vx_linear = vx0 * np.exp(-k * t)
    vy_linear = ((vy0 + g / k) * np.exp(-k * t) - g / k)

    if y_linear < 0: #Stop the simulation when the projectile reaches the ground.
        break

    #Kinetic energy
    kinetic_energy = 0.5 * mass * (vx_linear**2 + vy_linear**2)

    x_linear_values.append(x_linear)
    y_linear_values.append(y_linear)
    kinetic_energy_linear_values.append(kinetic_energy)
    time_linear_values.append(t)

    #Advance time
    t += dt


#3-Projectile with quadratic air resistance
#For quadratic drag, I use the Euler method because the equations are coupled and I don't use an analytical solution here.
x_quadratic = 0
y_quadratic = 0
vx_quadratic = vx0
vy_quadratic = vy0
t = 0

x_quadratic_values = [x_quadratic]
y_quadratic_values = [y_quadratic]
time_quadratic_values = [0]
kinetic_energy_quadratic_values = [0.5 * mass * v0**2]

while t <= flight_time:

    #Speed
    v = np.sqrt(vx_quadratic**2 + vy_quadratic**2)

    #Acceleration
    ax = -b * v * vx_quadratic
    ay = -g - b * v * vy_quadratic

    #Position update (Euler method)
    x_quadratic += vx_quadratic * dt
    y_quadratic += vy_quadratic * dt

    #Velocity update (Euler method)
    vx_quadratic += ax * dt
    vy_quadratic += ay * dt

    #Advance time
    t += dt

    if y_quadratic < 0: #Stop the simulation when the projectile reaches the ground.
        break

    #Kinetic energy
    kinetic_energy = (0.5 * mass * (vx_quadratic**2 + vy_quadratic**2))

    x_quadratic_values.append(x_quadratic)
    y_quadratic_values.append(y_quadratic)
    kinetic_energy_quadratic_values.append(kinetic_energy)
    time_quadratic_values.append(t)


#---------------------------------------------------

#Plot
plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)

#Position
plt.plot(x_values, y_values, label="No Drag")
plt.plot(x_linear_values, y_linear_values, color="red", label="Linear Drag")
plt.plot(x_quadratic_values, y_quadratic_values, color="purple", label="Quadratic Drag")

plt.xlabel("Horizontal Position (m)")
plt.ylabel("Vertical Position (m)")
plt.title("Projectile Motion with Air Resistance")
plt.legend()
plt.grid()

#Kinetic Energy
plt.subplot(2, 1, 2)

plt.plot(time_values, kinetic_energy_values, label="No Drag")
plt.plot(time_linear_values, kinetic_energy_linear_values, color="red", label="Linear Drag")
plt.plot(time_quadratic_values, kinetic_energy_quadratic_values, color="purple", label="Quadratic Drag")

plt.xlabel("Time (s)")
plt.ylabel("Kinetic Energy (J)")
plt.title("Kinetic Energy vs Time")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
