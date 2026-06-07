# 🗺️ Intelligent Route Planner Using Graph Algorithms

> A complete DSA project demonstrating **Dijkstra's Algorithm**, **BFS**, **DFS**, and **Priority Queue (Min-Heap)** on a real-world city road network — built for GitHub portfolios, DSA interviews, and software engineering roles.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Algorithm](https://img.shields.io/badge/Algorithm-Dijkstra%20%7C%20BFS%20%7C%20DFS-orange?style=flat-square)
![Data Structure](https://img.shields.io/badge/DS-Graph%20%7C%20Min--Heap%20%7C%20Adjacency%20List-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)
![Tests](https://img.shields.io/badge/Tests-15%20Passed-brightgreen?style=flat-square)

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Problem Statement](#-problem-statement)
3. [Real-World Applications](#-real-world-applications)
4. [DSA Concepts Used](#-dsa-concepts-used)
5. [Algorithm Explanation](#-algorithm-explanation)
6. [Project Architecture](#-project-architecture)
7. [Folder Structure](#-folder-structure)
8. [Tech Stack](#-tech-stack)
9. [Installation](#-installation)
10. [How to Run](#-how-to-run)
11. [Sample Output](#-sample-output)
12. [Graph Visualization](#-graph-visualization)
13. [Features](#-features)
14. [Learning Outcomes](#-learning-outcomes)
15. [Interview Questions](#-interview-questions)
16. [Contributing](#-contributing)

---

## 🎯 Project Overview

The **Intelligent Route Planner** is a Python-based CLI application that models a city road network as a **weighted graph** and finds the most optimal travel route between any two locations using three classical graph algorithms:

| Algorithm | Optimizes For | Data Structure Used |
|-----------|--------------|---------------------|
| **Dijkstra's** | Shortest distance / Minimum time / Minimum cost | Min-Heap (Priority Queue) |
| **BFS** | Fewest intermediate stops (hops) | Queue (deque) |
| **DFS** | Path existence check, deep exploration | Stack (list) |

The project uses **20+ major Indian cities** as nodes with real distances (km), travel time (min), and road cost (INR) as edge weights — making the simulation realistic and engaging.

---

## 🔴 Problem Statement

> **How do apps like Google Maps, Uber, Swiggy, and Ola find the fastest or cheapest route between two points in real time?**

At their core, these applications model roads as a **graph** where:
- **Locations** = Graph Nodes (Vertices)
- **Roads** = Graph Edges
- **Distance / Time / Cost** = Edge Weights

The challenge is: **given a source and destination, find the optimal path** through potentially thousands of interconnected roads — efficiently.

This project solves that problem using classical DSA algorithms on a real city dataset.

---

## 🌍 Real-World Applications

| Industry | Company | How Route Planning Is Used |
|----------|---------|---------------------------|
| Navigation | Google Maps, Apple Maps | Dijkstra / A* for shortest path |
| Ride Sharing | Uber, Ola | Nearest driver + optimal route |
| Food Delivery | Swiggy, Zomato | Multi-stop delivery optimization |
| Logistics | Amazon, FedEx, Delhivery | Fleet routing, last-mile delivery |
| Public Transport | Railways, Metro, Bus | Timetable + shortest path scheduling |
| Social Networks | Facebook, LinkedIn | BFS for "degrees of separation" |

---

## 📚 DSA Concepts Used

```
Graph Theory
├── Adjacency List Representation
├── Weighted Edges (Distance, Time, Cost)
├── Directed vs Undirected Graphs
├── Connected Components
└── Graph Traversal

Algorithms
├── Dijkstra's Shortest Path (Greedy + DP)
├── BFS — Breadth-First Search
├── DFS — Depth-First Search
└── Path Reconstruction (Backtracking via prev[] table)

Data Structures
├── Min-Heap / Priority Queue (heapq)
├── Hash Map / Dictionary
├── Set (visited tracking)
├── Queue / deque (BFS)
└── Stack / list (DFS)

Complexity Analysis
├── Dijkstra: O((V + E) log V)
├── BFS: O(V + E)
└── DFS: O(V + E)
```

---

## ⚙️ Algorithm Explanation

### 1. Dijkstra's Algorithm — The Core Engine

```
INITIALIZE:
  dist[source] = 0
  dist[all others] = INFINITY
  prev[all] = None
  heap = [(0, source)]

LOOP while heap is not empty:
  (current_dist, current_node) = heappop(heap)   ← Pick minimum

  if current_node == destination: STOP (early exit)

  FOR each neighbor of current_node:
    new_dist = current_dist + edge_weight(current_node, neighbor)

    IF new_dist < dist[neighbor]:
      dist[neighbor] = new_dist                  ← Relax edge
      prev[neighbor] = current_node              ← Track path
      heappush(heap, (new_dist, neighbor))

RECONSTRUCT PATH:
  Backtrack from destination → source using prev[]
  Reverse to get source → destination path
```

**Why it works:** Dijkstra uses a greedy approach. By always expanding the unvisited node with the **minimum known distance**, it guarantees that when a node is first popped from the heap, its distance is already optimal (for non-negative weights).

---

### 2. BFS — Breadth-First Search

```
queue = [(source, [source])]
visited = {source}

LOOP:
  (current, path) = queue.popleft()
  if current == destination: return path

  FOR neighbor in adjacency_list[current]:
    if neighbor not in visited:
      visited.add(neighbor)
      queue.append((neighbor, path + [neighbor]))
```

**Finds:** Path with minimum number of **hops** (edges), not minimum weight.

---

### 3. DFS — Depth-First Search

```
stack = [(source, [source])]

LOOP:
  (current, path) = stack.pop()
  if current == destination: return path

  FOR neighbor in adjacency_list[current]:
    if neighbor not in visited:
      stack.append((neighbor, path + [neighbor]))
```

**Finds:** A valid path (not guaranteed optimal). Useful for connectivity checks.

---

## 🏗️ Project Architecture

```
INPUT
  └── Source City + Destination City + Weight Preference
         │
         ▼
GRAPH CREATION
  └── City nodes added to Adjacency List
  └── Roads added as weighted edges (distance/time/cost)
         │
         ▼
ALGORITHM SELECTION
  ├── Dijkstra (distance / time / cost)
  ├── BFS (fewest hops)
  └── DFS (depth-first path)
         │
         ▼
SHORTEST PATH COMPUTATION
  └── Min-Heap processes nodes in priority order
  └── dist[] and prev[] tables updated
  └── Early exit on destination found
         │
         ▼
PATH RECONSTRUCTION
  └── Backtrack prev[] from destination → source
  └── Reverse to get: source → ... → destination
         │
         ▼
OUTPUT
  ├── Route sequence (city by city)
  ├── Total distance (km)
  ├── Total travel time (hours/minutes)
  ├── Total cost (INR)
  ├── Saved report (.txt)
  └── Graph visualization (.png)
```

---

## 📁 Folder Structure

```
Intelligent-Route-Planner-Graph-Algorithms/
│
├── src/                        # All source modules
│   ├── __init__.py             # Package initializer
│   ├── graph.py                # Graph data structure (Adjacency List)
│   ├── algorithms.py           # BFS, DFS, Dijkstra implementations
│   ├── city_data.py            # India city dataset + demo graph builder
│   ├── report.py               # Route report formatter & file saver
│   ├── visualizer.py           # NetworkX + Matplotlib graph drawer
│   └── cli.py                  # Interactive CLI menu
│
├── data/                       # Dataset documentation
│   └── README.md
│
├── outputs/                    # Generated route reports (auto-created)
│   ├── route_mumbai_to_delhi_*.txt
│   └── demo_comparison_*.json
│
├── images/                     # Graph visualizations (auto-created)
│   ├── india_map_Mumbai_to_Delhi_distance.png
│   └── demo_graph_shortest_path.png
│
├── docs/                       # Extended documentation
│   ├── PROJECT_EXPLANATION.md
│   ├── ARCHITECTURE.md
│   ├── IMPLEMENTATION_PLAN.md
│   └── INTERVIEW_PREP.md
│
├── main.py                     # Entry point (CLI / demo / test)
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git exclusion rules
└── README.md                   # This file
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.8+ | Core development |
| Graph DS | Custom (Adjacency List) | Store nodes and edges |
| Algorithm | Dijkstra's + BFS + DFS | Route computation |
| Priority Queue | `heapq` (stdlib) | Min-Heap for Dijkstra |
| Visualization | `networkx` + `matplotlib` | Graph drawing |
| CLI | Python `input()` + stdlib | User interface |
| Output | File I/O + JSON | Report saving |

---

## ⚡ Installation

### Prerequisites
- Python 3.8 or above
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/[your-username]/Intelligent-Route-Planner-Graph-Algorithms.git
cd Intelligent-Route-Planner-Graph-Algorithms
```

### Step 2: (Optional) Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

### Mode 1: Interactive CLI Menu
```bash
python main.py
```
Follow the on-screen menu to select graph, algorithm, source, and destination.

### Mode 2: Automated Full Demo (No Input Required)
```bash
# Windows
set PYTHONIOENCODING=utf-8
python main.py --demo

# Mac/Linux
PYTHONIOENCODING=utf-8 python main.py --demo
```
Runs 5 demo routes, generates reports in `outputs/` and visualizations in `images/`.

### Mode 3: Run Algorithm Tests
```bash
python main.py --test
```
Runs 15 automated correctness tests across all algorithms.

---

## 📊 Sample Output

### Dijkstra's Algorithm — Mumbai → Delhi (Minimum Distance)
```
=================================================================
  INTELLIGENT ROUTE PLANNER  —  ROUTE REPORT
=================================================================
  Algorithm   : Dijkstra's (Min Distance)
  Source      : Mumbai
  Destination : Delhi
  Timestamp   : 2026-06-06 00:22:13
-----------------------------------------------------------------

  ROUTE FOUND (3 stops)

  Route Sequence:
     Mumbai  →  Ahmedabad  →  Jaipur  →  Delhi

-----------------------------------------------------------------

  ROUTE METRICS  (Optimized by: DISTANCE)

  Total Distance         1470 km
  Total Travel Time      23h 0m  (1380 min)
  Total Cost             INR 1990
  Total Stops            4 locations
  Hops (Edges)           3
=================================================================
```

### Algorithm Comparison — Mumbai → Delhi
```
BFS (Fewest Hops)      : Mumbai → Ahmedabad → Jaipur → Delhi       | 3 hops
DFS (Depth-First)      : Mumbai → Nashik → ... → Delhi              | 11 hops
Dijkstra (Min Dist)    : Mumbai → Ahmedabad → Jaipur → Delhi        | 1470 km
Dijkstra (Min Time)    : Mumbai → Ahmedabad → Jaipur → Delhi        | 23h 0m
Dijkstra (Min Cost)    : Mumbai → Ahmedabad → Jaipur → Delhi        | INR 1990
```

> **Key Insight:** DFS found a path through 11 cities (2x longer!), while Dijkstra found the true optimal 3-hop route. This is exactly why real navigation apps use Dijkstra, not DFS.

---

## 🖼️ Graph Visualization

The project generates dark-themed graph plots using NetworkX + Matplotlib:

- **Green node** = Source city
- **Red node** = Destination city
- **Orange nodes/edges** = Shortest path
- **Blue nodes** = Other cities
- **Grey edges** = Non-optimal roads

Visualization files are saved to the `images/` folder automatically.

---

## ✅ Features

- [x] Weighted graph using **Adjacency List** (industry standard)
- [x] **Dijkstra's Algorithm** with Min-Heap — optimized by distance, time, or cost
- [x] **BFS** for minimum-hop path finding
- [x] **DFS** for path exploration and connectivity
- [x] **20+ Indian cities** with realistic distances, times, and costs
- [x] **8-node demo graph** for beginner-friendly testing
- [x] **Algorithm Comparison** — shows why Dijkstra beats BFS/DFS for weights
- [x] **Route Report** — saved as `.txt` and `.json`
- [x] **Graph Visualization** — dark-themed PNG with highlighted shortest path
- [x] **Interactive CLI** — menu-driven, no GUI needed
- [x] **Automated Demo Mode** — `python main.py --demo`
- [x] **Test Suite** — 15 correctness checks, `python main.py --test`
- [x] **Modular Code** — 5 separate modules, fully commented
- [x] **Windows / Mac / Linux** compatible

---

## 🎓 Learning Outcomes

After completing this project, you will understand:

1. **Graph Theory** — Nodes, edges, weights, directed vs undirected
2. **Adjacency List** — Why it's preferred over adjacency matrix for sparse graphs
3. **Dijkstra's Algorithm** — Greedy approach, edge relaxation, correctness proof
4. **Priority Queue / Min-Heap** — How `heapq` enables O(log n) minimum extraction
5. **BFS vs DFS** — When to use each, their trade-offs
6. **Path Reconstruction** — Using a `prev[]` table to backtrack the optimal path
7. **Complexity Analysis** — O((V+E) log V) for Dijkstra, O(V+E) for BFS/DFS
8. **Real-World Modeling** — How navigation systems translate maps to graphs
9. **Software Architecture** — Modular Python project structure
10. **GitHub Portfolio** — How to present DSA work professionally

---

## 💼 Interview Questions

> See `docs/INTERVIEW_PREP.md` for 30+ detailed Q&A covering:

- Why Dijkstra fails on negative weights (use Bellman-Ford)
- Difference between BFS and Dijkstra
- How to detect cycles in a graph
- What is a Min-Heap and how does it work?
- Time and space complexity of all algorithms
- How Google Maps uses A* (Dijkstra extension) with heuristics
- How to handle disconnected graphs

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/add-astar`
3. Commit changes: `git commit -m "feat: Add A* algorithm"`
4. Push and open a PR

---

## 📄 License

This project is licensed under the **MIT License** — use it freely for learning and portfolio.

---



> ⭐ **Star this repository** if it helped you learn graph algorithms!
> Built with ❤️ as a DSA portfolio project.
