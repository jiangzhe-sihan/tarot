from tarot import CardStack
import shelve

cs = CardStack()
cs.ask('今天是不是星期天？', False)
cs.shuffle()
cs.cut()
res = cs.sample(3)
with shelve.open('./desc/zh_CN') as rec:
    for c in res:
        t = rec[str(c.get_id())]
        print(t['name'], '顺位' if c.get_direct() else '逆位')
    for c in res:
        t = rec[str(c.get_id())]
        print(t['name'], c.get_direct())
        print('\ndesc')
        print(t['desc'])
        print('\ntrue')
        print(t['true'])
        print('\nfalse')
        print(t['false'])
        print()

# import os
# os.system('pause')
