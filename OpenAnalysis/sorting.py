import matplotlib.pyplot as plt
import numpy.random as ran
import matplotlib.animation as animation
from multiprocessing import Process
import numpy as np


class SortingAlgorithm:
    """
    Base class for all sorting algorithms
    """

    def __init__(self, name: str):
        """
        :param name: Name of the Sorting algorithm
        """
        self.name = name
        self.hist_array = None  # 2D array to save instances of original array for each swap
        self.count = 0  # Number of basic operations performed by the algorithm

    def sort(self, array: np.ndarray, visualization: bool):
        """
        The Sorting algorithm must call this before proceeding
        :param array: 1D numpy array which has to be sorted
        :param visualization: If True, saves instances of array after each swap
        """
        self.count = 0  # Reset the count
        if visualization:
            self.hist_array = np.array(array)
        pass
        # Do sorting in derived classes


class SortVisualizer:
    def __init__(self, sorter) -> None:
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
        And saves it
        To-Do:       * Save it with user defined name
                     * Saving thread is too slow...Make it fast
                     * When saving is in progress, animation flickers, find a solution
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
            path = os.path.join('output',self.sorter.name + ".mp4")
            p1 = Process(
                target=lambda: self.animation.save(path, writer=animation.FFMpegWriter(fps=100)))
            p1.start()
        plt.show()

    def efficiency(self, maxpts=1000):
        """
        Plots the running time of sorting algorithm
        Checks for 3 cases, Already Sorted array, reverse sorted array and Shuffled array
        Analysis is done  by inputting randomly shuffled integer arrays with size staring
        from 100, and varying upto maxpts in the steps of 100, and counting the number of
        basic operations
        :param maxpts: Upper bound on elements chosen for analysing efficiency
        """
        # x is list of input sizes
        # y_1 running time in case of Sorted Array
        # y_2 running time in case of Shuffled Array
        # y_3 running time in case of Reverse Sorted Array
        x, y_1, y_2, y_3 = np.array([0]), np.array([0]), np.array([0]), np.array([0])
        for n in range(100, maxpts, 100):
            # Vary n from 100 to max in steps of 100
            i_1 = np.arange(n)  # array of items from 1 to n
            self.sorter.sort(i_1, False)
            val_sorted = self.sorter.count
            i_2 = i_1[::-1]  # reverse the array
            ran.shuffle(i_1)  # shuffle the array
            self.sorter.sort(i_1, False)
            val_normal = self.sorter.count
            self.sorter.sort(i_2, False)
            val_reverse = self.sorter.count
            x = np.vstack((x, [n]))  # add n to list x
            y_1 = np.vstack((y_1, [val_sorted]))  # add number of basic operations to y lists
            y_2 = np.vstack((y_2, [val_normal]))
            y_3 = np.vstack((y_3, [val_reverse]))
        plt.suptitle(self.sorter.name + " Analysis")
        plt.subplot(2, 2, 1)
        plt.title("Sorted Array")
        plt.xlabel("No. of Elements")
        plt.ylabel("No. of Basic Operations")
        plt.scatter(x, y_1)
        plt.subplot(2, 2, 2)
        plt.title("Randomly Shuffled Array")
        plt.xlabel("No. of Elements")
        plt.ylabel("No. of Basic Operations")
        plt.scatter(x, y_2)
        plt.subplot(2, 2, 3)
        plt.title("Reverse Sorted Array")
        plt.xlabel("No. of Elements")
        plt.ylabel("No. of Basic Operations")
        plt.scatter(x, y_3)
        plt.tight_layout(pad=2)
        plt.show()

    @staticmethod
    def compare(algorithms):
        """
        Compares the given list of Sorting Algorithms and Plots a bar chart
        :param algorithms: List of Sorting Algorithms
        """
        base_arr = np.arange(2000)
        np.random.shuffle(base_arr)
        arr = np.copy(base_arr)
        operations = []
        algorithms = [x() for x in algorithms] # Instantiate
        for algorithm in algorithms:
            algorithm.sort(arr)
            operations.append((algorithm.name,algorithm.count))
            arr = np.copy(base_arr)
        operations = sorted(operations,key=lambda x:x[0])
        rects = plt.bar(left=np.arange(len(operations)),height=[y for (x,y) in operations])
        plt.xticks(np.arange(len(operations)),[x for (x,y) in operations])
        ax = plt.axes()
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%d' % int(height),
                    ha='center', va='bottom')
        plt.show()

