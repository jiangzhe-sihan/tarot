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


def parse_stack(stack: list[Card]):
    cnt = 0
    for i in stack:
        if i.get_direct():
            cnt += 1
    return cnt > len(stack) // 2


class CardStack:
    def __init__(self):
        self._inter = []
        for i in range(78):
            self._inter.append(Card(i))
        random.shuffle(self._inter)
        self._reverse(self._inter)
        self._for_self = False
        self._stop = False

    def ask(self, question='', for_self=False):
        if not question.strip():
            random.seed(time.time_ns())
        else:
            random.seed(question)
        self._for_self = for_self
        self._stop = False

    def stop(self):
        self._stop = True

    @staticmethod
    def _reverse(li_cds):
        sli = random.sample(li_cds, random.randint(0, len(li_cds)))
        for c in sli:
            c.reverse()

    def shuffle(self):
        for i in range(randint()):
            if self._stop:
                break
            a = random.randint(1, 77)
            b = random.randint(a, 78)
            s1 = self._inter[:a]
            self._reverse(s1)
            s2 = self._inter[a:b]
            self._reverse(s2)
            s3 = self._inter[b:]
            self._reverse(s3)
            s2.extend(s1)
            s2.extend(s3)
            self._inter = s2
            self._inter.reverse()
            random.shuffle(self._inter)

    def cut(self):
        if self._stop:
            return
        a = random.randint(1, 77)
        s = self._inter[:a]
        s1 = self._inter[a:]
        b = random.randint(0, a - 1)
        s3 = s[:b]
        s2 = s[b:]
        s1.extend(s2)
        s1.extend(s3)
        self._inter = s1
        if not self._for_self:
            return
        for c in self._inter:
            c.reverse()

    def sample(self, n):
        return random.sample(self._inter, n) if not self._stop else None

    def answer(self, question, n, for_self=False):
        self.ask(question, for_self)
        self.shuffle()
        self.cut()
        return self.sample(n)


if __name__ == '__main__':
    cs = CardStack()
    cs.shuffle()
    cs.cut()
    li = cs.sample(3)
    for cd in li:
        print(cd.get_id(), cd.get_direct())
