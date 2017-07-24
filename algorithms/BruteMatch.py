
class BruteMatch:
    pos = -1

    def __init__(self, text,  p):
        for i in range(0, len(text)- len(p) + 1):
            flag = 1
            for j in range(0, len(p)):
                if p[j] != text[i + j]:
                    flag = 0
                    break
            if flag == 1:
                self.pos = i

if __name__ == '__main__':
    b = BruteMatch(input("Enter text:\n"), input("Enter pattern:\n"))
    if b.pos >= 0:
        print("Pattern found at position ", b.pos)
    else:
        print("Pattern not found")
