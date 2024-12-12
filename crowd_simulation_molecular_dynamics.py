import numpy as np
import random
import matplotlib.pyplot as plt
from math import sqrt, exp
from scipy import stats

# Parameters
radius_agent = 0.5  # Radius of an agent
mass_agent = 75  # Mass of an agent in kg
relaxation_time = 0.5  # Relaxation time for agents
time_step = 5**(-4)  # Time step
A_c = 2000  # Constant for contact force (N)
B_c = 0.08  # Constant for contact force (m)
v_max = sqrt(2) * (10**3)  # Max velocity (m/time_step)
room_size = 50  # Size of the room (meters)
exit_center = np.array([0, room_size / 2])  # Coordinates of the exit center
exit_width = 2  # Width of the exit (meters)
wall_divisions = 200  # Number of wall divisions
friction_coefficient_agents = 0.15  # Friction coefficient between agents
friction_coefficient_walls = 0.35  # Friction coefficient with walls
wall_contact_tangent = 2.4 * (10**6)  # Wall contact tangent constant
agent_contact_normal = 1.2 * (10**6)  # Agent contact normal constant

state_dict = {}  # Dictionary to track the states (1 = exited, 0 = not exited)
contact_list = []  # List to store contact events

# Define the walls of the room, excluding the exit area
wall_positions = [
    np.array([0., 0.]), np.array([0., float(room_size)]),
    np.array([float(room_size), 0.]), np.array([float(room_size), float(room_size)])
]

step_size = room_size / wall_divisions
for k in range(1, wall_divisions):
    if (k * step_size) >= (room_size - exit_width) / 2 and (k * step_size) <= (room_size + exit_width) / 2:
        # Skip walls on the exit area
        wall_positions.append(np.array([k * step_size, 0.]))
        wall_positions.append(np.array([room_size, k * step_size]))
        wall_positions.append(np.array([k * step_size, room_size]))
    else:
        wall_positions.append(np.array([k * step_size, 0.]))
        wall_positions.append(np.array([0., k * step_size]))
        wall_positions.append(np.array([room_size, k * step_size]))
        wall_positions.append(np.array([k * step_size, room_size]))


# Function to calculate Euclidean distance between two points
def euclidean_distance(a, b):
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


# Function to calculate distance between two agents
def agent_distance(i, j, positions):
    """
    Input: two agents (index i and j)
    Output: Euclidean distance between the two agents' centers
    """
    return sqrt((positions[i][0] - positions[j][0])**2 + (positions[i][1] - positions[j][1])**2)


# Function to calculate the direction vector for an agent towards the exit
def exit_direction(agent_index, positions):
    """
    Calculate the direction vector pointing from agent to the exit
    """
    exit_position = np.array([room_size / 2, room_size / 2])  # Define exit position
    direction = (1 / euclidean_distance(positions[agent_index], exit_position)) * np.array([exit_position[0] - positions[agent_index][0], exit_position[1] - positions[agent_index][1]])
    return direction


# Function to calculate the direction vector between two agents
def interaction_direction(i, j, positions):
    """
    Direction vector between two agents at a given time, computed based on their positions
    """
    distance = agent_distance(i, j, positions)
    if distance > 1e-20:
        return (1 / distance) * np.array([positions[i][0] - positions[j][0], positions[i][1] - positions[j][1]])
    else:
        return 1e20 * np.array([positions[i][0] - positions[j][0], positions[i][1] - positions[j][1]])


# Function to calculate the direction vector from a wall to an agent
def wall_interaction_direction(agent_index, wall_position, positions):
    """
    Direction vector from a wall to an agent at a given time
    """
    if euclidean_distance(positions[agent_index], wall_position) > 1e-20:
        return (1 / euclidean_distance(positions[agent_index], wall_position)) * np.array([positions[agent_index][0] - wall_position[0], positions[agent_index][1] - wall_position[1]])
    else:
        return 1e20 * np.array([positions[agent_index][0] - wall_position[0], positions[agent_index][1] - wall_position[1]])


# Contact function to model contact force between agents or with walls
def contact_function(x):
    if x > 1e-20:
        return 0
    else:
        contact_list.append('a')  # Log contact event
        return x


# Desired force function for agent i at a given time
def desired_force(i, positions, velocities):
    desired_velocity = v_max * exit_direction(i, positions)  # Desired velocity based on exit direction
    return (mass_agent / relaxation_time) * (desired_velocity - velocities[i])


# Social force function to calculate social forces between agents
def social_force(i, positions):
    social_force = np.zeros(2)
    num_agents = len(positions) // 2
    for j in range(num_agents):
        if j != i and state_dict[j] == 0:  # Exclude self-interaction and agents that have exited
            distance = agent_distance(i, j, positions)
            if distance < 2 * radius_agent:
                social_force += A_c * exp((2 * radius_agent - distance) / B_c) * interaction_direction(i, j, positions)
    
    # Interaction with walls
    for wall in wall_positions:
        if room_size / 2 >= euclidean_distance(wall, positions[i]) - radius_agent:
            social_force += A_c * exp((radius_agent - euclidean_distance(positions[i], wall)) / B_c) * wall_interaction_direction(i, wall, positions)
    
    return social_force


# Normal contact force function to handle collisions between agents and walls
def normal_contact_force(i, positions):
    normal_force = np.zeros(2)
    num_agents = len(positions) // 2
    for j in range(num_agents):
        if j != i and state_dict[j] == 0:  # Exclude self-interaction and agents that have exited
            interaction_vector = interaction_direction(i, j, positions)
            normal_force += agent_contact_normal * contact_function(agent_distance(i, j, positions) - 2 * radius_agent - 1) * interaction_vector
    
    # Interaction with walls
    for wall in wall_positions:
        normal_force += wall_contact_tangent * contact_function(euclidean_distance(positions[i], wall) - radius_agent - 1) * wall_interaction_direction(i, wall, positions)
    
    return normal_force


# Initialization of agents' positions and velocities
num_agents = 20
initial_positions = np.array([np.array([0., 0.])]*num_agents)
initial_velocities = np.array([np.array([0., 0.])]*num_agents)

# Function to check if an agent has exited
def has_exited(agent_index, positions):
    distance_to_exit = euclidean_distance(positions[agent_index], exit_center)
    if distance_to_exit <= sqrt(2) / 2:
        state_dict[agent_index] = 1  # Agent has exited
        return True
    return False


# Main simulation function
def simulate(num_iterations):
    positions = np.array([np.array([random.uniform(5, room_size - 5), random.uniform(5, room_size - 5)]) for _ in range(num_agents)])
    velocities = np.array([v_max * exit_direction(i, positions) for i in range(num_agents)]) * 0.5

    position_history = [positions]
    velocity_history = [velocities]
    acceleration_history = []

    for _ in range(num_iterations):
        accelerations = np.array([desired_force(i, positions, velocities) + social_force(i, positions) + normal_contact_force(i, positions) for i in range(num_agents)])
        
        new_positions = positions + time_step * velocities
        new_velocities = velocities + time_step * 0.5 * accelerations
        
        position_history.append(new_positions)
        velocity_history.append(new_velocities)
        acceleration_history.append(accelerations)
        
        positions = new_positions
        velocities = new_velocities
    
    return position_history


# Function to visualize the agent movement and the walls
def plot_positions(position_history):
    num_timesteps = len(position_history)
    plt.axis([-5, 55, -5, 55])
    
    for i in range(num_agents):
        color = (random.random(), random.random(), random.random())
        x_coords = [position_history[k][i][0] for k in range(num_timesteps)]
        y_coords = [position_history[k][i][1] for k in range(num_timesteps)]
        plt.plot(x_coords, y_coords, color=color, linestyle=":", marker=5)
    
    # Plot walls
    wall_x = [wall[0] for wall in wall_positions]
    wall_y = [wall[1] for wall in wall_positions]
    plt.scatter(wall_x, wall_y, color='black', marker='x')
    
    # Plot exit
    plt.scatter([exit_center[0]], [exit_center[1]], color='red')
    plt.axis("equal")
    plt.show()

# Run the simulation and plot results
position_history = simulate(100)
plot_positions(position_history)
