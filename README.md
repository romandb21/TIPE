# Crowd Movement Modeling

This project explores the modeling of crowd dynamics using two distinct approaches: **cellular automaton** and **molecular dynamics**. The goal is to understand and simulate how crowds behave under various conditions, such as navigating obstacles or interacting with other individuals. 

## Project Overview

### 1. **Cellular Automaton Model**:
   In the first model, we start with a basic **A\*** algorithm for pathfinding to simulate movement through a grid environment. However, we soon realized that the A\* algorithm was not the most efficient for our specific needs, especially when it came to handling obstacles in the environment. Therefore, we developed a custom pathfinding algorithm that is better suited for our simulation. This new algorithm takes into account the interactions between the crowd and obstacles, making the crowd's movement more realistic.

   **Key aspects of the cellular automaton model**:
   - The simulation grid is populated with cells that represent either free space or obstacles.
   - The pathfinding algorithm avoids obstacles and ensures that individuals move efficiently through the space.
   - The model simulates the collective behavior of individuals moving through the environment, taking into account various crowd dynamics.

### 2. **Molecular Dynamics Model**:
   The second model simulates crowd movement using principles from **molecular dynamics**, specifically the application of Newton’s equations of motion. We use **Verlet integration** to update the positions and velocities of individuals (represented as particles) over time.

   **Key aspects of the molecular dynamics model**:
   - Each individual in the crowd is modeled as a particle with properties such as position, velocity, and mass.
   - Newton’s second law is used to simulate the interactions between particles (representing individuals in the crowd), accounting for forces such as repulsion and attraction.
   - Verlet integration is used to update the particle positions at each timestep, ensuring stability in the simulation.

### 3. **MCOT**:
   The **MCOT** (Model Crowd Optimization Tool) is an additional resource in the project that describes the underlying structure of our models and provides auxiliary tools for simulation and visualization. It contains supporting code and configurations necessary to run the models and analyze the results.

## Files in the repository:

1. **`crowd_simulation_cellular_automaton.py`**: 
   Python implementation of the crowd simulation using a custom pathfinding algorithm for a cellular automaton-based model.
   
2. **`crowd_simulation_molecular_dynamics.py`**:
   Python implementation of the crowd simulation using molecular dynamics principles, with Newton's equations of motion and Verlet integration.

3. **`mcot`**:
   Additional resources that describe the project, the models, and the underlying theory. Includes configurations, utilities, and visualizations.

## Libraries used:
- **NumPy**: For efficient numerical operations, particularly array manipulations and mathematical calculations.
- **Matplotlib**: For visualizing the results of the simulations, including plotting particle trajectories and grid representations of the environment.


