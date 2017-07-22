import networkx as nx
import matplotlib.pyplot as plt


def tree_growth_visualizer(fun):
    """
    Visualizer function for Graph algorithms yielding the edges
    :param fun: A function which has the signature f(G) and returns iterator of edges of graph G
    :return: Saves the images of growth step in given directory. ffmpeg can be used to make video
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
    os.system(
        'ffmpeg -y -r 2 -i output/fig%04d.png \
         -c:v libx264 -vf "format=yuv420p" \
          output/{0}.mp4'.format(fun.__name__)
    )
    os.system('rm output/*png')


def apply_to_graph(fun):
    """
    Visualizer function for Graph algorithms yielding the edges
    :param fun: A function which has the signature f(G) and returns iterator of edges of graph G
    :return: Plot showing G and fun(G)
    """
    G = nx.random_geometric_graph(100, .125)
    # position is stored as node attribute data for random_geometric_graph
    pos = nx.get_node_attributes(G, 'pos')
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
    for u, v in G.edges():
        G.edge[u][v]['weight'] = ((G.node[v]['pos'][0] - G.node[u]['pos'][0]) ** 2 +
                                  (G.node[v]['pos'][1] - G.node[u]['pos'][1]) ** 2) ** .5
    res = nx.Graph(list(fun(G)))
    plt.figure(figsize=(10, 8))
    plt.suptitle(fun.__name__ + " algorithm application")
    plt.subplot(1, 2, 1)
    plt.title("Original Graph G")
    nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
    nx.draw_networkx_nodes(G, pos,
                           nodelist=color.keys(),
                           node_size=80,
                           node_color=list(color.values()),
                           cmap=plt.get_cmap("Reds_r")
                           ).set_edgecolor('k')
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.title("Resultant Graph, R = {0}(G)".format(fun.__name__))
    nx.draw_networkx_edges(res, pos, nodelist=[ncenter], alpha=0.4)
    nx.draw_networkx_nodes(res, pos,
                           node_color=list(color[n] for n in res.nodes()),
                           node_size=80,
                           cmap=plt.get_cmap("Greens_r")).set_edgecolor('k')
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.axis('off')
    plt.show()
