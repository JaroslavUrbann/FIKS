from leon import *
import time
from multiprocessing import Process, Value, Array


class Handler:
    def __init__(self, a, b, x0):
        self.a  = a
        self.b  = b
        self.x = x0

    def nextInt(self):
        self.x = ((self.x * self.a + self.b) % 1000000007)
        return self.x


def do_the_sada(n, params, answers):
    operationCount = int(params[0])
    arrayLenght = int(params[1])
    a = int(params[2])
    b = int(params[3])
    x0 = int(params[4])
    handler = Handler(a, b, x0)
    tree = LPSTree(arrayLenght)
    xorSmalls = None
    xorBigs = None
    xorSums = None
    for operation in range(operationCount):
        operationType = handler.nextInt() % 3
        begining = handler.nextInt() % arrayLenght
        end = handler.nextInt() % arrayLenght
        if begining > end:
            b = end
            end = begining
            begining = b
        add = handler.nextInt() % arrayLenght

        end += 1
        if (operationType == 0):
            sumarize, minimum, maximum = tree.get(begining, end)
            # print("search")
            # print(begining, end)
            # print(sumarize)
            # print(tree.tree)
            xorSmalls = (xorSmalls ^ minimum) if xorSmalls is not None else minimum
            xorBigs = (xorBigs ^ maximum) if xorBigs is not None else maximum
            xorSums = (xorSums ^ sumarize) if xorSums is not None else sumarize
        if operationType == 1:
            tree.add(begining, end, add)
            # print("add")
            # print(begining, end, add)
            # print(tree.tree)
        if operationType == 2:
            tree.set(begining, end, add)
            # print("set")
            # print(begining, end, add)
            # print(tree.tree)
    answers[n*3] = xorSmalls if xorSmalls is not None else 0
    answers[n*3+1] = xorBigs if xorBigs is not None else 0
    answers[n*3+2] = xorSums if xorSums is not None else 0


if __name__ == '__main__':
    tim = time.time()
    with open("input.txt", "r") as input_file:
        with open("output.txt", "w") as output_file:
            sets = int(input_file.readline())
            answers = Array('d', [0] * sets * 3)
            params_list = []
            for s in range(sets):
                params_list.append(input_file.readline().split())
                if int(params_list[s][0]) > 900000:
                    xd = Process(target=do_the_sada, args=(s, params_list[s], answers,))
                    xd.start()
                    print("started that boi")

            for a in range(len(params_list)):
                if int(params_list[a][0]) > 900000:
                    continue
                do_the_sada(a, params_list[a], answers)
                print(a)
            try:
                xd.join()
            except:
                print("lolec díkes")
            print(answers)
            for i in range(len(answers)):
                output_file.write(str(int(answers[i])) + '\n')
    print(time.time() - tim)
