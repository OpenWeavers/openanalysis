class UnionFind:
    """Union-find data structure.

    Each unionFind instance X maintains a family of disjoint sets of
    hashable objects, supporting the following two methods:

    - X[item] returns a name for the set containing the given item.
      Each set is named by an arbitrarily-chosen one of its members; as
      long as the set remains unchanged it will keep the same name. If
      the item is not yet part of a set in X, a new singleton set is
      created for it.

    - X.union(item1, item2, ...) merges the sets containing each item
      into a single larger set.  If any item is not yet part of a set
      in X, it is added to X as one of the members of the merged set.

      Union-find data structure. Based on Josiah Carlson's code,
      http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/215912
      with significant additional changes by D. Eppstein.
      http://www.ics.uci.edu/~eppstein/PADS/UnionFind.py

    """

    def __init__(self):
        """Create a new empty union-find structure."""
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        """Find and return the name of the set containing the object."""

        # check for previously unknown object
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    def __iter__(self):
        """Iterate through all items ever found or unioned by this structure.

        """
        return iter(self.parents)

    def union(self, *objects):
        """Find the sets containing the objects and merge them all."""
        roots = [self[x] for x in objects]
        # Find the heaviest root according to its weight.
        heaviest = max(roots, key=lambda r: self.weights[r])
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest


class PriorityQueue:
    """
    A simple Priority Queue Implementation for usage in algorithms
    Internally uses heapq to maintain min-heap and tasks are added
    as tuples (priority,task) to queue. To make the order of tasks
    with same priority clear, count of element insertion is added
    to the tuple, making it as (priority,count,task), which means
    that tasks are first ordered by priority then by count
    """
    def __init__(self):
        """
        Create an empty Priority Queue
        """
        from itertools import count
        self.heap = []
        self.counter = count()

    def add_task(self, task, priority):
        """
        Add a task to priority queue
        :param task: task to be added to queue
        :param priority: priority of the task, must be orderable
        """
        import heapq
        heapq.heappush(self.heap, (priority, next(self.counter), task))

    def remove_min(self):
        """
        Removes the minimum element of heap
        :return: task with less priority
        """
        import heapq
        return heapq.heappop(self.heap)[2]

    def remove(self, task):
        """
        Removes the tasks from Queue
        :param task: task to removed from the Queue

        Currently it takes O(n) time to find , and O(log n) to remove, making it O(n)
        further improvements can be done
        """
        import heapq
        for task_pair in self.heap:
            if task_pair[2] == task:
                self.heap.remove(task_pair)
                heapq.heapify(self.heap)

    def update_task(self, task, new_priority):
        """
        Updates the priority of exsisting task in Queue
        :param task: task to be updated
        :param new_priority: new value of priority

        Updation is implemented as deletion and insertion, takes O(n) time
        further improvements can be done
        """
        self.remove(task)
        self.add_task(task, new_priority)