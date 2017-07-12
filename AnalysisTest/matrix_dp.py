from OpenAnalysis.matrix_animator import MatrixAnimator
import networkx as nx
import numpy as np


def Floyd_Warshall(G):
    D = nx.to_numpy_matrix(G)
    m, n = D.shape
    for i in range(0, n):
        for j in range(0, n):
            if i != j and D[i, j] == 0:
                D[i, j] = float('inf')
    yield np.array(D), (0, 0, 0)
    count = 0
    for k in range(0, n):
        for i in range(0, n):
            for j in range(0, n):
                if D[i, j] > D[i, k] + D[k, j]:
                    yield np.array(D), (i, j, k)
                    D[i, j] = D[i, k] + D[k, j]
                print(count)
                count += 1
    yield np.array(D), (0, 0, 0)


def Transitive_Closure(G):
    D = nx.to_numpy_matrix(G).astype(bool)
    m, n = D.shape
    for k in range(0, n):
        for i in range(0, n):
            for j in range(0, n):
                if not D[i, j]:
                    yield np.array(D), (i, j, k)
                    D[i, j] = D[i, k] and D[k, j]
    yield np.array(D), (0, 0, 0)


if __name__ == "__main__":
    M = nx.from_numpy_matrix(
        np.matrix(
            [[0, 1, 0, 0, 1, 0],
             [1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 0],
             [0, 0, 1, 0, 1, 1],
             [1, 1, 0, 1, 0, 0],
             [0, 0, 0, 1, 0, 0]]
        ))
    import random
    for u, v in M.edges():
        M.edge[u][v]['weight'] = random.randint(1, 10)
    MatrixAnimator(Floyd_Warshall, M).animate(True)

