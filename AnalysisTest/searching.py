from OpenAnalysis.searching import SearchingAlgorithm,SearchVisualizer


class LinearSearch(SearchingAlgorithm):
    def __init__(self):
        SearchingAlgorithm.__init__(self, "Linear Search")

    def search(self, arr, key) -> bool:
        SearchingAlgorithm.search(self, arr, key)
        for i in range(0, arr.size - 1):
            self.count += 1
            if arr[i] == key:
                return True
        return False


class BinarySearch(SearchingAlgorithm):
    def __init__(self):
        SearchingAlgorithm.__init__(self, "Binary Search")

    def search(self, arr, key) -> bool:
        SearchingAlgorithm.search(self, arr, key)
        SearchingAlgorithm.search(self, arr, key)
        low, high = 0, arr.size - 1
        while low <= high:
            mid = int((low + high) / 2)
            self.count += 1
            if arr[mid] == key:
                return True
            elif arr[mid] < key:
                low = mid + 1
            else:
                high = mid - 1
        return False

if __name__ == "__main__":
    SearchVisualizer(BinarySearch).analyze(maxpts=10000)