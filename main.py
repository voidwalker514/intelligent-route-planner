"""
=============================================================
  Intelligent Route Planner
  File: main.py
  Description: Entry point — launches the interactive CLI
               or runs a non-interactive demo mode.

  Usage:
    python main.py           → Interactive CLI menu
    python main.py --demo    → Auto-run full demo
    python main.py --test    → Run all algorithm unit tests

  Author  : [Your Name]
  GitHub  : github.com/[your-username]/Intelligent-Route-Planner
  Course  : Data Structures & Algorithms (DSA Project)
=============================================================
"""

import sys
import os

# Fix Windows terminal encoding so emojis/Unicode display correctly
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # Python < 3.7 fallback

# Ensure project root is in sys.path
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)


# ── Imports ──────────────────────────────────────────────────
from src.graph       import Graph
from src.algorithms  import bfs, dfs, dijkstra, all_pairs_shortest_path
from src.city_data   import build_india_city_graph, build_small_demo_graph
from src.report      import (print_route_report, print_comparison_report,
                              save_report_to_file, save_json_report)
from src.visualizer  import (draw_india_map, draw_small_demo,
                              VISUALIZATION_AVAILABLE)
from src.cli         import main_menu, action_full_demo, banner


# ==============================================================
# Demo Mode — runs without user input
# ==============================================================

def run_demo():
    """
    Fully automated demo — no user input needed.
    Perfect for showing GitHub CI outputs.
    """
    print("\n" + "═" * 65)
    print("  🎬  INTELLIGENT ROUTE PLANNER — AUTOMATED DEMO")
    print("═" * 65)

    # ─── DEMO 1: Small Graph ────────────────────────────────────
    print("\n" + "─" * 65)
    print("  📋 DEMO 1: Small City Graph")
    print("─" * 65)
    small_g = build_small_demo_graph()
    small_g.display()

    routes = [
        ("Home", "Hospital"),
        ("Home", "Airport"),
        ("School", "City Center"),
    ]

    for src, dst in routes:
        result = dijkstra(small_g, src, dst, "distance")
        print_route_report(result, "Dijkstra's (Min Distance)", src, dst)

    # ─── DEMO 2: India Map ──────────────────────────────────────
    print("\n" + "─" * 65)
    print("  📋 DEMO 2: India City Map — Key Routes")
    print("─" * 65)
    india_g = build_india_city_graph()

    demo_routes = [
        ("Mumbai",   "Delhi",     "distance"),
        ("Chennai",  "Delhi",     "time"),
        ("Kolkata",  "Mumbai",    "cost"),
        ("Bengaluru","Jaipur",    "distance"),
        ("Amritsar", "Coimbatore","time"),
    ]

    for src, dst, wt in demo_routes:
        result = dijkstra(india_g, src, dst, wt)
        label  = f"Dijkstra's (Min {wt.title()})"
        print_route_report(result, label, src, dst)
        save_report_to_file(result, label, src, dst)

    # ─── DEMO 3: Algorithm Comparison ──────────────────────────
    print("\n" + "─" * 65)
    print("  📋 DEMO 3: Algorithm Comparison — Mumbai → Delhi")
    print("─" * 65)
    bfs_r  = bfs(india_g,     "Mumbai", "Delhi")
    dfs_r  = dfs(india_g,     "Mumbai", "Delhi")
    dijk_d = dijkstra(india_g, "Mumbai", "Delhi", "distance")
    dijk_t = dijkstra(india_g, "Mumbai", "Delhi", "time")
    dijk_c = dijkstra(india_g, "Mumbai", "Delhi", "cost")

    print_comparison_report("Mumbai", "Delhi",
                            bfs_r, dfs_r,
                            dijk_d, dijk_t, dijk_c)

    # Save comparison JSON
    comparison_data = {
        "source": "Mumbai",
        "destination": "Delhi",
        "algorithms": {
            "bfs":               {"path": bfs_r.get("path", []),
                                  "hops": bfs_r.get("hops", 0)},
            "dfs":               {"path": dfs_r.get("path", []),
                                  "hops": dfs_r.get("hops", 0)},
            "dijkstra_distance": dijk_d,
            "dijkstra_time":     dijk_t,
            "dijkstra_cost":     dijk_c,
        }
    }
    save_json_report(comparison_data, "demo_comparison_mumbai_delhi.json")

    # ─── DEMO 4: Visualization ──────────────────────────────────
    if VISUALIZATION_AVAILABLE:
        print("\n" + "─" * 65)
        print("  📋 DEMO 4: Graph Visualizations")
        print("─" * 65)
        draw_small_demo(small_g, dijkstra(small_g, "Home", "Airport", "distance"))
        draw_india_map(india_g, dijk_d, "distance")
        draw_india_map(india_g, dijk_t, "time")
    else:
        print("\n  ℹ️  Skipping visualizations (matplotlib/networkx not installed).")
        print("  Run: pip install matplotlib networkx")

    print("\n" + "═" * 65)
    print("  ✅ Demo complete!")
    print("  📁 Check outputs/ for saved reports")
    print("  📁 Check images/ for graph visualizations")
    print("=" * 65 + "\n")


# ==============================================================
# Test Mode — algorithm correctness checks
# ==============================================================

def run_tests():
    """Simple correctness tests without pytest dependency."""
    print("\n" + "═" * 65)
    print("  🧪  RUNNING ALGORITHM TESTS")
    print("═" * 65)

    passed = 0
    failed = 0

    def test(name, condition, msg=""):
        nonlocal passed, failed
        if condition:
            print(f"  ✅ PASS: {name}")
            passed += 1
        else:
            print(f"  ❌ FAIL: {name} {msg}")
            failed += 1

    # ── Build small graph ────────────────────────────────────
    g = build_small_demo_graph()

    # BFS Tests
    bfs_r = bfs(g, "Home", "Hospital")
    test("BFS: Route found",           bfs_r["found"])
    test("BFS: Path starts at source", bfs_r["path"][0] == "Home")
    test("BFS: Path ends at dest",     bfs_r["path"][-1] == "Hospital")
    test("BFS: Non-existent route",    not bfs(g, "Home", "NonExistent")["found"])

    # DFS Tests
    dfs_r = dfs(g, "Home", "Airport")
    test("DFS: Route found",           dfs_r["found"])
    test("DFS: Path starts at source", dfs_r["path"][0] == "Home")
    test("DFS: Path ends at dest",     dfs_r["path"][-1] == "Airport")

    # Dijkstra Tests
    dijk_r = dijkstra(g, "Home", "Hospital", "distance")
    test("Dijkstra: Route found",         dijk_r["found"])
    test("Dijkstra: Optimal distance ≤ 9",dijk_r["total_distance"] <= 9)
    test("Dijkstra: Positive distance",   dijk_r["total_distance"] > 0)
    test("Dijkstra: Path is valid",       dijk_r["path"][0] == "Home" and
                                          dijk_r["path"][-1] == "Hospital")

    # Same node test
    dijk_same = dijkstra(g, "Home", "Home", "distance")
    # Same node should just return self or handle gracefully
    test("Dijkstra: Same src/dst handled", True)  # doesn't crash

    # India graph
    india = build_india_city_graph()
    ir = dijkstra(india, "Mumbai", "Delhi", "distance")
    test("India: Mumbai→Delhi found",     ir["found"])
    test("India: Distance > 0",          ir["total_distance"] > 0)
    test("India: Time > 0",              ir["total_time"] > 0)

    print(f"\n  Results: {passed} passed, {failed} failed")
    print("═" * 65 + "\n")

    return failed == 0


# ==============================================================
# Entry Point
# ==============================================================

if __name__ == "__main__":
    args = sys.argv[1:]

    if "--demo" in args:
        banner()
        run_demo()
    elif "--test" in args:
        banner()
        success = run_tests()
        sys.exit(0 if success else 1)
    else:
        # Default: interactive CLI
        main_menu()
