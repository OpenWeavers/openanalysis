from OpenAnalysis.string_matching import  StringMatchingAlgorithm, StringVisualizer


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
