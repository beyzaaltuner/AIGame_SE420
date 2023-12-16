import heapq

class Node:
    def __init__(self, state, cost, parent=None):
        self.state = state
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost
    

def uniform_cost_search(graph, start, goal):
    
    frontier = []
    heapq.heappush(frontier, Node(start, 0))

    
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
                new_node = Node(neighbor, new_cost, current_node)
                heapq.heappush(frontier, new_node)

    
    return []


graph = {
    'A': {'B': 2},
    'B': {'A': 2, 'E': 1},
    'C': {'F': 1},
    'D': {'E': 2,'G': 1},
    'E': {'B': 1, 'D': 2, 'F': 2, 'H': 1},
    'F': {'C': 1, 'E': 2 ,'I': 1},
    'G': {'D': 1},
    'H': {'I': 2, 'E': 1},
    'I': {'F':1,'H':2}
}

start_node = 'A'
goal_node = 'C'

path = uniform_cost_search(graph, start_node, goal_node)

if path:
    print(f"Shortest path from {start_node} to {goal_node}: {path}")
else:
    print(f"No path found from {start_node} to {goal_node}")
