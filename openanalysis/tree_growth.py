import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

__all__ = ['apply_to_graph', 'tree_growth_visualizer']


def tree_growth_visualizer(fun):
    """
    Visualizer function for Graph algorithms iterating the edges of graph forming a Tree
    Visualizes given function by inputting a Random Geometric Graph as an input

    :param fun: A function which has the signature f(G) and returns iterator of edges of graph G
    :return: Saves the animation of tree growth in output/ directory
    """
    G = nx.random_geometric_graph(100, .125)
    # position is stored as node attribute data for random_geometric_graph
    pos = nx.get_node_attributes(G, 'pos')
    # find node near center (0.5,0.5)
    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) ** 2
        if d < dmin:
            ncenter = n
            dmin = d
    for u, v in G.edges():
        G.edge[u][v]['weight'] = ((G.node[v]['pos'][0] - G.node[u]['pos'][0]) ** 2 +
                                  (G.node[v]['pos'][1] - G.node[u]['pos'][1]) ** 2) ** .5
    plt.figure(figsize=(8, 8))
    plt.title(fun.__name__ + " algorithm visualization")
    nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.axis('off')
    edge_list = []
    # Create folder to save visualization
    import errno
    import os
    path = "output"
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    i = 0
    for i, edge in enumerate(fun(G)):
        plt.clf()
        plt.title(fun.__name__ + " algorithm visualization")
        nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
        T = nx.Graph(edge_list)
        nx.draw_networkx_edges(T, pos, nodelist=[ncenter], edge_color="r")
        nx.draw_networkx_nodes(T, pos, node_color='g', alpha=0.5, node_size=100)
        plt.axis('off')
        plt.savefig("output/fig%04d.png" % i)
        print(i)
        edge_list += [edge]
    plt.clf()
    plt.title(fun.__name__ + " algorithm visualization")
    nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
    T = nx.Graph(edge_list)
    nx.draw_networkx_edges(T, pos, nodelist=[ncenter], edge_color="r")
    nx.draw_networkx_nodes(T, pos, node_color='g', alpha=0.5, node_size=100)
    plt.axis('off')
    plt.savefig(os.path.join("output", 'fig%04d.png' % i))
    # Now call ffmpeg to convert images to video
    # Check for POSIX OS
    if os.name == 'posix':
        os.system(
            'ffmpeg -y -r 2 -i output/fig%04d.png \
            -c:v libx264 -vf "format=yuv420p" \
            output/{0}.mp4'.format(fun.__name__)
        )
    # Check for Windows OS
    elif os.name == 'nt':
        os.system(
            'ffmpeg -y -r 2 -i output\fig%%04d.png ^
            -c:v libx264 -vf "format=yuv420p" ^
            output\{0}.mp4'.format(fun.__name__)
        )
    # Deleting all temporary '.png' files in 'output' directory
    import glob
    out_path = os.path.join('output', '*png')
    for f in glob.glob(out_path):
        os.remove(f)


def apply_to_graph(fun, G = None):
    """
    Applies given algorithm to random geometric graph and displays the results side by side

    :param fun: A function which has the signature f(G) and returns iterator of edges of graph G
    :param G: a networkx Graph. If None, random geometric graph is created and applied
    :return: Plot showing G and fun(G)
    """
    if G is None:
        G = nx.random_geometric_graph(100, .125)
        # position is stored as node attribute data for random_geometric_graph
        pos = nx.get_node_attributes(G, 'pos')
        nodesize = 80
        for u, v in G.edges():
            G.edge[u][v]['weight'] = ((G.node[v]['pos'][0] - G.node[u]['pos'][0]) ** 2 +
                                      (G.node[v]['pos'][1] - G.node[u]['pos'][1]) ** 2) ** .5
    else:
        pos = graphviz_layout(G)
        nodesize = 200
    # find node near center (0.5,0.5)
    color = {}
    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) ** 2
        color[n] = d
        if d < dmin:
            ncenter = n
            dmin = d

    res = nx.Graph(list(fun(G)))
    plt.figure(figsize=(10, 8))
    plt.suptitle(fun.__name__ + " algorithm application")
    plt.subplot(1, 2, 1)
    plt.title("Original Graph G")
    nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
    nx.draw_networkx_nodes(G, pos,
                           nodelist=color.keys(),
                           node_size=nodesize,
                           node_color=list(color.values()),
                           cmap=plt.get_cmap("Reds_r")
                           ).set_edgecolor('k')
    if G is not None:
        nx.draw_networkx_labels(G,pos)
        nx.draw_networkx_edge_labels(G,pos,
                                     edge_labels=nx.get_edge_attributes(G,'weight'))
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.title("Resultant Graph, R = {0}(G)".format(fun.__name__))
    nx.draw_networkx_edges(res, pos, nodelist=[ncenter], alpha=0.4)
    nx.draw_networkx_nodes(res, pos,
                           node_color=list(color[n] for n in res.nodes()),
                           node_size=nodesize,
                           cmap=plt.get_cmap("Greens_r")).set_edgecolor('k')
    if G is not None:
        nx.draw_networkx_labels(res,pos)
        nx.draw_networkx_edge_labels(res, pos,
                                     edge_labels=nx.get_edge_attributes(res, 'weight'))
    plt.axis('off')
    plt.show()
