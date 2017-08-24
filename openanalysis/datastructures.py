import pygraphviz as pgv
import gi
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

'''
Usage Instructions:

>sudo apt install python3-dev
>put sd.glade in same working directory
>in main(),pass any instance of DataStructureBase

'''


class DataStructureBase:
    """
    Base class for implementing Data Structures
    """

    def __init__(self, name, file_path):
        """
        Constructor
        :param name: Name of Data Structure. Drawing Layout is determined by the name itself
        :param file_path: Path to store output of DS
        If the name contains 'tree', then layout is tree layout, else Graph
        """
        self.name = name
        self.is_tree = "TREE" in name.upper() or "HEAP" in name.upper()
        self.graph = {}
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

    def get_graph(self, rt):
        pass

    def draw(self, nth=None):
        if self.get_root() is None:
            print("No entries yet!")
        else:
            code = lambda x: "n" + str(abs(x)) if x < 0 else "p" + str(abs(x))
            self.get_graph(self.get_root())
            dfile = open("test_dot.dot", "w")
            dfile.write("strict digraph {\n\tnode [shape = record,height=.1];\n")
            for key in self.graph:
                if nth is not None and nth == key:
                    dfile.write(
                        "\tnode{0} [label = \"<f0> |<f1> {1}|<f2> \"] [style=filled ,fillcolor = green];\n".format(
                            code(key), key))
                else:
                    dfile.write("\tnode{0} [label = \"<f0> |<f1> {1}|<f2> \"];\n".format(code(key), key))

            for key in self.graph:
                for value in self.graph[key]:
                    dfile.write("\t\"node{0}\":{1}->\"node{2}\":f1;\n".format(code(key), "f0"
                    if self.graph[key][value]['child_status'] == 'left'
                    else "f2", code(value)))

            dfile.write("}")
            dfile.close()
            pgv.AGraph("test_dot.dot").draw(self.file_path, prog="dot", format="png")


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
            val = self.map[choice](ele)
            if val is False:  # Search or Delete Case
                dialog = gtk.MessageDialog(None, 0, gtk.MessageType.ERROR,
                                           gtk.ButtonsType.CANCEL, "Value not found ERROR")
                dialog.format_secondary_text(
                    "Element not found in the %s" % self.ds.name)
                dialog.run()
                dialog.destroy()
            else:
                val = ele if val is True else None
                self.ds.draw(val)
                state.set_from_file(self.ds.file_path)
        except:
            raise
