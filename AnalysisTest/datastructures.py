from OpenAnalysis.datastructures import DataStructureVisualization,DataStructureBase


class BinarySearchTree(DataStructureBase):
    """
    Sample implementation of Data Structure, incomplete
    """

    class Node:
        def __init__(self, data):
            self.left = None
            self.right = None
            self.data = data

        def __str__(self):
            return str(self.data)

    def __init__(self):
        DataStructureBase.__init__(self, "Binary Search Tree","t.png")
        self.root = None
        self.count = 0

    def get_root(self):
        return self.root

    def insert(self, item):
        newNode = BinarySearchTree.Node(item)
        insNode = self.root
        parent = None
        while insNode is not None:
            parent = insNode
            if insNode.data > newNode.data:
                insNode = insNode.left
            else:
                insNode = insNode.right
        if parent is None:
            self.root = newNode
        else:
            self.graph.add_edge(parent, newNode)
            if parent.data > newNode.data:
                parent.left = newNode
                self.graph.node[newNode]['child_status'] = 'left'
            else:
                parent.right = newNode
                self.graph.node[newNode]['child_status'] = 'right'
        self.count += 1

    def find(self, item):
        node = self.root
        while node is not None:
            if item < node:
                node = node.left
            elif item > node:
                node = node.right
            else:
                return True
        return False

    def __contains__(self, item):
        """
        To use in operator
        :param item: item to be found out
        :return: True if item in self else False
        example:
            >>> t = BinarySearchTree()
            >>> x = [9,2,1,4,3,2,6,7,0]
            >>> for item in x:
            >>>     t.insert(x)
            >>> 0 in t
                True
            >>> 10 in t
                False
        """
        return self.find(item)

    def delete(self, item):
        if item not in self:
            raise ValueError("{0} not in Tree".format(item))
        pass
        # Implement


class BinaryHeap(DataStructureBase):
    """
    Sample implementation of Data Structure, Incomplete
    Do corrections
    """

    def __init__(self):
        DataStructureBase.__init__(self, "Binary Heap","sa.png")
        self.count = 0
        self.elements = [None]

    def get_root(self):
        return self.elements[1]

    def insert(self, element):
        if element in self:
            raise Exception("not unique")
        self.count += 1
        self.elements.extend([0])
        insert_position = self.count
        while insert_position > 1 and self.elements[int(insert_position / 2)] > element:
            self.elements[insert_position] = self.elements[int(insert_position / 2)]
            insert_position = int(insert_position / 2)
        self.elements[insert_position] = element
        self.update_graph()

    def delete(self, ele):
        pos = 0
        if ele in self:
            pos = self.pos(ele)
        else:
            raise ValueError("{0} not found in Heap".format(ele))

    pass

    # Implement

    def update_graph(self):
        H = self.graph
        H.clear()
        current_position = 1
        while current_position <= int(self.count / 2):
            H.add_edge(self.elements[current_position], self.elements[2 * current_position])
            H.node[self.elements[2 * current_position]]['child_status'] = 'left'
            if 2 * current_position + 1 <= self.count:
                H.add_edge(self.elements[current_position], self.elements[2 * current_position + 1])
                H.node[self.elements[2 * current_position + 1]]['child_status'] = 'right'
            current_position += 1

    def delete_min(self):
        return self.delete(self.elements[1])

    def __contains__(self, item):
        return item in self.elements[1:]

    def pos(self, item):
        return self.elements[1:].index(item)

if __name__ == '__main__':
    DataStructureVisualization(BinaryHeap).run()