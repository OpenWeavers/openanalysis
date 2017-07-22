class Horspool:
    def __init__(self):
        self.shift_table = {}
        self.pattern = ''

    def generate_shift_table(self, pattern):
        self.pattern = pattern
        for i in range(0, len(pattern) - 1):
            self.shift_table.update({pattern[i]: len(pattern) - 1 - i})

    def match(self, text, pattern):
        self.generate_shift_table(pattern)
        i = len(self.pattern) - 1
        while i < len(text):
            j = 0
            while j < len(self.pattern) and text[i-j] == self.pattern[len(self.pattern)-1-j]:
                j += 1
            if j == len(self.pattern):
                return i-len(self.pattern)+1
            if text[i] in self.shift_table:
                i += self.shift_table[text[i]]
            else:
                i += len(self.pattern)
        return -1

if __name__ == '__main__':
    h = Horspool()
    pos = h.match(input("Enter text:\n"), input("Enter pattern:\n"))
    if pos >= 0:
        print('Pattern found at position', pos)
    else:
        print("Pattern not found")
