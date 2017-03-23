# HEAP SORT
# WORKS


class Heap:

    count = 0

    def __init__(self, a, typ):
        self.elements = [0 for k in range(len(a)+1)]
        self.typ = typ
        for j in a:
            self.add(j)

    def add(self, element):
        self.count += 1
        insert_position = self.count
        while insert_position > 1 and self.compare_to(self.elements[insert_position/2], element):
            self.elements[insert_position] = self.elements[insert_position/2]
            insert_position /= 2
        self.elements[insert_position] = element

    def remove(self):
        root = self.elements[1]
        item = self.elements[self.count]
        self.count -= 1
        self.elements[1] = item
        insert_position = 1
        is_heap = False
        while insert_position <= self.count / 2 and not is_heap:
            extreme_c_pos = 2 * insert_position
            extreme_c_pos = extreme_c_pos if self.compare_to(self.elements[extreme_c_pos+1], self.elements[extreme_c_pos]) \
                else extreme_c_pos + 1
            if self.compare_to(self.elements[extreme_c_pos], item):
                is_heap = True
            else:
                self.elements[insert_position] = self.elements[extreme_c_pos]
                insert_position = extreme_c_pos
        self.elements[insert_position] = item
        return root

    def compare_to(self, p, q):
        if self.typ:
            return p > q
        return p < q

if __name__ == '__main__':

    try:
        print "Enter number of elements in the heap"
        n = int(raw_input())
        print "Enter elements one by one"
        a = map(int, raw_input().split())
        h = Heap(a, True)
        print "Heap is"
        for i in range(1, len(a)+1):
            print h.elements[i],
        print "\n"
        print "Sorted elements are:"
        for i in range(n):
            print h.remove(),

    except Exception as e:
        print e

    finally:
        print "\nGoodBye!"
