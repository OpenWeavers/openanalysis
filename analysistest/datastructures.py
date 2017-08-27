from openanalysis.datastructures import DataStructureVisualization, DataStructureBase


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
        DataStructureBase.__init__(self, "Binary Search Tree", "t.png")
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
            if parent.data > newNode.data:
                parent.left = newNode
            else:
                parent.right = newNode
        self.count += 1

    def find(self, item):
        node = self.root
        while node is not None:
            if item < node.data:
                node = node.left
            elif item > node.data:
                node = node.right
            else:
                return True
        return False
    
    def min_value_node(self):
        current = self.root
        while current.left is not None:
            current = current.left
        return current

    def delete(self, item):
        if item not in self:
            raise ValueError("{0} not in Tree".format(item))
        else:
            if self.root is None:
                return self.root
            if self.root.data == item and (self.root.left is None or self.root.right is None):
                if self.root.left is None and self.root.right is None:
                    self.root = None
                elif self.root.data == item and self.root.left is None:
                    self.root = self.root.right
                elif self.root.data == item and self.root.right is None:
                    self.root = self.root.left
                return self.root
            if item < self.root.data:
                temp = self.root
                self.root = self.root.left
                temp.left = self.delete(item)
                self.root = temp
            elif item > self.root.data:
                temp = self.root
                self.root = self.root.right
                temp.right = self.delete(item)
                self.root = temp
            else:
                if self.root.left is None:
                    return self.root.right
                elif self.root.right is None:
                    return self.root.left
                temp = self.root
                self.root = self.root.right
                min_node = self.min_value_node()
                temp.data = min_node.data
                temp.right = self.delete(min_node.data)
                self.root = temp
            return self.root

    def get_graph(self, rt):
        if rt is None:
            return
        self.graph[rt.data] = {}
        if rt.left is not None:
            self.graph[rt.data][rt.left.data] = {'child_status': 'left'}
            self.get_graph(rt.left)
        if rt.right is not None:
            self.graph[rt.data][rt.right.data] = {'child_status': 'right'}
            self.get_graph(rt.right)


class BinaryHeap(DataStructureBase):
    """
    Sample implementation of Data Structure, Incomplete
    Do corrections
    """

    def __init__(self):
        DataStructureBase.__init__(self, "Binary Heap", "sa.png")
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

    def delete(self, ele):
        pos = 0
        if ele in self:
            pos = self.pos(ele)
        else:
            raise ValueError("{0} not found in Heap".format(ele))
        pass

    def __iter__(self):
        return iter(self.elements[1:])

    def get_graph(self, root):
        self.graph = {x:{} for x in self}
        current_position = 1
        while current_position <= int(self.count / 2):
            current = self.elements[current_position]
            left_child = self.elements[2 * current_position]
            self.graph[current][left_child] = {'child_status': 'left'}
            if 2 * current_position + 1 <= self.count:
                right_child = self.elements[2 * current_position + 1]
                self.graph[current][right_child] = {'child_status': 'right'}
            current_position += 1

    def delete_min(self):
        return self.delete(self.elements[1])

    def find(self, item):
        return item in self.elements[1:]

    def pos(self, item):
        return self.elements[1:].index(item)


if __name__ == '__main__':
    DataStructureVisualization(BinaryHeap).run()
