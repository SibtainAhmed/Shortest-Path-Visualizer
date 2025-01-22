import heapq
import networkx as nx
import matplotlib.pyplot as plt

def dijkstra_shortest_path(graph, start, end):
    """Find the shortest path between start and end using Dijkstra's algorithm."""
    queue = []
    heapq.heappush(queue, (0, start))
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
    shortest_path = []
    current = end
    while current is not None:
        shortest_path.append(current)
        current = previous_nodes[current]
    shortest_path.reverse()

    return shortest_path, distances[end]

def visualize_graph(graph, shortest_path=None):
    """Visualize the graph with optional highlighting of the shortest path."""
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    if shortest_path:
        edges_in_path = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color='red', width=2)
    plt.show()

def add_place(graph):
    """Add a new place to the graph."""
    new_place = input("Enter the name of the new place: ").strip()
    if new_place in graph:
        print(f"{new_place} already exists in the graph.")
        return
    graph[new_place] = {}
    while True:
        neighbor = input(f"Enter a place connected to {new_place} (or 'done' to finish): ").strip()
        if neighbor.lower() == 'done':
            break
        if neighbor not in graph:
            print(f"{neighbor} does not exist in the graph.")
            continue
        try:
            distance = float(input(f"Enter the distance from {new_place} to {neighbor}: ").strip())
            graph[new_place][neighbor] = distance
            graph[neighbor][new_place] = distance
        except ValueError:
            print("Invalid distance. Please enter a numeric value.")

def remove_place(graph):
    """Remove a place and its associated routes from the graph."""
    place = select_place(graph, "Enter the number of the place to remove")
    if not place:
        return
    graph.pop(place)
    for neighbors in graph.values():
        neighbors.pop(place, None)
    print(f"{place} and its routes have been removed.")

def remove_route(graph):
    """Remove a route between two places."""
    place1 = select_place(graph, "Enter the number of the first place")
    place2 = select_place(graph, "Enter the number of the second place")
    if not place1 or not place2:
        return
    if place2 in graph[place1]:
        del graph[place1][place2]
        del graph[place2][place1]
        print(f"Route between {place1} and {place2} has been removed.")
    else:
        print(f"No route exists between {place1} and {place2}.")

def add_route(graph):
    """Add or update a route between two places."""
    place1 = select_place(graph, "Enter the number of the first place")
    place2 = select_place(graph, "Enter the number of the second place")
    if not place1 or not place2:
        return
    try:
        distance = float(input(f"Enter the distance between {place1} and {place2}: ").strip())
        graph[place1][place2] = distance
        graph[place2][place1] = distance
        print(f"Route between {place1} and {place2} has been added/updated.")
    except ValueError:
        print("Invalid distance. Please enter a numeric value.")

def list_places(graph):
    """List all places with serial numbers."""
    for idx, place in enumerate(graph, 1):
        print(f"{idx}. {place}")

def select_place(graph, prompt):
    """Prompt the user to select a place by number."""
    print("\nAvailable places:")
    list_places(graph)
    try:
        choice = int(input(f"{prompt}: ").strip())
        if 1 <= choice <= len(graph):
            return list(graph.keys())[choice - 1]
        else:
            print("Invalid choice. Please select a valid number.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def main():
    graph = {"Jauhar": {"Gulshan": 5, "Malir": 7},
        "Gulshan": {"Jauhar": 5, "Korangi": 10, "Malir": 3},
        "Korangi": {"Gulshan": 10, "Malir": 4},
        "Malir": {"Jauhar": 7, "Gulshan": 3, "Korangi": 4, "Saddar": 8},
        "Saddar": {"Malir": 8, "Clifton": 6},
        "Clifton": {"Saddar": 6, "Defence": 4},
        "Defence": {"Clifton": 4}}
    while True:
        print("\nMenu:")
        print("1. Find shortest path")
        print("2. Add a new place")
        print("3. Remove a place")
        print("4. Add or update a route")
        print("5. Remove a route")
        print("6. Visualize graph")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            start = select_place(graph, "Enter the number of the starting place")
            end = select_place(graph, "Enter the number of the destination place")
            if not start or not end:
                continue
            path, total_distance = dijkstra_shortest_path(graph, start, end)
            if total_distance == float('inf'):
                print(f"No path exists between {start} and {end}.")
            else:
                print(f"Shortest path: {' -> '.join(path)}")
                print(f"Total distance: {total_distance} km")
                visualize_graph(graph, shortest_path=path)
        elif choice == '2':
            add_place(graph)
        elif choice == '3':
            remove_place(graph)
        elif choice == '4':
            add_route(graph)
        elif choice == '5':
            remove_route(graph)
        elif choice == '6':
            visualize_graph(graph)
        elif choice == '7':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main()