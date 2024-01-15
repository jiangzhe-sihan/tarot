import random
import time


def randint():
    s = random.random().hex()
    s = s.split('.')[1]
    t = s.split('p')
    res = int(float.fromhex(t[0]))
    return res >> 32


class Card:
    def __init__(self, _id):
        self._id = _id
        self._dir = True

    def get_id(self):
        return self._id

    def get_direct(self):
        return self._dir

    def reverse(self):
        self._dir = not self._dir


class CardStack:
    def __init__(self):
        self._inter = []
        for i in range(78):
            self._inter.append(Card(i))
        random.shuffle(self._inter)

    @staticmethod
    def ask(question=''):
        if not question.strip():
            random.seed(time.time_ns())
        else:
            random.seed(question)

    def shuffle(self):
        for i in range(randint()):
            a = random.randint(1, 77)
            b = random.randint(a, 78)
            s1 = self._inter[:a]
            s2 = self._inter[a:b]
            s3 = self._inter[b:]
            s2.extend(s1)
            s2.extend(s3)
            self._inter = s2
        for i in range(randint()):
            self._inter.reverse()
            random.shuffle(self._inter)
            for j in range(78):
                c = random.choice(self._inter)
                c.reverse()

    def cut(self):
        a = random.randint(0, 77)
        s = self._inter[:a]
        s1 = self._inter[a:]
        b = random.randint(0, a - 1)
        s3 = s[:b]
        s2 = s[b:]
        s1.extend(s2)
        s1.extend(s3)
        self._inter = s1
        for c in self._inter:
            c.reverse()

    def sample(self, n):
        return random.sample(self._inter, n)


if __name__ == '__main__':
    cs = CardStack()
    cs.shuffle()
    cs.cut()
    li = cs.sample(3)
    for cd in li:
        print(cd.get_id(), cd.get_direct())
