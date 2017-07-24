import numpy as np
import os
import matplotlib.pyplot as plt
from random import randint
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.mlab import griddata


class StringMatchingAlgorithm:
    """
    Base class for all (Comparision Based) String Matching algorithms
    """
    def __init__(self, name):
        self.name = name
        self.count = 0  # Number of basic comparison
        self.dat = np.array([])

    def match(self, text: str, pattern: str):
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
    """
    Class to analyze the instances of StringMatchingAlgorithm
    """
    __package_directory = os.path.dirname(os.path.abspath(__file__))
    max_text_length = 10000
    max_patt_length = 1000
    text = ''
    pattern = ''
    sample_path = os.path.join(__package_directory, 'string_matching_samples')    # ../openanalysis/string_matching_samples
    samples_list = os.listdir(sample_path)
    # The samples are text files stored in string_matching_samples directory of Current Working
    # Directory. You can download the sample tar.gz texts from the SMART website.
    # https://www.dmi.unict.it/~faro/smart/download/data/

    def __init__(self, matcher):
        self.matcher = matcher()  # Instantiate
        # print(self.samples_list)

    def analyze(self):
        # Analyzes the matching algorithm
        file = open(os.path.join(self.sample_path, self.samples_list[randint(0, 3)]), 'r')
        file_text = file.read() 
        data_array = []
        print('please wait while analysing...')
        for n in range(1000, self.max_text_length, 100):
            for m in range(100, self.max_patt_length, 5):
                pos = randint(0, len(file_text) - n)
                text = file_text[pos:pos + n]   # Select a random text of size n
                pos = randint(0, len(text)-m)
                pattern = text[pos:pos+m]   # Select a random pattern of size m from text, where m<n
                self.matcher.match(text, pattern)   # Run the string matching algorithm with T and P as parameters
                # print(self.matcher.count)
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
        surf = ax.plot_surface(X, Y, Z, rstride=5, cstride=5, cmap=cm.jet, linewidth=1, antialiased=True)
        ax.set_xlabel('length of text')
        ax.set_ylabel('length of pattern')
        ax.set_zlabel('number of basic operations performed')
        ax.set_title('{0} Analysis'.format(self.matcher.name))
        ax.set_zlim3d(np.min(Z), np.max(Z))
        fig.colorbar(surf)
        plt.show()
