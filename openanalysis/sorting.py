import matplotlib.pyplot as plt
import numpy.random as ran
import matplotlib.animation as animation
from multiprocessing import Process
import numpy as np

__all__ = ['SortAnalyzer', 'SortingAlgorithm']


class SortingAlgorithm:
    """
    Base class for all sorting algorithms
    
    Remember to increment 'self.count' inside your algorithmic implementation every 
    time the control enters the inner-most loop to obtain correct visualization
    """

    def __init__(self, name):
        """
        :param name: Name of the Sorting algorithm
        """
        self.name = name
        self.hist_array = None  # 2D array to save instances of original array for each swap
        self.count = 0  # Number of basic operations performed by the algorithm

    def sort(self, array, visualization):
        """
        The Sorting algorithm must call this before proceeding
        It sets the count to 0, and initializes the history array

        :param array: 1D numpy array which has to be sorted
        :param visualization: If True, saves instances of array after each swap
        """
        self.count = 0  # Reset the count
        if visualization:
            self.hist_array = np.array(array)
        pass
        # Do sorting in derived classes


class SortAnalyzer:
    def __init__(self, sorter):
        """
        Constructor for Visualizer

        :param sorter: A Sorting Algorithm Class
        """
        self.hist_arr, self.scatter, self.animation = None, None, None
        self.sorter = sorter()
        self.fig = plt.figure()
        self.index = 0

    def __update(self, i):
        """
        Update function for animation
        Sets new array state for scatter plot

        :param i: Sent by the animator indicating the frame number
        :return: Modified scatter plot
        """
        x = np.arange(self.hist_arr.shape[1])
        y = self.hist_arr[i]
        data = np.dstack((x, y))  # call self.scatter.get_offsets() to know about initial data format
        self.scatter.set_offsets(data)
        return self.scatter,

    def visualize(self, num=100, save=False):
        """
        Visualizes given Sorting Algorithm

        :param num: Number of points that has to be chosen for visualization
        :param save: Boolean indicating whether to save animation in 'output' directory
        """
        plt.title(self.sorter.name + " Visualization")
        plt.xlabel("Array Index")
        plt.ylabel("Element")
        data = np.arange(num)
        ran.shuffle(data)
        self.sorter.sort(data, visualization=True)
        self.hist_arr = self.sorter.hist_array
        self.scatter = plt.scatter(np.arange(self.hist_arr.shape[1]), self.hist_arr[0])  # plt.scatter(x-array,y-array)
        self.animation = animation.FuncAnimation(self.fig, self.__update, frames=self.hist_arr.shape[0], repeat=False,
                                                 blit=False, interval=1)
        if save:
            import os
            import errno
            path = "output"
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise
            path = os.path.join('output', self.sorter.name + ".mp4")
            p1 = Process(
                target=lambda: self.animation.save(path, writer=animation.FFMpegWriter(fps=100)))
            p1.start()
        plt.show()

    def analyze(self, maxpts=1000, progress=True):
        """
        Plots the running time of sorting algorithm
        Checks for 3 cases, pre-sorted array, reverse sorted array and shuffled array
        Analysis is done  by inputting randomly shuffled integer arrays with size staring
        from 100, and varying upto maxpts in the steps of 100, and counting the number of
        basic operations
        
        
        :param maxpts: Upper bound on elements chosen for analysing efficiency
        :param progress: Boolean indicating whether to show progress bar or not
        """
        # x is list of input sizes
        # y_1 running time in case of Sorted Array
        # y_2 running time in case of Shuffled Array
        # y_3 running time in case of Reverse Sorted Array
        x, y = np.array([0]), [np.array([0]), np.array([0]), np.array([0])]
        labels = ['Sorted Array', 'Shuffled Array', 'Reverse Sorted Array']
        print('Please wait while analyzing {} Algorithm'.format(self.sorter.name))
        if progress:
            import progressbar
            count = 0
            max_count = (maxpts - 100) // 100
            bar = progressbar.ProgressBar(max_value=max_count)
        for n in range(100, maxpts, 100):
            # Vary n from 100 to max in steps of 100
            if progress:
                count += 1
                bar.update(count)
            data = np.arange(n)
            input_data = [np.array(data), data[::-1]]
            np.random.shuffle(data)
            input_data.append(data)
            for i in range(3):
                self.sorter.sort(input_data[i], False)
                y[i] = np.vstack((y[i], [self.sorter.count]))
            x = np.vstack((x, [n]))
        plt.suptitle(self.sorter.name + " Analysis")
        for i in range(3):
            plt.subplot(2, 2, i + 1)
            plt.title(labels[i])
            plt.xlabel("No. of Elements")
            plt.ylabel("No. of Basic Operations")
            plt.scatter(x, y[i])
        plt.tight_layout(pad=2)
        plt.show()

    @staticmethod
    def compare(algorithms, pts=2000, maxrun=5, progress=True):
        """
        Compares the given list of Sorting algorithms over and Plots a bar chart

        :param algorithms: List of Sorting algorithms
        :param pts: Number of elements in testing array
        :param maxrun: Number of iterations to take average
        :param progress: Whether to show progress bar or not
        """
        base_arr = np.arange(pts)
        np.random.shuffle(base_arr)
        algorithms = [x() for x in algorithms]  # Instantiate
        operations = {x.name: 0 for x in algorithms}
        print('Please wait while comparing Sorting Algorithms')
        if progress:
            import progressbar
            count = 0
            max_count = maxrun * len(algorithms)
            bar = progressbar.ProgressBar(max_value=max_count)
        for _ in range(maxrun):
            for algorithm in algorithms:
                if progress:
                    count += 1
                    bar.update(count)
                algorithm.sort(base_arr)
                operations[algorithm.name] += algorithm.count
                np.random.shuffle(base_arr)
        operations = [(k, v / maxrun) for k, v in operations.items()]
        plt.suptitle('Sorting Algorithm Comparision\nAveraged over {} loops'.format(maxrun))
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
