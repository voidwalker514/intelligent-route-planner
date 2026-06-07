"""
=============================================================
  Intelligent Route Planner - Algorithms Module
  File: src/algorithms.py
  Description: BFS, DFS, and Dijkstra's Algorithm
               implementations with route reconstruction
=============================================================
"""

import heapq
from collections import deque
from src.graph import Graph


# ==============================================================
# 1. BFS - Breadth-First Search (Unweighted Shortest Path)
# ==============================================================

def bfs(graph: Graph, source: str, destination: str) -> dict:
    """
    Breadth-First Search — finds the path with the FEWEST HOPS
    (not necessarily shortest distance).

    How it works:
      - Uses a queue (FIFO).
      - Explores all neighbors at the current depth before going deeper.
      - Guarantees shortest path by number of edges (hops).

    Args:
        graph       : Graph object
        source      : Starting location
        destination : Target location

    Returns:
        dict with keys: path, hops, found
    """
    if source not in graph.nodes or destination not in graph.nodes:
        return {"path": [], "hops": 0, "found": False,
                "error": "Source or destination not in graph."}

    # Queue stores (current_node, path_so_far)
    queue = deque()
    queue.append((source, [source]))
    visited = set()
    visited.add(source)

    while queue:
        current, path = queue.popleft()

        if current == destination:
            return {
                "path": path,
                "hops": len(path) - 1,
                "found": True
            }

        for neighbor, _ in graph.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return {"path": [], "hops": 0, "found": False,
            "error": f"No path found from {source} to {destination}."}


# ==============================================================
# 2. DFS - Depth-First Search (Path Existence Check)
# ==============================================================

def dfs(graph: Graph, source: str, destination: str) -> dict:
    """
    Depth-First Search — explores as deep as possible before backtracking.

    How it works:
      - Uses a stack (LIFO).
      - Does NOT guarantee shortest path.
      - Useful for: connectivity check, maze solving, cycle detection.

    Args:
        graph       : Graph object
        source      : Starting location
        destination : Target location

    Returns:
        dict with keys: path, hops, found
    """
    if source not in graph.nodes or destination not in graph.nodes:
        return {"path": [], "hops": 0, "found": False,
                "error": "Source or destination not in graph."}

    # Stack stores (current_node, path_so_far)
    stack = [(source, [source])]
    visited = set()

    while stack:
        current, path = stack.pop()

        if current in visited:
            continue
        visited.add(current)

        if current == destination:
            return {
                "path": path,
                "hops": len(path) - 1,
                "found": True
            }

        for neighbor, _ in graph.get_neighbors(current):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return {"path": [], "hops": 0, "found": False,
            "error": f"No path found from {source} to {destination}."}


# ==============================================================
# 3. Dijkstra's Algorithm (Optimized with Min-Heap / Priority Queue)
# ==============================================================

def dijkstra(graph: Graph, source: str, destination: str,
             weight_type: str = "distance") -> dict:
    """
    Dijkstra's Shortest Path Algorithm.

    How it works:
      - Uses a Min-Heap (Priority Queue) for greedy selection.
      - Maintains a 'dist' table — minimum cost to reach each node.
      - Maintains a 'prev' table — previous node on optimal path.
      - At each step: pick the unvisited node with smallest dist,
        then relax all its edges.

    Time Complexity : O((V + E) log V)
    Space Complexity: O(V)

    Args:
        graph       : Graph object
        source      : Starting location
        destination : Target location
        weight_type : 'distance' | 'time' | 'cost'

    Returns:
        dict with keys:
          path           - ordered list of locations
          total_distance - total km
          total_time     - total minutes
          total_cost     - total cost in INR
          found          - bool
    """
    if source not in graph.nodes or destination not in graph.nodes:
        return {
            "path": [], "total_distance": 0, "total_time": 0,
            "total_cost": 0, "found": False,
            "error": "Source or destination not in graph."
        }

    # ---- Initialization ----
    INF = float("inf")

    # dist[node] = minimum accumulated weight from source
    dist = {node: INF for node in graph.nodes}
    dist[source] = 0

    # Store all weights separately for reporting
    dist_distance = {node: INF for node in graph.nodes}
    dist_time     = {node: INF for node in graph.nodes}
    dist_cost     = {node: INF for node in graph.nodes}
    dist_distance[source] = 0
    dist_time[source]     = 0
    dist_cost[source]     = 0

    # prev[node] = node that came before it on shortest path
    prev = {node: None for node in graph.nodes}

    visited = set()

    # Min-Heap: (priority_weight, node)
    heap = [(0, source)]

    # ---- Main Loop ----
    while heap:
        current_dist, current_node = heapq.heappop(heap)

        # Skip if already processed
        if current_node in visited:
            continue
        visited.add(current_node)

        # Early exit once destination is settled
        if current_node == destination:
            break

        # ---- Edge Relaxation ----
        for neighbor, weight in graph.get_neighbors(current_node):
            if neighbor in visited:
                continue

            edge_weight = weight.get(weight_type, INF)
            new_dist = current_dist + edge_weight

            if new_dist < dist[neighbor]:
                dist[neighbor]          = new_dist
                dist_distance[neighbor] = dist_distance[current_node] + weight["distance"]
                dist_time[neighbor]     = dist_time[current_node]     + weight["time"]
                dist_cost[neighbor]     = dist_cost[current_node]     + weight["cost"]
                prev[neighbor]          = current_node
                heapq.heappush(heap, (new_dist, neighbor))

    # ---- Path Reconstruction ----
    if dist[destination] == INF:
        return {
            "path": [], "total_distance": 0, "total_time": 0,
            "total_cost": 0, "found": False,
            "error": f"No path found from '{source}' to '{destination}'."
        }

    path = _reconstruct_path(prev, source, destination)

    return {
        "path"           : path,
        "total_distance" : round(dist_distance[destination], 2),
        "total_time"     : round(dist_time[destination], 2),
        "total_cost"     : round(dist_cost[destination], 2),
        "optimized_by"   : weight_type,
        "found"          : True
    }


# ==============================================================
# 4. All-Pairs Shortest Path summary (runs Dijkstra from every node)
# ==============================================================

def all_pairs_shortest_path(graph: Graph, weight_type: str = "distance") -> dict:
    """
    Compute shortest paths between every pair of nodes.

    Useful for: pre-computing route tables, analytics.

    Returns:
        dict[source][destination] = dijkstra_result
    """
    results = {}
    for node in graph.get_all_nodes():
        results[node] = {}
        for other in graph.get_all_nodes():
            if node != other:
                results[node][other] = dijkstra(graph, node, other, weight_type)
    return results


# ==============================================================
# Helper: Reconstruct path from 'prev' table
# ==============================================================

def _reconstruct_path(prev: dict, source: str, destination: str) -> list:
    """
    Trace backwards from destination to source using prev dict.

    Returns:
        List of nodes from source → destination
    """
    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = prev[current]

    path.reverse()

    # Validate reconstruction
    if path[0] != source:
        return []

    return path
