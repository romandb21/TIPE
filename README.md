# Crowd Movement Modeling

This project explores the modeling of crowd dynamics using two distinct approaches: **cellular automaton** and **molecular dynamics**. The goal is to understand and simulate how crowds behave under various conditions, such as navigating obstacles or interacting with other individuals. This project utilizes Python for simulation and visualization, incorporating different modeling techniques for realistic crowd movement behavior.

## Project Overview

### 1. **Cellular Automaton Model**:
   The first model simulates crowd movement using a **cellular automaton** approach. The simulation environment is represented by a grid where each cell can either be empty or contain an obstacle. Initially, we used the **A\*** pathfinding algorithm for individual movement. However, due to its limitations in efficiently handling obstacle interactions, a custom pathfinding algorithm was developed. This new algorithm takes into account the dynamic interaction between agents and obstacles, allowing for more realistic movement and crowd behavior.

   **Key aspects of the cellular automaton model**:
   - The environment is represented by a grid where each cell can either be free space or an obstacle.
   - The pathfinding algorithm guides agents through the grid, avoiding obstacles and adjusting for crowd interactions.
   - Each agent's movement is simulated based on the state of surrounding cells, considering social forces, agent-agent interaction, and local obstacles.

   **File**: **`crowd_simulation_cellular_automaton.py`**  
   This Python script implements the crowd simulation based on the cellular automaton model. The agents’ movements are determined by a custom pathfinding algorithm that avoids obstacles and optimizes the flow of the crowd.

### 2. **Molecular Dynamics Model**:
   The second model uses **molecular dynamics** principles, applying Newton's equations of motion to simulate interactions between crowd members. The agents are treated as particles with defined positions, velocities, and masses, and their movement is updated using **Verlet integration**.

   **Key aspects of the molecular dynamics model**:
   - Each agent is represented as a particle in the simulation with properties such as position, velocity, and mass.
   - Interactions between particles are modeled using forces such as repulsion and attraction, following Newton's second law.
   - Verlet integration is used to update the positions and velocities of particles over time, ensuring that the simulation remains stable and physically accurate.

   **File**: **`crowd_simulation_molecular_dynamics.py`**  
   This Python script implements the crowd simulation using molecular dynamics principles. The positions and velocities of particles are updated at each timestep based on the forces acting on them.

### 3. **MCOT (Model Crowd Optimization Tool)**:
   The **MCOT** (Model Crowd Optimization Tool) is an additional resource that provides auxiliary tools and configurations for the simulation. It contains supporting code necessary for running the models, analyzing the results, and visualizing the movement of agents.

   **Content**:
   - Supporting utilities for the models.
   - Configurations to set up the environment and adjust simulation parameters.
   - Visualization tools to plot the results of the simulations and analyze the behavior of agents.

## Files in the repository:

1. **`crowd_simulation_cellular_automaton.py`**:  
   Python implementation of the crowd simulation using a custom pathfinding algorithm in a cellular automaton-based model. It simulates agent movement in a grid environment while accounting for obstacle avoidance and social interactions.

2. **`crowd_simulation_molecular_dynamics.py`**:  
   Python implementation of the crowd simulation based on molecular dynamics principles. It simulates agent movement using Newton's equations of motion and updates positions with Verlet integration, taking into account repulsive and attractive forces between agents.

3. **`mcot`**:  
   A directory containing additional resources for the project, including configuration files, utilities, and visualization scripts to support the crowd simulation models.

## Libraries used:
- **NumPy**: For efficient numerical operations, particularly array manipulations, mathematical calculations, and the handling of large datasets in the simulations.
- **Matplotlib**: For visualizing the simulation results, including plotting the trajectories of agents and visual representations of the environment grid.
