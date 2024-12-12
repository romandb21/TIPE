from math import *
import numpy as np
import random
import matplotlib.pyplot as plt
import copy


def create_graph(n):
    """
    Create a graph of size n x n where each position (x, y) is associated with its neighbors
    according to the "diagonal" rule (including diagonals).
    """
    graph = {}  # Dictionary to hold positions (keys) and their neighbors (values)
    for i in range(n):
        for j in range(n):
            graph[(i, j)] = []  # Initialize empty neighbor lists for each position

    for i in range(n):
        for j in range(n):  # Current vertex at (i, j)
            for i1 in range(n):
                for j1 in range(n):  # Potential neighboring vertex at (i1, j1)
                    if abs(i - i1) < 2 and abs(j - j1) < 2 and not (i == i1 and j == j1):
                        graph[(i, j)].append((i1, j1))  # Add valid neighbor
    return graph


def dijkstra_algorithm(n, a, b):
    """
    Run Dijkstra's algorithm to calculate the minimum distance from all points to the target (a, b).
    """
    graph = create_graph(n)
    distances = {position: float("inf") for position in graph}
    distances[(a, b)] = 1  # Start from the exit position with a distance of 1
    to_visit = [(a, b)]  # List of positions to visit
    visited = []  # List of visited positions

    while to_visit:
        # Find the position with the smallest distance
        current_distance = distances[to_visit[0]]
        current_position = to_visit[0]
        index = 0  # Index in the to_visit list

        for i in range(len(to_visit)):
            if distances[to_visit[i]] < current_distance:
                current_position = to_visit[i]
                current_distance = distances[to_visit[i]]
                index = i

        to_visit.pop(index)  # Remove the current position from the to_visit list
        visited.append(current_position)  # Mark as visited

        for neighbor in graph[current_position]:
            if neighbor not in visited:
                distances[neighbor] = min(distances[neighbor], 1 + distances[current_position])
                to_visit.append(neighbor)
    
    return distances


def manhattan_distance_algorithm(n, a, b):
    """
    Calculate the Manhattan distance from each point to the target (a, b) and return the distances.
    """
    distances = {}
    for i in range(n):
        for j in range(n):
            distances[(i, j)] = 1 + sqrt(abs(i - a) ** 2 + abs(j - b) ** 2)
    return distances


def create_room_with_walls(n, a, b):
    """
    Create a room with walls set to a high value (500) and the rest with the Manhattan distance to (a, b).
    """
    room = {}
    for i in range(n):
        for j in range(n):
            room[(i, j)] = 1 + sqrt(abs(i - a) ** 2 + abs(j - b) ** 2)
    
    for i in range(n):
        room[(0, i)] = 500
        room[(n - 1, i)] = 500
        room[(i, 0)] = 500
        room[(i, n - 1)] = 500
    room[(a, b)] = 1  # Ensure the exit is not blocked by a wall
    return room


def display_graph(n, a, b):
    """
    Display the graph created by the manhattan_distance_algorithm.
    """
    distances = manhattan_distance_algorithm(n, a, b)
    matrix = np.array([[distances[(i, j)] for j in range(n)] for i in range(n)])
    return matrix


def display_room_with_walls(n, a, b):
    """
    Display the graph created by the create_room_with_walls function.
    """
    room = create_room_with_walls(n, a, b)
    matrix = np.array([[room[(i, j)] for j in range(n)] for i in range(n)])
    return matrix


def single_agent_path(n, a, b, c, d):
    """
    Find the path taken by a single agent starting from (c, d) to the exit (a, b) using the manhattan_distance_algorithm.
    """
    distances = manhattan_distance_algorithm(n, a, b)
    path = [(c, d)]
    current_position = (c, d)
    current_distance = distances[current_position]

    while current_distance != 1:
        x, y = current_position
        min_distance = float('inf')
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n:
                    if distances[(nx, ny)] < min_distance:
                        current_position = (nx, ny)
                        current_distance = distances[(nx, ny)]
                        min_distance = distances[(nx, ny)]

        path.append(current_position)
    
    return path


def display_agent_path(n, a, b, c, d):
    """
    Display the graph with the points corresponding to the agent's path.
    """
    path = single_agent_path(n, a, b, c, d)
    x = [point[0] for point in path]
    y = [point[1] for point in path]
    
    print(f"Number of steps: {len(path)}")
    plt.scatter(x, y)
    plt.show()


def all_agents_arrived(agents):
    """
    Check if all agents have arrived at the destination.
    """
    return all(distance == 1 for distance in agents.values())


def are_all_positions_different(agents_positions):
    """
    Check if all agents have different target positions.
    """
    positions = list(agents_positions.values())
    return len(positions) == len(set(positions))


def group_agents_by_target(agents_positions):
    """
    Group agents by their target positions.
    """
    target_groups = {}
    for agent, target in agents_positions.items():
        if target not in target_groups:
            target_groups[target] = [agent]
        else:
            target_groups[target].append(agent)
    return target_groups


def multiple_agents_path(n, a, b, num_agents):
    """
    Find the paths of multiple agents starting from random positions to the exit (a, b).
    """
    distances = manhattan_distance_algorithm(n, a, b)
    agent_paths = {}
    agents_positions = {}

    # Randomly assign starting positions to agents
    while len(agent_paths) < num_agents:
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        if (i, j) not in agent_paths:
            agent_paths[(i, j)] = [(i, j)]

    agent_distances = {position: distances[position] for position in agent_paths}
    agent_positions = {position: position for position in agent_paths}

    while not all_agents_arrived(agent_distances):
        previous_positions = copy.deepcopy(agent_positions)
        previous_distances = copy.deepcopy(agent_distances)

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for agent, position in agent_positions.items():
                    x, y = position
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < n and 0 <= new_y < n:
                        if agent_distances[agent] > distances[(new_x, new_y)]:
                            agent_distances[agent] = distances[(new_x, new_y)]
                            agent_positions[agent] = (new_x, new_y)

        if are_all_positions_different(agent_positions):
            for agent in agent_positions:
                agent_paths[agent].append(agent_positions[agent])
        else:
            target_groups = group_agents_by_target(agent_positions)
            for target, agents in target_groups.items():
                if len(agents) > 1:
                    chosen_agent = random.choice(agents)
                    for agent in agents:
                        if agent != chosen_agent:
                            agent_positions[agent] = previous_positions[agent]
                            agent_distances[agent] = previous_distances[agent]

            for agent in agent_positions:
                agent_paths[agent].append(agent_positions[agent])

    return agent_paths


def display_multiple_agents_path(n, a, b, num_agents):
    """
    Display the graph with the paths of multiple agents.
    """
    agent_paths = multiple_agents_path(n, a, b, num_agents)
    print(agent_paths)  # For visualization of agent paths
    x = {agent: [] for agent in agent_paths}
    y = {agent: [] for agent in agent_paths}

    for agent, path in agent_paths.items():
        for position in path:
            x[agent].append(position[0])
            y[agent].append(position[1])

    # Plotting
    figure, axes = plt.subplots()
    axes.set_aspect(1)

    for agent in agent_paths:
        plt.scatter(agent_paths[agent][0][0], agent_paths[agent][0][1], marker='o')
        plt.plot(x[agent], y[agent])

    plt.xlim(0, n)
    plt.ylim(0, n)
    plt.title(f"Evacuation of a {n} x {n} room for {num_agents} agents", fontstyle='italic')
    plt.scatter(a, b, color='red', marker='>', s=400)
    plt.annotate(f"Evacuation time: {(len(x[agent]) - 1) * 0.2}s", (x[agent][-1], y[agent][-1]))
    plt.show()
