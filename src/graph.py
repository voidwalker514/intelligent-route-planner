"""
=============================================================
  Intelligent Route Planner - Graph Module
  File: src/graph.py
  Description: Core graph data structure using Adjacency List
               supporting directed/undirected weighted graphs
=============================================================
"""

from collections import defaultdict


class Graph:
    """
    Weighted Graph using Adjacency List representation.

    Each node represents a location/city.
    Each edge represents a road with attributes:
      - distance (km)
      - time     (minutes)
      - cost     (INR)
    """

    def __init__(self, directed: bool = False):
        """
        Initialize the graph.

        Args:
            directed (bool): If True, edges are one-directional.
                             If False (default), edges are bidirectional.
        """
        # adjacency_list[node] = list of (neighbor, {distance, time, cost})
        self.adjacency_list: dict = defaultdict(list)
        self.nodes: set = set()
        self.directed = directed

    # ------------------------------------------------------------------
    # Node & Edge Management
    # ------------------------------------------------------------------

    def add_node(self, location: str):
        """Add a location node to the graph."""
        self.nodes.add(location)
        # Ensure it has an entry in the adjacency list
        if location not in self.adjacency_list:
            self.adjacency_list[location] = []

    def add_edge(self, source: str, destination: str,
                 distance: float, time: float, cost: float = 0.0):
        """
        Add a weighted edge between two locations.

        Args:
            source      : Starting location
            destination : Ending location
            distance    : Distance in kilometres
            time        : Travel time in minutes
            cost        : Travel cost in INR (optional, default 0)
        """
        # Auto-register nodes
        self.add_node(source)
        self.add_node(destination)

        weight = {"distance": distance, "time": time, "cost": cost}

        self.adjacency_list[source].append((destination, weight))

        # For undirected graphs add reverse edge too
        if not self.directed:
            self.adjacency_list[destination].append((source, weight))

    def remove_edge(self, source: str, destination: str):
        """Remove the edge between source and destination."""
        self.adjacency_list[source] = [
            (n, w) for n, w in self.adjacency_list[source] if n != destination
        ]
        if not self.directed:
            self.adjacency_list[destination] = [
                (n, w) for n, w in self.adjacency_list[destination] if n != source
            ]

    def get_neighbors(self, location: str) -> list:
        """Return all neighbors of a given location."""
        return self.adjacency_list.get(location, [])

    def get_all_nodes(self) -> list:
        """Return all nodes sorted alphabetically."""
        return sorted(list(self.nodes))

    def get_edge_weight(self, source: str, destination: str,
                        weight_type: str = "distance"):
        """
        Get specific weight of an edge.

        Args:
            weight_type: 'distance' | 'time' | 'cost'
        Returns:
            float weight or None if edge doesn't exist
        """
        for neighbor, weight in self.adjacency_list.get(source, []):
            if neighbor == destination:
                return weight.get(weight_type, None)
        return None

    # ------------------------------------------------------------------
    # Graph Information
    # ------------------------------------------------------------------

    def node_count(self) -> int:
        """Total number of nodes."""
        return len(self.nodes)

    def edge_count(self) -> int:
        """Total number of unique edges."""
        total = sum(len(neighbors) for neighbors in self.adjacency_list.values())
        return total if self.directed else total // 2

    def display(self):
        """Print the entire adjacency list (human-readable)."""
        print("\n" + "=" * 60)
        print("  GRAPH - ADJACENCY LIST")
        print("=" * 60)
        print(f"  Nodes : {self.node_count()}  |  Edges : {self.edge_count()}")
        print(f"  Type  : {'Directed' if self.directed else 'Undirected'}")
        print("-" * 60)
        for node in self.get_all_nodes():
            neighbors = self.adjacency_list[node]
            if neighbors:
                print(f"\n  📍 {node}")
                for neighbor, w in neighbors:
                    print(f"       ──▶  {neighbor:<25} "
                          f"[{w['distance']} km | {w['time']} min | ₹{w['cost']}]")
            else:
                print(f"\n  📍 {node}  (no outgoing edges)")
        print("=" * 60)

    def to_dict(self) -> dict:
        """Serialize the graph to a plain dictionary."""
        return {
            "directed": self.directed,
            "nodes": list(self.nodes),
            "edges": {
                node: neighbors
                for node, neighbors in self.adjacency_list.items()
            }
        }
