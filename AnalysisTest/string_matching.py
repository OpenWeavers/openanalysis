import numpy
import os
import matplotlib.pyplot as plt
from random import randint
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.mlab import griddata


class StringMatchingAlgorithm:
    """
    Base class for all (Comparision Bases) String Matching Algorithms
    """
    s_count = 0  # Number of Successful comparison
    count = 0  # Total Number of comparision
    name = ""  # Name of the String Matching Algorithm
    basic_op = 0

    def __init__(self, name):
        self.name = name

    def match(self, text: str, pattern: str):
        """
        The core matching function
        :param text: Source Text
        :param pattern: String to be matched
        :return: True if pattern in text else False
        Do the exact matching in Derived Classes by calling this function first
        """
        self.s_count, self.count, self.basic_op = 0, 0, 0
        pass


class BruteForceMatch(StringMatchingAlgorithm):
    """
    Class to implement Brute Force String Matching Algorithm
    """

    def __init__(self):
        StringMatchingAlgorithm.__init__(self, "Brute Force Matching")

    def match(self, text: str, pattern: str):
        # can implement __call__ method to use object as function
        """
        class X:
            def __call__(self,params):  # class X is callable now
                print(params)
        y = X()
        y("Hello")
        # O/p: Hello
        """
        StringMatchingAlgorithm.match(self, text, pattern)
        for i in range(0, len(text) - len(pattern)):
            j = 0
            self.count += 1
            while j < len(pattern) and pattern[j] == text[i + j]:
                self.s_count += 1
                j += 1
            self.basic_op += self.s_count
            if j == len(pattern):
                return True
        return False


class StringMatchingAnalyzer:
    """
    Class to analyze the instances of StringMatchingAlgorithm
    """
    max_text_length = 5000
    # max_patt_length = 3000
    txt = ""
    pattern = ""
    # The samples are tar.gz files stored in StringMatchingSamples directory of Current Working
    # Directory. You can download the sample tar.gz texts from the SMART website.
    # https://www.dmi.unict.it/~faro/smart/download/data/
    samples_list = os.listdir("StringMatchingSamples")

    def __init__(self, matcher: StringMatchingAlgorithm):
        self.matcher = matcher
        print(self.samples_list)

    def analyze(self):
        # Analyzes the matching algorithm
        file = open(os.path.join(os.path.abspath('StringMatchingSamples'), self.samples_list[0]), 'r')
        brute_force_match = BruteForceMatch()
        # Select a random text T of size n from any of sample in sample_list
        file_text = file.read()
        data_array = []
        for n in range(1000, 10000, 100):
            for m in range(100, 1000, 5):
                pos = randint(0, len(file_text) - n)
                text = file_text[pos:pos + n]
                pos = randint(0, len(text)-m)
                pattern = text[pos:pos+m]
            # Select a random pattern P of size m from T (you can choose from sample also), where m<n
            # Run the string matching algorithm with T and P as parameters
                brute_force_match.match(text, pattern)
                print(brute_force_match.basic_op)
                data_array.append((n, m, brute_force_match.basic_op))

        dat = numpy.array(data_array)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        x = dat[:, 0]
        y = dat[:, 1]
        z = dat[:, 2]
        xi = numpy.linspace(min(x), max(x))
        yi = numpy.linspace(min(y), max(y))

        X, Y = numpy.meshgrid(xi, yi)
        Z = griddata(x, y, z, xi, yi, interp='linear')
        surf = ax.plot_surface(X, Y, Z, rstride=5, cstride=5, cmap=cm.jet, linewidth=1, antialiased=True)
        ax.set_xlabel('length of text')
        ax.set_ylabel('length of pattern')
        ax.set_zlabel('number of basic operations performed')
        ax.set_title('Brute force String Matching Analysis')
        ax.set_zlim3d(numpy.min(Z), numpy.max(Z))
        fig.colorbar(surf)

        plt.show()
        #plt.plot(x[:, 1][-500:], x[:, 2][-500:])
        #plt.xlabel('length of the pattern')
        #plt.ylabel('number of basic operation')
        #plt.title('constant text length varying pattern length')
        #plt.show()


if __name__ == "__main__":
    StringMatchingAnalyzer(BruteForceMatch()).analyze()
