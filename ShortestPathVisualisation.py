#explanation
# https://harrymunro.hashnode.dev/simulating-a-car-driving-across-london-in-20-lines-of-python

import osmnx as ox
import random
from matplotlib import pyplot as plt
from celluloid import Camera
import networkx as nx

from matplotlib.animation import FuncAnimation,PillowWriter

# Latitude and Longitude for a point in Cork (English Market)
latitude = 51.897845
longitude = 8.474891

# Create a graph from a point
G = ox.graph_from_point((latitude, longitude), dist=5000, dist_type='bbox', network_type='drive')

# Ensure the graph is strongly connected
G = ox.utils_graph.get_largest_component(G, strongly=True)

# shortest path between two random path
# Select two random nodes
origin, destination = random.sample(list(G.nodes), 2)

# Compute the shortest path
shortest_path = nx.shortest_path(G, origin, destination, weight='length')

#shortest path between two given nodes
#origin = (51.89799458151566, -8.475036848226916)
#destination = (51.88440002855128, -8.538946173284181)
#origin_node = ox.nearest_nodes(G,51.89799458151566, -8.475036848226916)
#destination_node = ox.nearest_nodes(G, 51.88440002855128, -8.538946173284181)
#shortest_path = nx.shortest_path(G, origin_node, destination_node)


# Visualisation
fig, ax = plt.subplots()  # Create a matplotlib figure and axes.
camera = Camera(fig)  # Prepare the camera for capturing each frame.

# Instead of plotting point by point, accumulate the points in the path for each frame.
for i in range(1, len(shortest_path) + 1):
    ox.plot_graph(G, ax=ax, show=False, close=False, node_size=0, bgcolor='k')  # Redraw the graph for each frame.
    ox.plot_graph_route(G, shortest_path[:i], route_linewidth=6, node_size=0, bgcolor='k', route_color='r', orig_dest_node_size=100, ax=ax, show=False, close=False)  # Plot the route up to the current point.
    camera.snap()  # Capture the frame.

animation = camera.animate()  # Create the animation.
animation.save('car_journey.gif', writer='imagemagick')  # Save the animation as a GIF.

