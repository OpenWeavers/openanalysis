from OpenAnalysis.base_data_structures import UnionFind,PriorityQueue
import OpenAnalysis.tree_growth as TreeGrowth


def kruskal_mst(G):
    """
    Finds Minimum Spanning Tree of graph by Kruskal's Algorithm
    :param G: networkx graph
    :return: iterator through edges of Minimum spanning Tree
    """
    edge_list = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
    subtrees = UnionFind()
    for u, v, w in edge_list:
        if subtrees[u] != subtrees[v]:
            yield (u, v, {'weight': w})
            subtrees.union(u, v)


def prim(G):
    """
    Finds Minimum Spanning Tree of graph by Prim's Algorithm
    :param G: networkx graph
    :return: iterator through edges of Minimum spanning Tree
    """
    V = G.nodes()  # Set of all vertices of G
    while V:
        # We pop the nodes as soon as they are visited,
        # so this means "until all the nodes are visited"
        u = V.pop(0)  # Now remove the first vertex and start building the tree
        visited = {u}  # Set of visited nodes
        stringe_heap = []  # Store the stringe nodes with weights
        import heapq
        for v in G.neighbors(u):
            heapq.heappush(stringe_heap,
                           (G.edge[u][v]['weight'], u, v))
            # Now build the min heap storing (weight,source,dest) tuples
            # Tuples are sorted by their first element
        # Now start popping from heap,and build MST
        while stringe_heap:
            weight, u_star, v_star = heapq.heappop(stringe_heap)
            if v_star in visited:  # No need to do anything since v_star is already visited
                continue
            visited.add(v_star)  # Mark dest as visited
            V.remove(v_star)
            yield (u_star, v_star, {'weight': weight})  # yield the edge
            for w_star in G.neighbors(v_star):  # Update strige heap with neighbour edges of v_star
                if w_star not in visited:
                    heapq.heappush(stringe_heap, (G.edge[v_star][w_star]['weight'], v_star, w_star))


def dfs(G, root=None):
    """
    Iterates through edges of DFS tree of G
    :param G: networkx Graph
    :param root: node to start DFS from. If it is none, DFS is done for all components of G
                 else DFS is done for components connected with root
    :return: Iterator of edges of DFS tree
    """
    visited = set()
    if root is None:
        nodes = G.nodes()  # nodes to visit
    else:
        nodes = [root]
    for start in nodes:
        if start in visited:
            continue
        visited.add(start)
        stack = [(start, child) for child in sorted(G.neighbors(start), reverse=True)]
        while stack:
            parent, child = stack.pop()
            if child not in visited:
                visited.add(child)
                yield (parent, child)
                stack += [(child, grandchild) for grandchild in sorted(G.neighbors(child), reverse=True)]


def bfs(G, root=None):
    """
        Iterates through edges of DFS tree of G
        :param G: networkx Graph
        :param root: node to start DFS from. If it is none, DFS is done for all components of G
                     else DFS is done for components connected with root
        :return: Iterator of edges of DFS tree
        """
    visited = set()
    if root is None:
        nodes = G.nodes()
    else:
        nodes = [root]
    for start in nodes:
        if start in visited:
            continue
        visited.add(start)
        Q = [start]
        while Q:
            current = Q.pop(0)
            for n in sorted(G.neighbors(current)):
                if n not in visited:
                    visited.add(n)
                    Q.append(n)
                    yield (current, n)


def dijkstra(G, source=None):
    """
    Returns edges of Single source shortest path starting form source
    :param G: networkx Graph
    :param source: source to compute the distances from
    :return: Iterator through edges of SSSP Tree
    """
    if source is None: source = G.nodes()[0]
    V = G.nodes()
    dist, prev = {}, {}
    Q = PriorityQueue()
    for v in V:
        dist[v] = float("inf")
        prev[v] = None
        Q.add_task(task=v, priority=dist[v])
    dist[source] = 0
    Q.update_task(task=source, new_priority=dist[source])
    visited = set()
    for i in range(0, len(G.nodes())):
        u_star = Q.remove_min()
        if prev[u_star] is not None:
            yield (u_star, prev[u_star])
        visited.add(u_star)
        for u in G.neighbors(u_star):
            if u not in visited and dist[u_star] + G.edge[u][u_star]['weight'] < dist[u]:
                dist[u] = dist[u_star] + G.edge[u][u_star]['weight']
                prev[u] = u_star
                Q.update_task(u, dist[u])


if __name__ == "__main__":
    TreeGrowth.tree_growth_visualizer(dijkstra)