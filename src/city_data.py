"""
=============================================================
  Intelligent Route Planner - City Data Module
  File: src/city_data.py
  Description: Pre-built Indian city map with real distances,
               travel times, and road costs.
               Builds and returns the Graph object.
=============================================================
"""

from src.graph import Graph


def build_india_city_graph() -> Graph:
    """
    Build a realistic weighted graph of major Indian cities.

    Nodes  : 20 major cities/locations
    Edges  : Roads with distance (km), time (min), cost (INR)

    Returns:
        Graph object ready for algorithm use
    """
    g = Graph(directed=False)

    # ------------------------------------------------------------------
    # Format: g.add_edge(city_a, city_b, distance_km, time_min, cost_inr)
    # ------------------------------------------------------------------

    # ── DELHI CLUSTER ──────────────────────────────────────────────────
    g.add_edge("Delhi",       "Agra",         200,  180, 350)
    g.add_edge("Delhi",       "Jaipur",       280,  300, 420)
    g.add_edge("Delhi",       "Chandigarh",   250,  270, 380)
    g.add_edge("Delhi",       "Lucknow",      550,  480, 700)
    g.add_edge("Delhi",       "Amritsar",     450,  420, 600)

    # ── AGRA CLUSTER ───────────────────────────────────────────────────
    g.add_edge("Agra",        "Jaipur",       235,  240, 360)
    g.add_edge("Agra",        "Lucknow",      360,  300, 500)
    g.add_edge("Agra",        "Gwalior",      120,  110, 200)

    # ── RAJASTHAN CLUSTER ──────────────────────────────────────────────
    g.add_edge("Jaipur",      "Jodhpur",      340,  330, 490)
    g.add_edge("Jaipur",      "Udaipur",      395,  370, 560)
    g.add_edge("Jaipur",      "Ahmedabad",    660,  600, 850)
    g.add_edge("Jodhpur",     "Udaipur",      250,  240, 380)

    # ── GUJARAT CLUSTER ────────────────────────────────────────────────
    g.add_edge("Ahmedabad",   "Surat",        265,  240, 380)
    g.add_edge("Ahmedabad",   "Mumbai",       530,  480, 720)
    g.add_edge("Surat",       "Mumbai",       280,  250, 400)
    g.add_edge("Surat",       "Pune",         340,  310, 480)

    # ── MAHARASHTRA CLUSTER ────────────────────────────────────────────
    g.add_edge("Mumbai",      "Pune",         150,  150, 250)
    g.add_edge("Mumbai",      "Nashik",       170,  180, 280)
    g.add_edge("Pune",        "Nashik",       210,  200, 300)
    g.add_edge("Pune",        "Hyderabad",    560,  520, 750)
    g.add_edge("Pune",        "Goa",          450,  420, 630)
    g.add_edge("Nashik",      "Aurangabad",   170,  160, 250)
    g.add_edge("Aurangabad",  "Hyderabad",    490,  460, 660)

    # ── SOUTH CLUSTER ──────────────────────────────────────────────────
    g.add_edge("Hyderabad",   "Bengaluru",    570,  540, 780)
    g.add_edge("Hyderabad",   "Chennai",      625,  580, 840)
    g.add_edge("Bengaluru",   "Chennai",      345,  320, 480)
    g.add_edge("Bengaluru",   "Mysuru",       145,  130, 220)
    g.add_edge("Bengaluru",   "Goa",          560,  510, 760)
    g.add_edge("Chennai",     "Coimbatore",   490,  450, 650)
    g.add_edge("Chennai",     "Madurai",      460,  430, 640)
    g.add_edge("Coimbatore",  "Madurai",      210,  200, 320)
    g.add_edge("Coimbatore",  "Mysuru",       200,  190, 300)

    # ── EAST CLUSTER ───────────────────────────────────────────────────
    g.add_edge("Lucknow",     "Kanpur",        80,   70, 120)
    g.add_edge("Lucknow",     "Varanasi",     330,  300, 440)
    g.add_edge("Varanasi",    "Kolkata",      700,  650, 920)
    g.add_edge("Kolkata",     "Bhubaneswar",  440,  420, 620)
    g.add_edge("Bhubaneswar", "Hyderabad",    920,  870, 1200)
    g.add_edge("Kolkata",     "Patna",        575,  540, 760)
    g.add_edge("Patna",       "Varanasi",     295,  270, 400)
    g.add_edge("Patna",       "Lucknow",      530,  490, 700)

    # ── NORTH CLUSTER ──────────────────────────────────────────────────
    g.add_edge("Chandigarh",  "Amritsar",     230,  220, 340)
    g.add_edge("Amritsar",    "Jammu",        200,  210, 320)
    g.add_edge("Gwalior",     "Lucknow",      430,  400, 580)

    return g


def build_small_demo_graph() -> Graph:
    """
    A small 8-node demo graph for beginner-friendly testing.
    Models a simple city with locations like Market, Hospital, etc.
    """
    g = Graph(directed=False)

    # Small city layout
    g.add_edge("Home",        "Market",       5,    10, 15)
    g.add_edge("Home",        "School",       3,     6, 10)
    g.add_edge("Market",      "Hospital",     4,     8, 12)
    g.add_edge("Market",      "Park",         2,     5,  8)
    g.add_edge("School",      "Library",      2,     4,  6)
    g.add_edge("Library",     "Park",         3,     6, 10)
    g.add_edge("Park",        "Hospital",     6,    12, 18)
    g.add_edge("Hospital",    "Airport",      10,   20, 30)
    g.add_edge("Airport",     "City Center",  15,   25, 40)
    g.add_edge("Park",        "City Center",  8,    15, 22)
    g.add_edge("Home",        "City Center",  20,   35, 55)

    return g
