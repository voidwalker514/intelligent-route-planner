"""
=============================================================
  Intelligent Route Planner - Report Generator
  File: src/report.py
  Description: Formats and prints beautiful route reports.
               Saves reports to outputs/ folder.
=============================================================
"""

import os
import json
from datetime import datetime


OUTPUTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")


def _ensure_outputs_dir():
    os.makedirs(OUTPUTS_DIR, exist_ok=True)


def format_path_arrow(path: list) -> str:
    """Format path as:  A  →  B  →  C"""
    return "  →  ".join(path)


def format_time(minutes: float) -> str:
    """Convert minutes to human-readable format: Xh Ym"""
    h = int(minutes // 60)
    m = int(minutes % 60)
    if h > 0:
        return f"{h}h {m}m"
    return f"{m}m"


def print_route_report(result: dict, algorithm: str,
                       source: str, destination: str):
    """
    Print a formatted route report to terminal.

    Args:
        result      : dict returned by algorithm (dijkstra / bfs / dfs)
        algorithm   : Name string e.g. "Dijkstra's", "BFS", "DFS"
        source      : Source location name
        destination : Destination location name
    """
    width = 65
    sep   = "═" * width

    print(f"\n{sep}")
    print(f"  🗺️   INTELLIGENT ROUTE PLANNER  —  ROUTE REPORT")
    print(f"{sep}")
    print(f"  Algorithm   : {algorithm}")
    print(f"  Source      : 📍 {source}")
    print(f"  Destination : 🏁 {destination}")
    print(f"  Timestamp   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'─' * width}")

    if not result.get("found"):
        error = result.get("error", "Route not found.")
        print(f"\n  ❌ ERROR: {error}")
        print(f"\n{sep}\n")
        return

    path = result.get("path", [])

    print(f"\n  ✅ ROUTE FOUND ({len(path) - 1} stop{'s' if len(path)-1 != 1 else ''})\n")
    print(f"  📌 Route Sequence:")
    print(f"     {format_path_arrow(path)}")
    print(f"\n{'─' * width}")

    # Dijkstra has full metrics
    if "total_distance" in result:
        opt_by = result.get("optimized_by", "distance").upper()
        print(f"\n  📊 ROUTE METRICS  (Optimized by: {opt_by})\n")
        print(f"  {'Metric':<22} {'Value':<25}")
        print(f"  {'──────':<22} {'─────':<25}")
        print(f"  {'Total Distance':<22} {result['total_distance']} km")
        print(f"  {'Total Travel Time':<22} {format_time(result['total_time'])}"
              f"  ({result['total_time']} min)")
        print(f"  {'Total Cost':<22} ₹{result['total_cost']}")
        print(f"  {'Total Stops':<22} {len(path)} locations")
        print(f"  {'Hops (Edges)':<22} {len(path) - 1}")

    # BFS / DFS have hop info
    elif "hops" in result:
        print(f"\n  📊 ROUTE METRICS\n")
        print(f"  {'Total Stops':<22} {len(path)} locations")
        print(f"  {'Hops (Edges)':<22} {result['hops']}")
        print(f"\n  ℹ️  Note: {algorithm} finds fewest hops, NOT shortest distance.")
        print(f"  ℹ️  Use Dijkstra's for optimized distance/time/cost.")

    print(f"\n{'═' * width}\n")


def print_comparison_report(source: str, destination: str,
                             bfs_result: dict, dfs_result: dict,
                             dijkstra_dist: dict, dijkstra_time: dict,
                             dijkstra_cost: dict):
    """
    Print a side-by-side comparison of all algorithm results.
    Helps demonstrate WHY Dijkstra is better for route optimization.
    """
    width = 70
    sep   = "═" * width

    print(f"\n{sep}")
    print(f"  📊  ALGORITHM COMPARISON REPORT")
    print(f"  📍 {source}  →  🏁 {destination}")
    print(f"{sep}")

    algorithms = [
        ("BFS (Fewest Hops)",         bfs_result),
        ("DFS (Depth-First)",          dfs_result),
        ("Dijkstra (Min Distance)",    dijkstra_dist),
        ("Dijkstra (Min Time)",        dijkstra_time),
        ("Dijkstra (Min Cost)",        dijkstra_cost),
    ]

    for name, res in algorithms:
        if not res.get("found"):
            print(f"\n  🔴 {name:<30} NOT FOUND")
            continue

        path = res.get("path", [])
        hops = len(path) - 1
        print(f"\n  🔵 {name}")
        print(f"     Path   : {format_path_arrow(path)}")
        print(f"     Hops   : {hops}")

        if "total_distance" in res:
            print(f"     Dist   : {res['total_distance']} km")
            print(f"     Time   : {format_time(res['total_time'])}")
            print(f"     Cost   : ₹{res['total_cost']}")

    print(f"\n{sep}\n")


def save_report_to_file(result: dict, algorithm: str,
                        source: str, destination: str):
    """
    Save route report as a text file in outputs/ folder.

    Returns:
        str: path to saved file
    """
    _ensure_outputs_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"route_{source.lower().replace(' ', '_')}_to_" \
                f"{destination.lower().replace(' ', '_')}_{timestamp}.txt"
    filepath  = os.path.join(OUTPUTS_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=" * 65 + "\n")
        f.write("  INTELLIGENT ROUTE PLANNER - ROUTE REPORT\n")
        f.write("=" * 65 + "\n")
        f.write(f"  Algorithm   : {algorithm}\n")
        f.write(f"  Source      : {source}\n")
        f.write(f"  Destination : {destination}\n")
        f.write(f"  Timestamp   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 65 + "\n\n")

        if result.get("found"):
            path = result["path"]
            f.write(f"  Route Sequence:\n")
            f.write(f"  {format_path_arrow(path)}\n\n")

            if "total_distance" in result:
                f.write(f"  Total Distance : {result['total_distance']} km\n")
                f.write(f"  Total Time     : {format_time(result['total_time'])}"
                        f" ({result['total_time']} min)\n")
                f.write(f"  Total Cost     : INR {result['total_cost']}\n")
                f.write(f"  Optimized By   : {result.get('optimized_by', 'distance')}\n")
            if "hops" in result:
                f.write(f"  Total Hops     : {result['hops']}\n")
        else:
            f.write(f"  ERROR: {result.get('error', 'Route not found.')}\n")

        f.write("\n" + "=" * 65 + "\n")

    print(f"  💾 Report saved → {filepath}")
    return filepath


def save_json_report(data: dict, filename: str):
    """Save a JSON report to the outputs/ folder."""
    _ensure_outputs_dir()
    filepath = os.path.join(OUTPUTS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  💾 JSON saved  → {filepath}")
    return filepath
