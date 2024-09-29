import heapq

# Function to calculate shortest paths using Dijkstra's algorithm
def dijkstra(graph, start):
    num_nodes = len(graph)
    distances = {i: float('inf') for i in range(num_nodes)}
    distances[start] = 0
    pq = [(0, start)]  # Priority queue initialized with the start node

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

# Input number of nodes and edges from the user
num_nodes = int(input("Enter number of routers (nodes): "))
graph = {i: {} for i in range(num_nodes)}

num_edges = int(input("Enter number of connections (edges): "))
for _ in range(num_edges):
    u, v, w = map(int, input(f"Enter connection (node1 node2 weight): ").split())
    graph[u][v] = graph[v][u] = w

# Perform Dijkstra's algorithm from a source node
source_node = int(input("Enter the source node: "))
distances = dijkstra(graph, source_node)

# Output the shortest distance to each node
for node, distance in distances.items():
    print(f"Shortest distance from {source_node} to node {node}: {distance}")
