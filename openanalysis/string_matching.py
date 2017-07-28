from warnings import warn
import numpy as np
import os
import matplotlib.pyplot as plt
from random import randint, randrange
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.mlab import griddata

__all__ = ['StringMatchingAnalyzer', 'StringMatchingAlgorithm']


class StringMatchingAlgorithm:
    """
    Base class for all (Comparision Based) String Matching algorithms
    """

    def __init__(self, name):
        self.name = name
        self.count = 0  # Number of basic comparison
        self.dat = np.array([])

    def match(self, text, pattern):
        """
        The core matching function
        :param text: Source Text
        :param pattern: String to be matched
        :return: True if pattern in text else False
        Do the exact matching in Derived Classes by calling this function first
        """
        self.count = 0
        pass


class StringMatchingAnalyzer:
    __package_directory = os.path.dirname(os.path.abspath(__file__))
    __sample_path = os.path.join(__package_directory, 'string_matching_samples')  # openanalysis/string_matching_samples
    __samples_list = os.listdir(__sample_path)
    __min_text_length = 5000
    __min_patt_length = 500

    # The samples are text files stored in string_matching_samples directory of Current Working
    # Directory. You can download the sample tar.gz texts from the SMART website.
    # https://www.dmi.unict.it/~faro/smart/download/data/

    def __init__(self, matcher):
        """
        Constructor for Analyzer
        :param matcher: A class which is derived from StringMatchingBase
        """
        self.matcher = matcher()  # Instantiate

    def analyze(self, max_text_length=10000, max_patt_length=1000, progress=True, input_file_path=None):
        """
        Analyzes given algorithm by varying both text and pattern length and plots it in 3D space

        :param max_text_length: Maximum length of text used in analysis. Should be greater than 5000
        :param max_patt_length: Maximum length of pattern used in analysis. Should be greater than 500
        :param progress: If True, Progress bar is shown
        :param input_file_path: Path to the sample file. Must be larger than 5000 char length. If None, analysis is done with in-built sample
        :return: 3D plot of running time vs text and pattern length
        """
        # Analyzes the matching algorithm
        if max_text_length < self.__min_text_length:
            raise ValueError('Minimum text length is {}'.format(self.__min_text_length))
        if max_patt_length < self.__min_patt_length:
            raise ValueError('Minimum text length is {}'.format(self.__min_patt_length))
        if max_text_length < max_patt_length:
            raise ValueError(
                'Pattern length {} is incompatible with Text Length {}'.format(max_patt_length, max_text_length))
        if input_file_path is None:
            input_file_path = os.path.join(self.__sample_path,
                                           self.__samples_list[randrange(0, len(self.__samples_list))])
        file = open(input_file_path, 'r')
        file_text = file.read()
        if max_text_length > len(file_text):
            raise ValueError('File length {} is smaller than {}'.format(len(file_text), max_text_length))
        data_array = []
        print('Please wait while analysing {} algorithm'.format(self.matcher.name))
        if progress:
            import progressbar
            count = 0
            max_count = (max_text_length - 1000) // 100 * (max_patt_length - 100) // 5
            bar = progressbar.ProgressBar(max_value=max_count)
        for n in range(1000, max_text_length, 100):
            for m in range(100, max_patt_length, 5):
                if progress:
                    bar.update(count)
                    count += 1
                pos = randint(0, len(file_text) - n)
                text = file_text[pos:pos + n]  # Select a random text of size n
                pos = randint(0, len(text) - m)
                pattern = text[pos:pos + m]  # Select a random pattern of size m from text, where m<n
                self.matcher.match(text, pattern)  # Run the string matching algorithm with T and P as parameters
                data_array.append((n, m, self.matcher.count))

        dat = np.array(data_array)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        x = dat[:, 0]
        y = dat[:, 1]
        z = dat[:, 2]
        xi = np.linspace(min(x), max(x))
        yi = np.linspace(min(y), max(y))
        X, Y = np.meshgrid(xi, yi)
        Z = griddata(x, y, z, xi, yi, interp='linear')
        surf = ax.plot_surface(X, Y, Z, rstride=5, cstride=5, cmap=plt.get_cmap('jet'), linewidth=1, antialiased=True)
        ax.set_xlabel('length of text $n$')
        ax.set_ylabel('length of pattern $m$')
        ax.set_zlabel('number of basic operations performed $c$')
        plt.suptitle('{0} Analysis\n Sample = {1}'.format(self.matcher.name, os.path.basename(input_file_path)))
        ax.set_zlim3d(np.min(Z), np.max(Z))
        fig.colorbar(surf)
        plt.show()

    @staticmethod
    def compare(algorithms, n=1000, m=500, maxrun=5, progress=True, input_file_path=None):
        """
        Compares the string matching algorithms

        :param algorithms: List of String Matching Algorithm classes
        :param n: Text length to be used for comparision
        :param m: Pattern Length to be used for comparision
        :param maxrun: Number of times the test has to be performed. Warns if it is greater than 5
        :param progress: Boolean indicating whether to show Progress bar during comparision, True by default
        :param input_file_path: The path of custom file to be used for analysis. If not given, default file is selected from in-built file
        :return: Bar charts showing the average of basic operations performed
        """
        algorithms = [x() for x in algorithms]
        if input_file_path is None:
            input_file_path = os.path.join(StringMatchingAnalyzer.__sample_path,
                                           StringMatchingAnalyzer.__samples_list[
                                               randrange(0, len(StringMatchingAnalyzer.__samples_list))])
        file = open(input_file_path, 'r')
        file_text = file.read()
        if n > len(file_text):
            raise ValueError('{n} is greater than file text length {l}'.format(n=n, l=len(file_text)))
        if m > n:
            raise ValueError('Text length {n} is lesser than Pattern Length {m}'.format(n=n, m=m))
        if maxrun > 5:
            warn('More than 5 loops for testing can take significant amount of time')
        operations = {x.name: 0 for x in algorithms}
        if progress:
            import progressbar
            count = 0
            max_count = maxrun * len(algorithms)
            bar = progressbar.ProgressBar(max_value=max_count)
        for i in range(maxrun):
            pos = randint(0, len(file_text) - n)
            text = file_text[pos:pos + n]  # Select a random text of size n
            pos = randint(0, len(text) - m)
            pattern = text[pos:pos + m]  # Select a random pattern of size m from text, where m<n
            for algorithm in algorithms:
                if progress:
                    count += 1
                    bar.update(count)
                algorithm.match(text, pattern)
                operations[algorithm.name] += algorithm.count
        operations = [(k, v / maxrun) for k, v in operations.items()]
        plt.suptitle(
            'Comparision of String Matching Algorithms\n n = {}, m = {}\n Averaged over {} loops'.format(n, m, maxrun))
        operations = sorted(operations, key=lambda x: x[0])
        rects = plt.bar(left=np.arange(len(operations)), height=[y for (x, y) in operations])
        plt.xticks(np.arange(len(operations)), [x for (x, y) in operations])
        ax = plt.axes()
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%d' % int(height),
                    ha='center', va='bottom')
        plt.show()
