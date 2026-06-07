"""
=============================================================
  Intelligent Route Planner - CLI Menu Module
  File: src/cli.py
  Description: Interactive command-line interface for the
               route planner. Menus, input validation, etc.
=============================================================
"""

import sys
import os

# Ensure src/ imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import Graph
from src.algorithms import bfs, dfs, dijkstra
from src.report import (print_route_report, print_comparison_report,
                        save_report_to_file, save_json_report)
from src.city_data import build_india_city_graph, build_small_demo_graph
from src.visualizer import (draw_india_map, draw_small_demo,
                             draw_graph, VISUALIZATION_AVAILABLE)


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print("""
+--------------------------------------------------------------+
|                                                              |
|   [MAP] INTELLIGENT ROUTE PLANNER                           |
|         Using Graph Algorithms (DSA Project)                 |
|                                                              |
|   Algorithms : BFS | DFS | Dijkstra's (Min-Heap)             |
|   Dataset    : 20+ Indian Cities / Custom Demo Graph         |
|   Author     : [Your Name]  -  GitHub DSA Portfolio          |
|                                                              |
+--------------------------------------------------------------+
""")


def pick_graph() -> tuple:
    """
    Let user choose between India city graph or small demo graph.
    Returns (Graph, graph_name)
    """
    print("  Select Graph Dataset:")
    print("  [1] India City Map (20+ cities, real distances)")
    print("  [2] Small Demo City (8 locations, beginner-friendly)")
    choice = input("\n  Enter choice (1 or 2): ").strip()

    if choice == "2":
        return build_small_demo_graph(), "small_demo"
    return build_india_city_graph(), "india"


def pick_algorithm() -> str:
    """Let user pick an algorithm."""
    print("\n  Select Algorithm:")
    print("  [1] Dijkstra's — Shortest Distance")
    print("  [2] Dijkstra's — Minimum Time")
    print("  [3] Dijkstra's — Minimum Cost")
    print("  [4] BFS — Fewest Hops")
    print("  [5] DFS — Depth-First Path")

    mapping = {
        "1": ("dijkstra", "distance"),
        "2": ("dijkstra", "time"),
        "3": ("dijkstra", "cost"),
        "4": ("bfs",      None),
        "5": ("dfs",      None),
    }

    while True:
        choice = input("\n  Enter choice (1-5): ").strip()
        if choice in mapping:
            return mapping[choice]
        print("  ⚠️  Invalid choice. Please enter 1-5.")


def pick_locations(graph: Graph) -> tuple:
    """Let user pick source and destination from node list."""
    nodes = graph.get_all_nodes()
    print(f"\n  Available Locations ({len(nodes)} total):\n")

    cols = 3
    for i, node in enumerate(nodes, 1):
        print(f"  [{i:>2}] {node:<25}", end="")
        if i % cols == 0:
            print()
    print("\n")

    while True:
        src_input = input("  Enter SOURCE location name: ").strip().title()
        if src_input in graph.nodes:
            break
        # Try partial match
        matches = [n for n in nodes if src_input.lower() in n.lower()]
        if len(matches) == 1:
            src_input = matches[0]
            print(f"  ✅ Auto-matched: {src_input}")
            break
        elif len(matches) > 1:
            print(f"  Multiple matches: {matches}. Be more specific.")
        else:
            print(f"  ❌ '{src_input}' not found. Try again.")

    while True:
        dst_input = input("  Enter DESTINATION location name: ").strip().title()
        if dst_input in graph.nodes:
            if dst_input == src_input:
                print("  ⚠️  Source and destination cannot be the same.")
                continue
            break
        matches = [n for n in nodes if dst_input.lower() in n.lower()]
        if len(matches) == 1:
            dst_input = matches[0]
            print(f"  ✅ Auto-matched: {dst_input}")
            break
        elif len(matches) > 1:
            print(f"  Multiple matches: {matches}. Be more specific.")
        else:
            print(f"  ❌ '{dst_input}' not found. Try again.")

    return src_input, dst_input


# ──────────────────────────────────────────────────────────────
# Main Menu
# ──────────────────────────────────────────────────────────────

def main_menu():
    """Main interactive CLI loop."""
    banner()

    while True:
        print("  +------------------------------+")
        print("  |         MAIN MENU            |")
        print("  +------------------------------+")
        print("  |  [1] Find Shortest Route     |")
        print("  |  [2] Compare All Algorithms  |")
        print("  |  [3] View City Map Graph     |")
        print("  |  [4] View Graph Info         |")
        print("  |  [5] Run Full Demo           |")
        print("  |  [6] Exit                    |")
        print("  +------------------------------+")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            action_find_route()
        elif choice == "2":
            action_compare_algorithms()
        elif choice == "3":
            action_view_graph()
        elif choice == "4":
            action_graph_info()
        elif choice == "5":
            action_full_demo()
        elif choice == "6":
            print("\n  👋 Thank you! Happy Learning.\n")
            sys.exit(0)
        else:
            print("  ⚠️  Invalid option.\n")


# ──────────────────────────────────────────────────────────────
# Actions
# ──────────────────────────────────────────────────────────────

def action_find_route():
    print("\n" + "─" * 50)
    graph, graph_name = pick_graph()
    source, destination = pick_locations(graph)
    algo, weight_type = pick_algorithm()

    print(f"\n  ⏳ Computing route...")

    if algo == "dijkstra":
        result = dijkstra(graph, source, destination, weight_type)
        label  = f"Dijkstra's (Optimized by {weight_type.title()})"
    elif algo == "bfs":
        result = bfs(graph, source, destination)
        label  = "BFS (Fewest Hops)"
    else:
        result = dfs(graph, source, destination)
        label  = "DFS (Depth-First)"

    print_route_report(result, label, source, destination)

    if result.get("found"):
        save = input("  💾 Save report? (y/n): ").strip().lower()
        if save == "y":
            save_report_to_file(result, label, source, destination)

        if VISUALIZATION_AVAILABLE:
            viz = input("  🖼️  Generate graph visualization? (y/n): ").strip().lower()
            if viz == "y":
                draw_graph(graph,
                           title=f"{label}: {source} → {destination}",
                           save_filename=f"route_{source}_{destination}.png",
                           highlight_path=result.get("path"),
                           weight_type=weight_type or "distance")

    input("\n  Press Enter to return to menu...")


def action_compare_algorithms():
    print("\n" + "─" * 50)
    graph, _ = pick_graph()
    source, destination = pick_locations(graph)

    print(f"\n  ⏳ Running all algorithms...")

    bfs_r   = bfs(graph, source, destination)
    dfs_r   = dfs(graph, source, destination)
    dijk_d  = dijkstra(graph, source, destination, "distance")
    dijk_t  = dijkstra(graph, source, destination, "time")
    dijk_c  = dijkstra(graph, source, destination, "cost")

    print_comparison_report(source, destination,
                            bfs_r, dfs_r,
                            dijk_d, dijk_t, dijk_c)

    save = input("  💾 Save comparison as JSON? (y/n): ").strip().lower()
    if save == "y":
        data = {
            "source": source, "destination": destination,
            "bfs": bfs_r, "dfs": dfs_r,
            "dijkstra_distance": dijk_d,
            "dijkstra_time": dijk_t,
            "dijkstra_cost": dijk_c
        }
        save_json_report(data, f"comparison_{source}_{destination}.json")

    input("\n  Press Enter to return to menu...")


def action_view_graph():
    print("\n" + "─" * 50)
    if not VISUALIZATION_AVAILABLE:
        print("  ⚠️  Install matplotlib & networkx: pip install matplotlib networkx")
        input("\n  Press Enter to return to menu...")
        return

    graph, graph_name = pick_graph()
    print("  ⏳ Generating graph visualization...")
    draw_graph(graph,
               title="City Road Network — All Routes",
               save_filename=f"{graph_name}_full_graph.png")
    input("\n  Press Enter to return to menu...")


def action_graph_info():
    print("\n" + "─" * 50)
    graph, _ = pick_graph()
    graph.display()
    input("\n  Press Enter to return to menu...")


def action_full_demo():
    """Runs a complete pre-configured demo with sample routes."""
    print("\n" + "═" * 65)
    print("  🎬 FULL PROJECT DEMO")
    print("═" * 65)

    # Demo 1: Small graph
    print("\n  ▶ DEMO 1: Small City Graph — Home → Hospital")
    small_g  = build_small_demo_graph()
    result_s = dijkstra(small_g, "Home", "Hospital", "distance")
    print_route_report(result_s, "Dijkstra's (Min Distance)", "Home", "Hospital")

    # Demo 2: India map - distance
    print("\n  ▶ DEMO 2: India Map — Mumbai → Delhi (Min Distance)")
    india_g  = build_india_city_graph()
    result_d = dijkstra(india_g, "Mumbai", "Delhi", "distance")
    print_route_report(result_d, "Dijkstra's (Min Distance)", "Mumbai", "Delhi")

    # Demo 3: India map - time
    print("\n  ▶ DEMO 3: India Map — Chennai → Delhi (Min Time)")
    result_t = dijkstra(india_g, "Chennai", "Delhi", "time")
    print_route_report(result_t, "Dijkstra's (Min Time)", "Chennai", "Delhi")

    # Demo 4: BFS comparison
    print("\n  ▶ DEMO 4: BFS — Mumbai → Delhi (Fewest Hops)")
    result_bfs = bfs(india_g, "Mumbai", "Delhi")
    print_route_report(result_bfs, "BFS (Fewest Hops)", "Mumbai", "Delhi")

    # Save outputs
    save_report_to_file(result_d, "Dijkstra's", "Mumbai", "Delhi")

    if VISUALIZATION_AVAILABLE:
        print("\n  🖼️  Generating visualizations...")
        draw_small_demo(small_g, result_s)
        draw_india_map(india_g, result_d, "distance")
        draw_india_map(india_g, result_t, "time")

    print("\n  ✅ Demo complete! Check outputs/ and images/ folders.")
    input("\n  Press Enter to return to menu...")
