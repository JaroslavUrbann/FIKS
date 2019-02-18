from segment_tree import *
from leon import *
from random import randint
import time
from threading import Thread


# def do_this():
#     arr = [1, 2]
#     for i in range(10**6):
#         arr.append(randint(0, 10**9))
#     print(len(arr))
#     array = [3, 1, 5, 3, 13, 7, 2, 7, 2]
#     tree = SegmentTree(arr)
#
#     for i in range(int(10**6 / 3)):
#         xd = tree.query(0, 1, "sum")
#     print("sum")
#     for i in range(int(10**6 / 3)):
#         xd = tree.query(0, 1, "min")
#     print("min")
#     for i in range(int(10**6 / 3)):
#         xd = tree.query(0, 1, "max")
#     print("max")
#     for i in range(int(10**6 / 3)):
#         xd = tree.update_range(0, 1000000, randint(0, 10**9))
#     print("add")
#     for i in range(int(10**6 / 3)):
#         xd = tree.update_range(0, 1000000, randint(0, 10**9))
#
#
# tim = time.time()
# d = Thread(name='daemon', target=do_this)
# d.setDaemon(True)
# d.start()
#
# do_this()
# d.join()
# print(time.time() - tim)

def do_this():

    # tree = LPSTree(5)
    # tree.set(0, 2, 7)
    # tree.add(1, 2, 4)
    # tree.set(2, 3, 5)
    # print(tree.tree)
    # print(tree.tree2)
    # print(tree.tree3)
    # print(tree.get(0, 5, sum))
    # print(tree.get(0, 5, min))
    # print(tree.get(0, 5, max))

    tree = LPSTree(10**6)
    for i in range(int(10**6 / 3)):
        xd = tree.set(0, randint(1, 10**6), randint(1, 10**6))
        xd = tree.add(0, randint(1, 10**6), randint(1, 10**6))
        xd = tree.get(0, 5, sum)
        xd = tree.get(0, 5, max)
        xd = tree.get(0, 5, min)


tim = time.time()
do_this()
print(time.time() - tim)
