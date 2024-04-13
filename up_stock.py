from tarot import CardStack, Card
import os


def answer_me(cs: CardStack, ques: str, n: int = 3, forself=True):
    cs.ask(ques, forself)
    cs.shuffle()
    cs.cut()
    return cs.sample(n)


def is_possible(result: list[Card], strict=True):
    cnt = 0
    for c in result:
        if c.get_direct():
            cnt += 1
    if strict:
        return cnt == len(result)
    return cnt > len(result) // 2


def req_digit(cs: CardStack, idx: str):
    for i in range(10):
        an = answer_me(cs, f'它的代码第{idx}位是{i}吗？')
        if is_possible(an):
            return i


def req_shanghai(cs: CardStack):
    a1 = answer_me(cs, '它的代码第二位是8吗？')
    if is_possible(a1):
        print('88', end='', flush=True)
        for i in ('四', '五', '六'):
            d = req_digit(cs, i)
            if d is not None:
                print(d, end='', flush=True)
                continue
            print('..\t搞错了再来！', flush=True)
            return False
    else:
        a1 = answer_me(cs, '它的代码第二位是0吗？')
        if not is_possible(a1):
            return req_shanghai(cs)
        print('0', end='', flush=True)
        for i in ('三', '四', '五', '六'):
            d = req_digit(cs, i)
            if d is not None:
                print(d, end='', flush=True)
                continue
            print('..\t搞错了再来！', flush=True)
            return False
    return True


def req_shenzhen(cs: CardStack):
    a1 = answer_me(cs, '它的代码第一位是3吗？')
    if is_possible(a1):
        print('30', end='', flush=True)
        for i in ('三', '四', '五', '六'):
            d = req_digit(cs, i)
            if d is not None:
                print(d, end='', flush=True)
                continue
            print('..\t搞错了再来！', flush=True)
            return False
    else:
        a1 = answer_me(cs, '它的代码第一位是0吗？')
        if not is_possible(a1):
            return req_shenzhen(cs)
        print('00', end='', flush=True)
        for i in ('三', '四', '五', '六'):
            d = req_digit(cs, i)
            if d is not None:
                print(d, end='', flush=True)
                continue
            print('..\t搞错了再来！', flush=True)
            return False
    return True


def calc(cs: CardStack):
    a1 = answer_me(cs, '明天会涨停的股票在上交所吗？')
    if is_possible(a1):
        print('6', end='', flush=True)
        if req_shanghai(cs):
            print()
            return
        return calc(cs)
    else:
        a1 = answer_me(cs, '明天会涨停的股票在深交所吗？')
        if not is_possible(a1):
            return calc(cs)
        if req_shenzhen(cs):
            print()
            return
        return calc(cs)


def main():
    cs = CardStack()
    calc(cs)


if __name__ == '__main__':
    print('程序正在推衍天机..')
    print('根据推衍结果，明天将会涨停的股票代码为：')
    main()
    os.system('pause')
