import networkx as nx
import matplotlib.pyplot as plt
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
import os

'''
Usage Instructions:

>sudo apt install python-gi-cairo
>put sd.glade in same working directory
>in main(),pass any instance of DataStructureBase

'''


class DataStructureBase:
    """
    Base class for implementing Data Structures
    """

    def __init__(self, name: str,file_path):
        """
        Constructor
        :param name: Name of Data Structure. Drawing Layout is determined by the name itself
        :param file_path: Path to store output of DS
        If the name contains 'tree', then layout is tree layout, else Graph
        """
        self.name = name
        self.is_tree = "TREE" in name.upper() or "HEAP" in name.upper()
        self.layout = self.__binary_tree_layout if self.is_tree else self.__hierarchy_pos
        self.graph = nx.Graph()
        self.file_path = file_path
        print(os.path.abspath(file_path))
        # Layout to draw BFS tree

    def insert(self, item):
        """
        Insert item to Data Structure
        While inserting, add a edge from parent to child in self.graph
        :param item: item to be added
        """
        pass

    def delete(self, item):
        """
        Delete the item from Data Structure
        While removing, delete item from self.graph and modify the edges if necessary
        :param item: item to be deleted
        """
        pass

    def find(self, item):
        """
        Finds the item in Data Structure
        :param item: item to be searched
        :return: True if item in self else False
        also can implement __contains__(self,item)
        """
        pass

    def __contains__(self, item):
        return self.find(item)

    def get_root(self):
        """
        Return the root for drawing purpose
        :return:
        """
        pass

    def draw(self):
        """
        ----old-----
        Do a BFS and draw the Data Structure
        Data Structure is essentially graph like and can be represented by Mathematical Relation
        For example Graph G : 1--2--3 can be represented as R_G = {(1,2),(2,3)}
        In python they can be represented as Set, whose elements are tuples
        At last, set can be transformed into list, and a graph can be created
        example:
            >>> s = {(1,2),(2,3),(1,3)}
            >>> r = list(s)
            >>> G = nx.Graph(r)

        Such a set can be crated during operations or a BFS on Data Structure by updating self
        -----new-----
        plots self.graph, saves the image and returns the path to saved image
        """
        Tree = self.graph
        if Tree.nodes():
            plt.clf()
            pos = self.layout(Tree, self.get_root())
            nx.draw(Tree, pos, with_labels=True)
            plt.savefig(self.file_path)
        return self.file_path

    @staticmethod
    def __binary_tree_layout(G, root, width=1., vert_gap=0.2, vert_loc=0., xcenter=0.5,
                             pos=None, parent=None):
        """If there is a cycle that is reachable from root, then this will see infinite recursion.
           G: the graph
           root: the root node of current branch
           width: horizontal space allocated for this branch - avoids overlap with other branches
           vert_gap: gap between levels of hierarchy
           vert_loc: vertical location of root
           xcenter: horizontal location of root
           pos: a dict saying where all nodes go if they have been assigned
           parent: parent of this branch.
           each node has an attribute "left: or "right\""""
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        neighbors = G.neighbors(root)
        if parent is not None:
            neighbors.remove(parent)
        if len(neighbors) != 0:
            dx = width / 2.
            leftx = xcenter - dx / 2
            rightx = xcenter + dx / 2
            for neighbor in neighbors:
                if G.node[neighbor]['child_status'] == 'left':
                    pos = DataStructureBase.__binary_tree_layout(G, neighbor, width=dx, vert_gap=vert_gap,
                                                                 vert_loc=vert_loc - vert_gap, xcenter=leftx, pos=pos,
                                                                 parent=root)
                elif G.node[neighbor]['child_status'] == 'right':
                    pos = DataStructureBase.__binary_tree_layout(G, neighbor, width=dx, vert_gap=vert_gap,
                                                                 vert_loc=vert_loc - vert_gap, xcenter=rightx, pos=pos,
                                                                 parent=root)
        return pos

    @staticmethod
    def __hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
        '''If there is a cycle that is reachable from root, then result will not be a hierarchy.

           G: the graph
           root: the root node of current branch
           width: horizontal space allocated for this branch - avoids overlap with other branches
           vert_gap: gap between levels of hierarchy
           vert_loc: vertical location of root
           xcenter: horizontal location of root
        '''

        def h_recur(G, root, width=1., vert_gap=0.2, vert_loc=0., xcenter=0.5,
                    pos=None, parent=None, parsed=[]):
            if (root not in parsed):
                parsed.append(root)
                if pos == None:
                    pos = {root: (xcenter, vert_loc)}
                else:
                    pos[root] = (xcenter, vert_loc)
                neighbors = G.neighbors(root)
                if parent != None:
                    neighbors.remove(parent)
                if len(neighbors) != 0:
                    dx = width / len(neighbors)
                    nextx = xcenter - width / 2 - dx / 2
                    for neighbor in neighbors:
                        nextx += dx
                        pos = h_recur(G, neighbor, width=dx, vert_gap=vert_gap,
                                      vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                      parent=root, parsed=parsed)
            return pos

        return h_recur(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5)


class DataStructureVisualization:
    """
    Class for visualizing data structures in GUI
    Using GTK+ 3
    """
    __package_directory = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, ds):
        """
        Constructor
        :param ds: Any data structure, which is an instance of DataStructureBase
        """
        self.ds = ds()  # Instantiate
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.join(self.__package_directory, "sd.glade"))
        self.builder.connect_signals(self)
        self.map = [self.ds.insert, self.ds.delete, self.ds.find]

    def run(self):
        self.builder.get_object("stage").show_all()
        self.builder.get_object("name").set_text(self.ds.name)
        gtk.main()

    def on_stage_destroy(self, x):
        gtk.main_quit()

    def action_clicked_cb(self, button):
        try:
            ele = int(self.builder.get_object("item").get_text())
            choice = int(self.builder.get_object("operation").get_active())
            state = self.builder.get_object("state")
            self.map[choice](ele)
            state.set_from_file(self.ds.draw())
        except Exception as e:
            raise
