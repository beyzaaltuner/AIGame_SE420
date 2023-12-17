import heapq
import itertools  # Used for generating unique identifiers
import tkinter as tk


class Node:
    _ids = itertools.count()

    def __init__(self, row, col, value='_'):
        self.row = row
        self.col = col
        self.value = value
        self.neighbors = []
        self.id = next(self._ids)

    def add_neighbor(self, neighbor, cost):
        self.neighbors.append((neighbor, cost))

    def remove_neighbor(self, neighbor):
        self.neighbors = [(n, cost) for n, cost in self.neighbors if n != neighbor]    


# Create a 3x3 grid of nodes
grid = [[Node(row, col) for col in range(3)] for row in range(3)]

# Function to connect neighbors in the grid
def connect_neighbors():
    for row in range(3):
        for col in range(3):
            current_node = grid[row][col]

            # Connect with right neighbor
            if col < 2:
                current_node.add_neighbor(grid[row][col + 1], 2)

            # Connect with left neighbor
            if col > 0:
                current_node.add_neighbor(grid[row][col - 1], 2)

            # Connect with bottom neighbor
            if row < 2:
                current_node.add_neighbor(grid[row + 1][col], 1)

            # Connect with top neighbor
            if row > 0:
                current_node.add_neighbor(grid[row - 1][col], 1)

    # Allow the user to add walls between nodes
    add_wall_between_nodes()            

def add_wall_between_nodes():
    print("Enter the coordinates of the first node (row col): ")
    row1, col1 = map(int, input().split())

    print("Enter the coordinates of the second node (row col): ")
    row2, col2 = map(int, input().split())

    # Check if the input coordinates are valid
    if 0 <= row1 < 3 and 0 <= col1 < 3 and 0 <= row2 < 3 and 0 <= col2 < 3:
        # Remove neighbors to create a wall
        grid[row1][col1].remove_neighbor(grid[row2][col2])
        grid[row2][col2].remove_neighbor(grid[row1][col1])
        print("Wall added successfully!")
    else:
        print("Invalid coordinates. Please enter coordinates within the grid (0-2).")


# Uniform Cost Search Algorithm
def uniform_cost_search(start, goal, max_expanded_nodes=10):
    heap = [(0, start.id, start, [])]  # Priority queue to store (cost, id, node, path) tuples
    visited = set()

    while heap and len(visited) < max_expanded_nodes:
        current_cost, _, current_node, current_path = heapq.heappop(heap)
        
        if current_node in visited:
            continue

        visited.add(current_node)

        current_path = current_path + [(current_node.row, current_node.col)]

        print(f"Expanded Node: ({current_node.row}, {current_node.col}), Cost: {current_cost}")

        if current_node == goal:
            print(f"Goal reached! Final Path: {current_path}, Cost: {current_cost}")
            return

        for neighbor, cost in current_node.neighbors:
            heapq.heappush(heap, (current_cost + cost, neighbor.id, neighbor, current_path))


# Calculate Manhattan distance heuristic
def manhattan_distance(node, goal):
    return abs(node.row - goal.row) + abs(node.col - goal.col)

# A* Search Algorithm
def a_star_search(start, goal, max_expanded_nodes=10):
    heap = [(0, 0, start.id, start, [])]  # Priority queue to store (f, g, id, node, path) tuples
    visited = set()

    while heap and len(visited) < max_expanded_nodes:
        _, g, _, current_node, current_path = heapq.heappop(heap)
        
        if current_node in visited:
            continue

        visited.add(current_node)

        current_path = current_path + [(current_node.row, current_node.col)]

        h = manhattan_distance(current_node, goal)
        print(f"Expanded Node: ({current_node.row}, {current_node.col}), Cost: {g}, Heuristic: {h}")

        if current_node == goal:
            print(f"Goal reached! Final Path: {current_path}, Cost: {g}")
            return

        neighbors = [(neighbor, cost) for neighbor, cost in current_node.neighbors if neighbor.row == current_node.row]
        neighbors.sort(key=lambda x, g=g: (g + x[1], x[0].row, x[0].col))

        for neighbor, cost in neighbors:
            h_neighbor = manhattan_distance(neighbor, goal)
            f = g + cost + h_neighbor
            heapq.heappush(heap, (f, g + cost, neighbor.id, neighbor, current_path))


# Call the function to connect neighbors
connect_neighbors()

# Set the source and goal nodes
source_node = grid[0][0]
goal_node = grid[0][2]

# Run Uniform Cost Search
uniform_cost_search(source_node, goal_node)
# Run A* Search
a_star_search(source_node, goal_node)