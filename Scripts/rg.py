import networkx as nx
import random

def randomized_greedy_clustering(graph, num_iterations):
    best_clusters = None
    best_modularity = float("-inf")

    for _ in range(num_iterations):
        # Initialize each node as its own cluster
        clusters = list(graph.nodes())
        random.shuffle(clusters)

        # Function to calculate modularity for a given clustering
        def calculate_modularity(clusters, graph):
            modularity = 0
            m = graph.number_of_edges()
            for cluster in clusters:
                subgraph = graph.subgraph(cluster)
                l_c = subgraph.number_of_edges()
                d_c = sum(dict(subgraph.degree()).values())
                modularity += (l_c / (2 * m)) - ((d_c / (2 * m)) ** 2)
            return modularity

        # Main loop: merge nodes to maximize modularity
        while True:
            max_delta_modularity = 0
            for i in range(len(clusters)):
                for j in range(i + 1, len(clusters)):
                    merged_clusters = clusters[:i] + [clusters[i] + clusters[j]] + clusters[i + 1:j] + clusters[j + 1:]
                    delta_modularity = calculate_modularity(merged_clusters, graph) - calculate_modularity(clusters, graph)
                    if delta_modularity > max_delta_modularity:
                        max_delta_modularity = delta_modularity
                        best_clusters = merged_clusters[:]
            if max_delta_modularity <= 0:
                break
            clusters = best_clusters

        # Update best clustering if better modularity is found
        modularity = calculate_modularity(clusters, graph)
        if modularity > best_modularity:
            best_modularity = modularity
            best_clusters = clusters

    return best_clusters

# Example usage:
G = nx.karate_club_graph()
num_iterations = 10  # You can adjust the number of iterations as needed
clusters = randomized_greedy_clustering(G, num_iterations)
print(clusters)

