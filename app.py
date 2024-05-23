# app.py
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image

# Define the city map as a graph
city_map = nx.Graph()
# Add locations (vertices)
locations = {
    'Chennai': (0, 0),
    'Coimbatore': (1, 2),
    'Madurai': (3, 1),
    'Tiruchirappalli': (4, 3),
    'Salem': (2, 4),
    'Tirunelveli': (5, 0),
    'Vellore': (6, 2),
    'Erode': (7, 3),
    'Thoothukudi': (8, 1)
}

for location, pos in locations.items():
    city_map.add_node(location, pos=pos)

# Add roads (edges) and assign weights (distances)
roads = [('Chennai', 'Coimbatore', 3), ('Chennai', 'Madurai', 5),
         ('Coimbatore', 'Madurai', 2), ('Coimbatore', 'Tiruchirappalli', 7),
         ('Coimbatore', 'Salem', 6), ('Madurai', 'Salem', 4),
         ('Salem', 'Tirunelveli', 2), ('Salem', 'Tiruchirappalli', 3),
         ('Tiruchirappalli', 'Vellore', 2), ('Vellore', 'Thoothukudi', 4),
         ('Salem', 'Vellore', 4), ('Tirunelveli', 'Vellore', 6),
         ('Tirunelveli', 'Erode', 5), ('Vellore', 'Erode', 3),
         ('Erode', 'Thoothukudi', 4)]

for road in roads:
    # Assuming Salem to Tirunelveli is a one-way street
    if road[0] == 'Salem' and road[1] == 'Tirunelveli':
        city_map.add_edge(road[0], road[1], weight=road[2] * 2)  # Increase weight for one-way streets
    else:
        city_map.add_edge(road[0], road[1], weight=road[2])

# Function to find shortest path and distances
def find_shortest_path(city_map, source, destination):
    shortest_path = nx.shortest_path(city_map, source=source, target=destination, weight='weight')
    shortest_distance = nx.shortest_path_length(city_map, source=source, target=destination, weight='weight')
    return shortest_path, shortest_distance

# Function to create GIF of shortest path progression
def create_gif(city_map, pos, shortest_path):
    if not shortest_path:
        return None

    gif_images = []

    # Create images for each step of the shortest path
    for i in range(len(shortest_path) - 1):
        plt.figure(figsize=(8, 6))
        nx.draw(city_map, pos, with_labels=True, node_size=700, node_color='skyblue')
        edge_labels = nx.get_edge_attributes(city_map, 'weight')
        nx.draw_networkx_edge_labels(city_map, pos, edge_labels=edge_labels)

        # Highlight the edges of the shortest path
        nx.draw_networkx_edges(city_map, pos, edgelist=[(shortest_path[i], shortest_path[i + 1])], edge_color='red', width=2)

        plt.title(f'Shortest Path Progression ({shortest_path[i]} -> {shortest_path[i + 1]})')

        # Save image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as f:
            plt.savefig(f.name)
            gif_images.append(Image.open(f.name))
        plt.close()

    # Create GIF from images
    gif_path = tempfile.NamedTemporaryFile(delete=False, suffix='.gif').name
    gif_images[0].save(gif_path, save_all=True, append_images=gif_images[1:], loop=0, duration=1000)

    return gif_path

# Streamlit dashboard
def main():
    st.title("City Map Navigation")

    # Get user input for source and destination
    source = st.selectbox("Select source location:", list(locations.keys()))
    destination = st.selectbox("Select destination location:", list(locations.keys()))

    if source == destination:
        st.write("Source and destination are same.")
        return

    # Find shortest path and distances
    shortest_path, shortest_distance = find_shortest_path(city_map, source, destination)

    # Plot city map
    plt.figure(figsize=(8, 6))
    pos = nx.get_node_attributes(city_map, 'pos')
    nx.draw(city_map, pos, with_labels=True, node_size=700, node_color='skyblue')
    edge_labels = nx.get_edge_attributes(city_map, 'weight')
    nx.draw_networkx_edge_labels(city_map, pos, edge_labels=edge_labels)

    # Save plot as a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as f:
        plt.title('City Map')
        plt.savefig(f.name)

    # Display plot in Streamlit
    #st.image(f.name)

    # Create GIF of shortest path progression
    gif_path = create_gif(city_map, pos, shortest_path)

    # Display shortest path and distance
    st.write(f"Shortest path from {source} to {destination}: {' -> '.join(shortest_path)}")
    st.write(f"Shortest distance: {shortest_distance}")

    # Display GIF of shortest path progression
    if gif_path:
        st.image(gif_path)

if __name__ == '__main__':
    main()
