import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Constants
g = 9.81  # Acceleration due to gravity (m/s^2)
air_density = 1.225  # Air density (kg/m^3)
drag_coefficient = 0.47  # Drag coefficient for a sphere (dimensionless)
object_radius = 0.1  # Radius of the objects (meters)


# Function to calculate drag force
def calculate_drag_force(velocity):
    # Calculate the magnitude of velocity
    speed = np.linalg.norm(velocity)
    # Calculate the drag force
    drag_force_magnitude = (
        0.5 * air_density * speed**2 * drag_coefficient * np.pi * object_radius**2
    )
    # Calculate the drag force vector
    drag_force = -drag_force_magnitude * (velocity / speed)
    return drag_force


# Function to simulate physics for multiple objects
def simulate_physics(objects, total_time, time_step=0.01):
    # Create arrays to store time, position, and velocity values for each object
    time_values = np.arange(0, total_time, time_step)
    position_values = [[] for _ in objects]
    velocity_values = [[] for _ in objects]

    # Simulate the motion for each object
    for t in time_values:
        for i, obj in enumerate(objects):
            position_values[i].append(obj.position.copy())
            velocity_values[i].append(obj.velocity.copy())

            # Calculate gravitational force
            gravitational_force = np.array([0, 0, -obj.mass * g])

            # Calculate drag force
            drag_force = calculate_drag_force(obj.velocity)

            # Update position and velocity using the equations of motion
            net_force = gravitational_force + drag_force
            obj.position += obj.velocity * time_step
            obj.velocity += (net_force / obj.mass) * time_step

            # Check for ground collision (z < 0)
            if obj.position[2] < 0:
                obj.position[2] = 0
                obj.velocity[2] = 0  # Zero out vertical velocity

    return time_values, position_values, velocity_values


class PhysicsObject:
    def __init__(self, mass, initial_position, initial_velocity):
        self.mass = mass
        self.position = np.array(initial_position, dtype=float)
        self.velocity = np.array(initial_velocity, dtype=float)


# Example usage:
object1 = PhysicsObject(
    mass=1.0, initial_position=[0.0, 0.0, 100.0], initial_velocity=[10.0, 0.0, 20.0]
)
object2 = PhysicsObject(
    mass=0.5, initial_position=[0.0, 0.0, 100.0], initial_velocity=[15.0, 0.0, 25.0]
)

total_time = 10.0  # Total simulation time (seconds)

time, position, velocity = simulate_physics([object1, object2], total_time)

# Create a 3D plot of the trajectory
fig = plt.figure(figsize=(17, 8))
ax = fig.add_subplot(111, projection="3d")

for i, obj in enumerate([object1, object2]):
    positions = np.array(position[i])
    ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], label=f"Object {i + 1}")

ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
ax.set_title("3D Trajectory of Objects")
ax.legend()

plt.show()
