"""
=============================================================
  Intelligent Route Planner - Visualization Module
  File: src/visualizer.py
  Description: Graph visualization using NetworkX + Matplotlib.
               Draws the city map, highlights shortest path.
=============================================================
"""

try:
    import matplotlib
    matplotlib.use("Agg")          # Non-interactive backend (safe for all OS)
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import networkx as nx
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False

import os

OUTPUTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
IMAGES_DIR  = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")


def _check_libs():
    if not VISUALIZATION_AVAILABLE:
        print("\n  ⚠️  Visualization libraries not installed.")
        print("  Run: pip install matplotlib networkx")
        return False
    return True


def draw_graph(graph_obj, title: str = "City Road Network",
               save_filename: str = "city_graph.png",
               highlight_path: list = None,
               weight_type: str = "distance"):
    """
    Draw the full graph with optional highlighted shortest path.

    Args:
        graph_obj      : Graph object from src/graph.py
        title          : Title for the plot
        save_filename  : Name for saved image (in images/)
        highlight_path : List of nodes forming the shortest path
        weight_type    : 'distance' | 'time' | 'cost'
    """
    if not _check_libs():
        return

    os.makedirs(IMAGES_DIR, exist_ok=True)

    # ── Build NetworkX graph ──────────────────────────────────────────
    G = nx.Graph()

    for node in graph_obj.get_all_nodes():
        G.add_node(node)

    edge_labels = {}
    for node in graph_obj.get_all_nodes():
        for neighbor, weight in graph_obj.get_neighbors(node):
            if not G.has_edge(node, neighbor):
                G.add_edge(node, neighbor,
                           weight=weight[weight_type],
                           **weight)
                label_val = weight[weight_type]
                unit = {"distance": "km", "time": "min", "cost": "₹"}.get(weight_type, "")
                edge_labels[(node, neighbor)] = f"{label_val} {unit}"

    # ── Layout ───────────────────────────────────────────────────────
    # spring layout gives nice spreading; seed for reproducibility
    pos = nx.spring_layout(G, seed=42, k=2.5)

    # ── Figure Setup ─────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(18, 12))
    ax.set_facecolor("#0f0f1a")
    fig.patch.set_facecolor("#0f0f1a")

    # ── Determine edge colors ─────────────────────────────────────────
    path_edges = set()
    if highlight_path and len(highlight_path) > 1:
        for i in range(len(highlight_path) - 1):
            path_edges.add((highlight_path[i], highlight_path[i + 1]))
            path_edges.add((highlight_path[i + 1], highlight_path[i]))

    normal_edges = [(u, v) for u, v in G.edges() if (u, v) not in path_edges]
    short_edges  = [(u, v) for u, v in G.edges() if (u, v) in path_edges]

    # Draw normal edges
    nx.draw_networkx_edges(G, pos,
                           edgelist=normal_edges,
                           edge_color="#4a5568",
                           width=1.5,
                           alpha=0.6,
                           ax=ax)

    # Draw shortest path edges (highlighted)
    if short_edges:
        nx.draw_networkx_edges(G, pos,
                               edgelist=short_edges,
                               edge_color="#f6ad55",
                               width=4.0,
                               alpha=1.0,
                               ax=ax)

    # ── Node colors ───────────────────────────────────────────────────
    node_colors = []
    node_sizes  = []
    for node in G.nodes():
        if highlight_path:
            if node == highlight_path[0]:
                node_colors.append("#48bb78")   # Green = source
                node_sizes.append(900)
            elif node == highlight_path[-1]:
                node_colors.append("#fc8181")   # Red = destination
                node_sizes.append(900)
            elif node in highlight_path:
                node_colors.append("#f6ad55")   # Orange = on path
                node_sizes.append(700)
            else:
                node_colors.append("#4a90d9")   # Blue = other
                node_sizes.append(500)
        else:
            node_colors.append("#4a90d9")
            node_sizes.append(600)

    nx.draw_networkx_nodes(G, pos,
                           node_color=node_colors,
                           node_size=node_sizes,
                           alpha=0.95,
                           ax=ax)

    # ── Labels ────────────────────────────────────────────────────────
    nx.draw_networkx_labels(G, pos,
                            font_color="white",
                            font_size=7,
                            font_weight="bold",
                            ax=ax)

    nx.draw_networkx_edge_labels(G, pos,
                                 edge_labels=edge_labels,
                                 font_color="#e2e8f0",
                                 font_size=6,
                                 ax=ax)

    # ── Title & Legend ────────────────────────────────────────────────
    ax.set_title(title, color="white", fontsize=16, fontweight="bold", pad=20)
    ax.axis("off")

    if highlight_path:
        legend_items = [
            mpatches.Patch(color="#48bb78", label="Source"),
            mpatches.Patch(color="#fc8181", label="Destination"),
            mpatches.Patch(color="#f6ad55", label="Shortest Path"),
            mpatches.Patch(color="#4a90d9", label="Other Nodes"),
        ]
        ax.legend(handles=legend_items, loc="lower left",
                  facecolor="#1a1a2e", edgecolor="white",
                  labelcolor="white", fontsize=10)

    # ── Save ──────────────────────────────────────────────────────────
    filepath = os.path.join(IMAGES_DIR, save_filename)
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close()

    print(f"  🖼️  Graph saved  → {filepath}")
    return filepath


def draw_small_demo(graph_obj, result: dict, weight_type: str = "distance"):
    """Convenience wrapper for the small demo graph visualization."""
    path = result.get("path", []) if result.get("found") else []
    src  = path[0] if path else "Unknown"
    dst  = path[-1] if path else "Unknown"

    return draw_graph(
        graph_obj,
        title=f"Small City Graph — Shortest Path: {src} → {dst}",
        save_filename="demo_graph_shortest_path.png",
        highlight_path=path,
        weight_type=weight_type
    )


def draw_india_map(graph_obj, result: dict, weight_type: str = "distance"):
    """Convenience wrapper for the India city map visualization."""
    path = result.get("path", []) if result.get("found") else []
    src  = path[0] if path else "Unknown"
    dst  = path[-1] if path else "Unknown"
    opt  = weight_type.title()

    return draw_graph(
        graph_obj,
        title=f"India City Road Network — Shortest Path ({opt}): {src} → {dst}",
        save_filename=f"india_map_{src}_to_{dst}_{weight_type}.png",
        highlight_path=path,
        weight_type=weight_type
    )
