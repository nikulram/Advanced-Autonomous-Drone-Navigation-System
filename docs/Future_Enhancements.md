
# Future Enhancements for Advanced Autonomous Drone Navigation System

## Introduction

This document outlines the future enhancements and goals for the Advanced Autonomous Drone Navigation System project. It explains the planned implementation of A* and Dijkstra’s algorithms, their respective use cases, and the reasons for their current absence in the project.

## Pathfinding Algorithms: A* and Dijkstra's

### What is A* Algorithm ?

A* (A-Star) is a pathfinding algorithm used to find the shortest path between a start and an end point. It uses a heuristic to guide its search, making it faster and more efficient, especially in large graphs.(Hart, P.E., Nilsson, N.J., Raphael, B., 1968).

#### Implementation

Below is the implementation of the A* algorithm. This code will be integrated into the project's 'navigation.py' file.:

import heapq

class AStarPlanner:
    def __init__(self, grid):
        self.grid = grid

    def heuristic(self, start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def get_neighbors(self, node):
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        result = []
        for n in neighbors:
            neighbor = (node[0] + n[0], node[1] + n[1])
            if 0 <= neighbor[0] < len(self.grid) and 0 <= neighbor[1] < len(self.grid[0]) and the grid[neighbor[0]][neighbor[1]] == 0:
                result.append(neighbor)
        return result

    def a_star(self, start, end):
        open_list = []
        heapq.heappush(open_list, (0 + self.heuristic(start, end), 0, start, None))
        g_scores = {start: 0}
        parents = {}

        while open_list:
            current = heapq.heappop(open_list)[2]

            if current == end:
                path = []
                while current:
                    path.append(current)
                    current = parents.get(current)
                return path[::-1]

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_scores[current] + 1
                if tentative_g_score < g_scores.get(neighbor, float('inf')):
                    g_scores[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, end)
                    heapq.heappush(open_list, (f_score, tentative_g_score, neighbor))
                    parents[neighbor] = current
        return []


### What is Dijkstra’s Algorithm ?

Dijkstra’s algorithm is used to find the shortest paths between nodes in a graph. It does not use a heuristic and is optimal for graphs with uniform edge weights. (Dijkstra, E.W., 1959).

#### Implementation

Below is the implementation of Dijkstra’s algorithm. This code will also be integrated into the project's navigation.py file.:


import heapq

class DijkstraPlanner:
    def __init__(self, grid):
        self.grid = grid

    def get_neighbors(self, node):
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        result = []
        for n in neighbors:
            neighbor = (node[0] + n[0], node[1] + n[1])
            if 0 <= neighbor[0] < len(self.grid) and 0 <= neighbor[1] < len(self.grid[0]) and the grid[neighbor[0]][neighbor[1]] == 0:
                result.append(neighbor)
        return result

    def dijkstra(self, start, end):
        queue = [(0, start)]
        distances = {start: 0}
        parents = {start: None}

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_node == end:
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = parents[current_node]
                return path[::-1]

            for neighbor in self.get_neighbors(current_node):
                distance = current_distance + 1
                if distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))
                    parents[neighbor] = current_node

        return []


### Integration and Usage

These pathfinding algorithms will be integrated into the `navigation.py` file of the project. Users can choose which algorithm to use based on their specific requirements:

- **A* Algorithm**: Best used when a heuristic can be applied to guide the search, making it faster for larger grids.
- **Dijkstra’s Algorithm**: Optimal for graphs with uniform weights or when a heuristic is not available.

#### Example Usage in 'navigation.py'.:


from pathfinding import AStarPlanner, DijkstraPlanner

class Navigation:
    def __init__(self, grid):
        self.a_star_planner = AStarPlanner(grid)
        self.dijkstra_planner = DijkstraPlanner(grid)

    def find_path(self, start, end, method='a_star'):
        if method == 'a_star':
            return self.a_star_planner.a_star(start, end)
        elif method == 'dijkstra':
            return self.dijkstra_planner.dijkstra(start, end)
        else:
            raise ValueError("Unknown method: choose 'a_star' or 'dijkstra'")

# Example usage can be :
if __name__ == "__main__":
    grid = [
        [0, 1, 0, 0],
        [0, 1, 0, 1],
        [0, 0, 0, 0],
        [1, 1, 0, 0]
    ]
    navigator = Navigation(grid)
    path = navigator.find_path((0, 0), (3, 3), method='a_star')
    print("Path found using A*:", path)
    path = navigator.find_path((0, 0), (3, 3), method='dijkstra')
    print("Path found using Dijkstra's:", path)


### Reasons for Current State

Due to time and resource constraints, I have not yet trained models or integrated these algorithms fully into the operational system. The current focus has been on establishing a strong foundational framework and simulating basic functionalities.
(NOTE : FUTURE UPDATES WILL POSSIBLY BE GIVEN IN THIS FILE)  


### References

Hart, P.E., Nilsson, N.J., Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths". IEEE Transactions on Systems Science and Cybernetics. 

Dijkstra, E.W. (1959). "A Note on Two Problems in Connexion with Graphs". Numerische Mathematik
