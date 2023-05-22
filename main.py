import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
import random


def draw_augmenting_path(G, match, path, pos):
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edges(G, pos, edgelist=match.items(), edge_color='blue')
    nx.draw_networkx_edges(G, pos, edgelist=path, edge_color='red')
    plt.show(block=False)  # block=False to update the plot
    plt.pause(4)  # pause to allow update
    plt.clf()  # clear plot for next draw


def find_augmenting_path(G, match, visited, u):
    for v in G.neighbors(u):
        if v not in visited:
            visited.add(v)
            if v not in match or find_augmenting_path(G, match, visited, match[v]):
                match[u] = v
                match[v] = u
                return [(u, v)]
    return []


def hungarian_method(G):
    match = {}
    pos = bipartite_layout(G)
    for u in G.nodes:
        if u not in match:
            visited = set()
            path = find_augmenting_path(G, match, visited, u)
            draw_augmenting_path(G, match, path, pos)

    return match


def bipartite_layout(G): # This code places the nodes on the screen
    l, r = nx.bipartite.sets(G)
    pos = {}

    # update position for node from each group
    for index, node in enumerate(l):
        pos[node] = (-1, index / len(l))  # nodes from the left set will be on the left (-1)
    for index, node in enumerate(r):
        pos[node] = (1, index / len(r))  # nodes from the right set will be on the right (1)
    return pos


def generate_random_bipartite_graph():
    G = nx.Graph()

    # Generate random number of nodes in each partition
    left_nodes = [i for i in range(1, random.randint(5, 10))]
    right_nodes = [chr(97 + i) for i in range(random.randint(5, 10))]

    # Generate random edges
    edges = [(random.choice(left_nodes), random.choice(right_nodes)) for _ in range(random.randint(5, 20))]

    G.add_edges_from(edges) # Adds the edges between the nodes in the graph
    return G


def largest_connected_component(G):
    largest_cc = max(nx.connected_components(G), key=len)
    return G.subgraph(largest_cc).copy()


G = generate_random_bipartite_graph()
G = largest_connected_component(G)
match = hungarian_method(G)
print(match)
