import heapq

class Node:
    def __init__(self, state, cost, heuristic, parent=None):
        self.state = state
        self.cost = cost
        self.heuristic = heuristic
        self.parent = parent

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def manhattan_distance(coord1, coord2):
    # Calculate Manhattan distance between two sets of coordinates
    x1, y1 = coord1
    x2, y2 = coord2
    return abs(x1 - x2) + abs(y1 - y2)

def uniform_cost_search(graph, start, goal):
    frontier = []
    heapq.heappush(frontier, Node(start, 0, 0))
    explored = set()

    while frontier:
        current_node = heapq.heappop(frontier)

        if current_node.state == goal:
            path = []
            while current_node:
                path.insert(0, current_node.state)
                current_node = current_node.parent
            return path

        explored.add(current_node.state)

        for neighbor, cost in graph[current_node.state].items():
            if neighbor not in explored:
                new_cost = current_node.cost + cost
                new_node = Node(neighbor, new_cost, 0, current_node)
                heapq.heappush(frontier, new_node)

    return []

def a_star_search(graph, start, goal, heuristic):
    frontier = []
    heapq.heappush(frontier, Node(start, 0, heuristic(start, goal)))
    explored = set()

    while frontier:
        current_node = heapq.heappop(frontier)

        if current_node.state == goal:
            path = []
            while current_node:
                path.insert(0, current_node.state)
                current_node = current_node.parent
            return path

        explored.add(current_node.state)

        for neighbor, cost in graph[current_node.state].items():
            if neighbor not in explored:
                new_cost = current_node.cost + cost
                heuristic_value = heuristic(neighbor, goal)
                new_node = Node(neighbor, new_cost, heuristic_value, current_node)
                heapq.heappush(frontier, new_node)

    return []

# Example usage with coordinates:
graph = {
    (0, 0): {(0, 1): 2,(1, 0): 1}, #A 
    (0, 1): {(0, 0): 2, (0, 2): 2 , (1, 1): 1}, #B
    (0, 2): {(0, 1): 2, (1, 2): 1}, #C
    (1, 0): {(0,0): 1, (1,1): 2, (2,0): 1}, #D
    (1, 1): {(0, 1): 1, (1, 2): 2, (2, 1): 1, (1, 0): 2}, #E
    (1, 2): {(1, 1): 2, (2, 2): 1, (0,2):1 }, #F
    (2, 0): {(1, 0): 1, (2,1): 2}, #G
    (2, 1): {(2, 0): 2, (1, 1): 1, (2,2): 2}, #H
    (2, 2): {(2, 1): 2, (1, 2): 1} #I
}

start_node = (0, 0)
goal_node = (0, 2)

# Uniform Cost Search
path_uniform_cost = uniform_cost_search(graph, start_node, goal_node)
if path_uniform_cost:
    print(f"Uniform Cost Search: Shortest path from {start_node} to {goal_node}: {path_uniform_cost}")
else:
    print(f"Uniform Cost Search: No path found from {start_node} to {goal_node}")

# A* Search with Manhattan Distance as Heuristic
path_a_star = a_star_search(graph, start_node, goal_node, manhattan_distance)
if path_a_star:
    print(f"A* Search: Shortest path from {start_node} to {goal_node}: {path_a_star}")
else:
    print(f"A* Search: No path found from {start_node} to {goal_node}")
