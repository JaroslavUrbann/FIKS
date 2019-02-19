from leon import *
from random import randint
import time
from multiprocessing import Array


def do_this():

    tree = LPSTree(4)
    tree.set(0, 2, 23662758185)
    tree.add(1, 2, 23662758185)
    # tree.set(2, 4, 5)
    print(tree.tree)
    print(tree.tree2)
    print(tree.tree3)
    print(tree.get(0, 5))

    # tree = LPSTree(10**6)
    # for i in range(int(10**6 / 3)):
    #     xd = tree.set(0, randint(1, 10**6), randint(1, 10**6))
    #     xd = tree.add(0, randint(1, 10**6), randint(1, 10**6))
    #     xd = tree.get(0, 5, sum)
    #     xd = tree.get(0, 5, max)
    #     xd = tree.get(0, 5, min)
    return

tim = time.time()
do_this()
print(time.time() - tim)
import sys
xd = 217764957751
print(type(xd))
print(xd ^ 212764957751)
answers = Array('d', 1)
answers[0] = xd
print(answers[0])