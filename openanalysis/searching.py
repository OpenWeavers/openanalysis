import matplotlib.pyplot as plt
import numpy as np

__all__ = ['SearchAnalyzer', 'SearchingAlgorithm']


class SearchingAlgorithm:
    """
    Base class for all Searching algorithms
     
    Remember to increment 'self.count' inside your algorithmic implementation every 
    time the control enters the inner-most loop to obtain correct visualization
    """

    def __init__(self, name):
        """
        Constructor

        :param name: Name of Searching algorithm being implemented
        """
        self.count = 0
        self.name = name

    def search(self, arr, key):
        """
        The core search method

        :param arr: numpy array, in witch the search is performed
        :param key: the element to be searched
        :return: True if key in arr else False
        """
        self.count = 0
        pass
        # Do search in derived classes


class SearchAnalyzer:
    """
    Class for Visualizing Search algorithms
    """

    def __init__(self, searcher):
        """
        Constructor for visualizer
        :param searcher: Implementation of a Searching Algorithm
        """
        self.searcher = searcher()  # Instantiate
        self.fig = plt.figure()

    def analyze(self, maxpts=1000, progress=True):
        """
        Plots the running time of sorting algorithm
        Checks for 3 cases, Already Sorted array, reverse sorted array and Shuffled array
        Analysis is done  by inputting integer arrays with size staring from 100, and varying
        upto maxpts in the steps of 100, and counting the number of basic operations

        :param maxpts: Maximum number of element in the array, using witch analysis is done
        :param progress: Boolean indicating whether to show the progress bar or not
        """
        # x Number of elements
        # y[0] number of comparisons when First Element is the key
        # y[1] number of comparisons when Middle Element is the key
        # y[2] number of comparisons when key is not present in the array
        # y[3] number of comparisons when key is a randomly chosen element
        x, y = np.array([0]), [np.array([0]), np.array([0]), np.array([0]), np.array([0])]
        labels = ['First Element is the key', 'Middle Element is the key',
                  'Key not in array', 'Key at random position in the array']
        print('Please wait while analyzing {} Algorithm'.format(self.searcher.name))
        if progress:
            import progressbar
            count = 0
            max_count = (maxpts - 100) // 100
            bar = progressbar.ProgressBar(max_value=max_count)
        for i in range(100, maxpts, 100):
            if progress:
                count += 1
                bar.update(count)
            x = np.vstack((x, [i]))
            arr = np.arange(0, i, 1)
            keys = [0, i // 2, i + 1, np.random.randint(0, i)]
            for j in range(4):
                self.searcher.search(arr, keys[j])
                y[j] = np.vstack((y[j], [self.searcher.count]))
        plt.suptitle(self.searcher.name + " Analysis", size=19)
        for i in range(4):
            plt.subplot(2, 2, i + 1)
            plt.title(labels[i])
            plt.xlabel("No. of Elements")
            plt.ylabel("No. of Basic Operations")
            plt.scatter(x, y[i])
        plt.tight_layout()
        plt.show()

    @staticmethod
    def compare(algorithms, pts=2000, maxrun=5, progress=True):
        """
        Compares the given list of Searching algorithms and Plots a bar chart

        :param algorithms: List of Searching algorithms
        :param pts: Number of elements in testing array
        :param maxrun: Number of iterations to take average
        :param progress: Whether to show Progress bar or not
         """
        arr = np.arange(pts)
        algorithms = [x() for x in algorithms]
        operations = {x.name: 0 for x in algorithms}
        print('Please wait while comparing Searching Algorithms')
        if progress:
            import progressbar
            count = 0
            max_count = maxrun * len(algorithms)
            bar = progressbar.ProgressBar(max_value=max_count)
        for _ in range(maxrun):
            key = np.random.randint(0, 2000)
            for algorithm in algorithms:
                if progress:
                    count += 1
                    bar.update(count)
                algorithm.search(arr, key)
                operations[algorithm.name] += algorithm.count
        operations = [(k, v / maxrun) for k, v in operations.items()]
        plt.suptitle('Searching Algorithm Comparision\nAveraged over {} loops'.format(maxrun))
        rects = plt.bar(left=np.arange(len(operations)), height=[y for (x, y) in operations])
        plt.xticks(np.arange(len(operations)), [x for (x, y) in operations])
        ax = plt.axes()
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%d' % int(height),
                    ha='center', va='bottom')
        plt.ylabel('Average number of basic operations')
        plt.show()
