import networkx as nx

def plain_greedy_clustering(graph):
    # Initialize each node as its own cluster
    clusters = list(graph.nodes())

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
        best_clusters = clusters[:]
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

    return clusters

# Example usage:
G = nx.karate_club_graph()
clusters = plain_greedy_clustering(G)
print(clusters)

