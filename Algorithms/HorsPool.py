class HorsPool:
    t = {}

    def __init__(self, s):
        self.p = s
        for i in range(0, len(s)-1):
            self.t.update({s[i]: len(s) - 1 - i})

    def search(self, text):
        i = len(self.p) - 1
        while i < len(text):
            j = 0
            while j<len(self.p) and text[i-j] == self.p[len(self.p)-1-j]:
                j += 1
            if j == len(self.p):
                return i-len(self.p)+1
            if text[i] in self.t:
                i += self.t[text[i]]
            else:
                i += len(self.p)
        return -1

if __name__ == '__main__':
    h = HorsPool(raw_input("Enter pattern:\n"))
    pos = h.search(raw_input("Enter text:\n"))
    if pos >= 0:
        print "Pattern found at position ", pos
    else:
        print "Pattern not found"
