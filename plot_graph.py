import networkx as nx
import matplotlib.pyplot as plt
import make_adj_list
def plot_graph_from_adj(adj, directed=True):
    # adj: list of lists
    # node i has edges to all nodes in adj[i]
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    n = len(adj)
    G.add_nodes_from(range(n))

    for i in range(n):
        for j in adj[i]:
            G.add_edge(i, j)

    # choose a layout (spring_layout looks nice usually)
    pos = nx.spring_layout(G)

    plt.figure(figsize=(6, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=500,
        font_size=10,
        arrows=directed,
    )
    plt.title("Graph")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # tiny example
    adj = make_adj_list.process_graph(r"C:\Users\User\Longest-Path-2\graphs_adjlist_sparse.txt", 30)

    plot_graph_from_adj(adj, directed=True)
