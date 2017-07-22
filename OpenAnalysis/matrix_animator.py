import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np


class MatrixAnimator:
    def __init__(self, fn, G, pos=None, weights=True, labels=True, matrix_lables=True, node_size=300):
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(1, 3, figsize=(16, 9))
        self.fig.suptitle(fn.__name__ + ' algorithm')
        self.ax1.set_title("Graph G")
        self.ax2.set_title("Adjacency Matrix M")
        self.ax3.set_title("Final Matrix R")
        self.ax1.axis('off')

        self.frames = []
        self.active_cells = []
        self.active = []
        self.graph = G
        self.img = None
        self.lables = []
        self.fn = fn
        self.pos = pos
        self.weights = weights
        self.lables = labels
        self.matrix_labels = matrix_lables
        self.node_size = node_size

    @staticmethod
    def plot_matrix_labels(matrix, axis):
        labels = []
        n, m = matrix.shape
        for i in range(n):
            for j in range(m):
                t = axis.text(i, j, str(matrix[i, j]), va='center', ha='center')
                labels.append(t)
        return labels

    def update(self, i):
        # global img,fun
        if self.matrix_labels:
            l = np.transpose(self.frames[i]).flatten().astype(str)
            for k, old_label in enumerate(self.lables):
                old_label.set_text(l[k])
        self.img.set_data(self.frames[i])
        j, i, k = self.active[i]
        self.active_cells[0].set_xy((i - 0.5, k - 0.5,))
        self.active_cells[1].set_xy((k - 0.5, j - 0.5))
        self.active_cells[2].set_xy((i - 0.5, j - 0.5))
        return self.img, self.lables, self.active_cells

    def init_animation(self):
        masked_array = np.ma.array(self.frames[0], mask=np.isinf(self.frames[0]))
        vmin = 0
        vmax = np.max(np.ma.array(self.frames[-1], mask=np.isinf(self.frames[-1])))
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        div = make_axes_locatable(self.ax2)
        cax = div.append_axes('right', '5%', '5%')
        cax.axis('off')
        div = make_axes_locatable(self.ax3)
        cax = div.append_axes('right', '5%', '5%')
        self.img = self.ax3.imshow(masked_array, interpolation='nearest', vmin=vmin, vmax=vmax, alpha=0.7)
        if self.matrix_labels:
            self.lables = self.plot_matrix_labels(self.frames[0], self.ax3)
        else:
            self.lables = []
        self.fig.colorbar(self.img, cax=cax)
        self.active_cells.append(self.ax3.add_patch(
            patches.Rectangle((0, 0), 1, 1, fill=False, linestyle='--', color='k', linewidth=3)
        ))
        self.active_cells.append(self.ax3.add_patch(
            patches.Rectangle((0, 0), 1, 1, fill=False, linestyle='--', color='k', linewidth=3)
        ))
        self.active_cells.append(self.ax3.add_patch(
            patches.Rectangle((0, 0), 1, 1, fill=False, linestyle='-', color='k', linewidth=3)
        ))
        return self.lables + [self.img]

    def animate(self, save=False):
        result = self.fn(self.graph)
        for matrix, active in result:
            self.frames.append(matrix)
            self.active.append(active)
        # Draw the original matrix
        if self.pos is None:
            self.pos = nx.nx_pydot.graphviz_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax1, node_color='g', alpha=0.8,
                               node_size=self.node_size).set_edgecolor('k')
        nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax1, alpha=0.6)
        if self.weights:
            nx.draw_networkx_edge_labels(self.graph, self.pos, ax=self.ax1,
                                         edge_labels=nx.get_edge_attributes(self.graph, 'weight'))
        if self.lables:
            nx.draw_networkx_labels(self.graph, self.pos, ax=self.ax1)
        # Draw its adjacancy matrix
        vmin = 0
        vmax = np.max(np.ma.array(self.frames[-1], mask=np.isinf(self.frames[-1])))
        cmap = plt.get_cmap('jet')
        cmap.set_bad('white', 1.)
        masked_array = np.ma.array(self.frames[0], mask=np.isinf(self.frames[0]))
        self.ax2.imshow(masked_array, interpolation='nearest', vmin=vmin, vmax=vmax, alpha=0.7)
        if self.matrix_labels:
            self.plot_matrix_labels(self.frames[0], self.ax2)
        # Now start the animation
        x = animation.FuncAnimation(self.fig, self.update, interval=1000, blit=False,
                                    repeat=False, init_func=self.init_animation, frames=len(self.frames))
        if save:
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=1, metadata=dict(artist='V'), bitrate=1800)
            from multiprocessing import Process
            import os
            path = os.path.join('output', '%s.mp4' % self.fn.__name__)
            Process(target=x.save, args=(path,), kwargs={'writer': writer}).start()
        plt.show()

    def apply_to_graph(self, show_graph=True):
        # Draw the original matrix
        if show_graph:
            if self.pos is None:
                self.pos = nx.nx_pydot.graphviz_layout(self.graph)
            nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax1, node_color='g', alpha=0.8,
                                   node_size=self.node_size).set_edgecolor('k')
            nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax1, alpha=0.5)
            if self.weights:
                nx.draw_networkx_edge_labels(self.graph, self.pos, ax=self.ax1,
                                             edge_labels=nx.get_edge_attributes(self.graph, 'weight'))
            if self.lables:
                nx.draw_networkx_labels(self.graph, self.pos, ax=self.ax1)
        # Draw its adjacancy matrix
        result, adj = None, None
        for i, matrix in enumerate(self.fn(self.graph)):
            if i == 0:
                adj = matrix[0]
            result = matrix[0]
        print(adj, result)
        cmap = plt.get_cmap('jet')
        cmap.set_bad('white', 1.)
        vmin = 0
        vmax = np.max(result)
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        div = make_axes_locatable(self.ax2)
        cax = div.append_axes('right', '5%', '5%')
        cax.axis('off')
        masked_array = np.ma.array(adj, mask=np.isinf(adj))
        self.ax2.imshow(masked_array, interpolation='nearest', cmap=cmap, vmin=vmin, vmax=vmax)
        if self.matrix_labels:
            self.plot_matrix_labels(adj, self.ax2)
        # Now draw the final matrix
        masked_array = np.ma.array(result, mask=np.isinf(result))
        div = make_axes_locatable(self.ax3)
        cax = div.append_axes('right', '5%', '5%')
        if self.matrix_labels:
            self.plot_matrix_labels(result, self.ax3)
        self.img = self.ax3.imshow(masked_array, interpolation='nearest', cmap=cmap, vmin=vmin, vmax=vmax)
        self.fig.colorbar(self.img, cax=cax)
        plt.show()
