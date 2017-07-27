from openanalysis.string_matching import StringMatchingAlgorithm, StringMatchingAnalyzer


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
            while j < len(pattern) and pattern[j] == text[i + j]:
                j += 1
                self.count += 1
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
            self.count += j
            if j == len(self.pattern):
                return i-len(self.pattern)+1
            if text[i] in self.shift_table:
                i += self.shift_table[text[i]]
            else:
                i += len(self.pattern)
        return -1
    

class BoyerMoore(StringMatchingAlgorithm):
	def __init__(self):
		StringMatchingAlgorithm.__init__(self, "Boyer-Moore String Matching")
		self.gdsuf_shift_table = []
		self.bdsym_shift_table = {}
		self.pattern = ''

	def generate_bdsym_shift_table(self, pattern):
		self.pattern = pattern
		for i in range(len(pattern) - 1):
			self.bdsym_shift_table[pattern[i]] = len(pattern) - i - 1
		
	def generate_gdsuf_shift_table(self, pattern):
		lp = len(pattern)
		for i in range(lp-1):
			suff = pattern[lp-i-1:]
			# find highest index where suffix 'suff' is present in pattern
			targ = pattern.rfind(suff, 0, lp-i-1)
			while pattern[targ-1] == pattern[lp-i-2] and targ > 0:
				targ = pattern.rfind(suff, 0, targ)
			if targ > 0:
				self.gdsuf_shift_table.append((lp-i-1) - targ)
			elif targ == 0:
				self.gdsuf_shift_table.append(lp-i-1)
			else:
				lis = []
				# find first and last pre and suff that should match, then append distance b/w them
				for j in range(lp-1, lp-i-2,-1):
					if pattern[j:] == pattern[0:lp-j]:
						lis.append(j)
				if len(lis) == 0:
					self.gdsuf_shift_table.append(lp)
				else:
					self.gdsuf_shift_table.append(max(lis))

	def match(self, text: str, pattern: str):
		StringMatchingAlgorithm.match(self, text, pattern)
		# pattern = "BAOBAB"
		self.generate_bdsym_shift_table(pattern)
		self.generate_gdsuf_shift_table(pattern)
		# print(self.gdsuf_shift_table, self.bdsym_shift_table)
		i = len(self.pattern) - 1
		while i < len(text):
			j = 0
			k = 0	# matched characters
			while j < len(self.pattern) and text[i-j] == self.pattern[len(self.pattern)-j-1]:
				j += 1
				k += 1
			self.count += j
			if j == len(self.pattern):
				return i-len(self.pattern)+1
			if text[i-j] in self.bdsym_shift_table:
				t1 = self.bdsym_shift_table[text[i-j]]
			else:
				t1 = len(self.pattern)
			d1 = max(t1 - k, 1)
			d = d1
			if k > 0:
				d2 = self.gdsuf_shift_table[k-1]	# 0 based index table
				d = max(d1, d2)
			i += d
		return -1


if __name__ == "__main__":
    StringMatchingAnalyzer(BoyerMoore).analyze()
