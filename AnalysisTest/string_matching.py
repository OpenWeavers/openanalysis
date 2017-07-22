from OpenAnalysis.string_matching import StringMatchingAlgorithm, StringMatchingAnalyzer


class BruteForceMatch(StringMatchingAlgorithm):
    """
    Class to implement Brute Force String Matching Algorithm
    """

    def __init__(self):
        StringMatchingAlgorithm.__init__(self, "Brute Force String Matching")

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


class Horspool(StringMatchingAlgorithm):
    def __init__(self):
        StringMatchingAlgorithm.__init__(self, "Hosrpool String Matching")
        self.shift_table = {}
        self.pattern = ''

    def generate_shift_table(self, pattern):
        self.pattern = pattern
        for i in range(0, len(pattern) - 1):
            self.shift_table.update({pattern[i]: len(pattern) - 1 - i})

    def match(self, text: str, pattern: str):
        StringMatchingAlgorithm.match(self, text, pattern)
        self.generate_shift_table(pattern)
        i = len(self.pattern) - 1
        while i < len(text):
            j = 0
            while j < len(self.pattern) and text[i-j] == self.pattern[len(self.pattern)-1-j]:
                j += 1
            self.basic_op += j
            if j == len(self.pattern):
                return i-len(self.pattern)+1
            if text[i] in self.shift_table:
                i += self.shift_table[text[i]]
            else:
                i += len(self.pattern)
        return -1


if __name__ == "__main__":
    StringMatchingAnalyzer(Horspool()).analyze()
