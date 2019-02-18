from leon import *
import time

class Handler:
    def __init__(self, a, b, x0):
        self.a  = a
        self.b  = b
        self.x = x0

    def nextInt(self):
        self.x = ((self.x * self.a + self.b) % 1000000007)
        return self.x

tim = time.time()
with open("input.txt", "r") as input_file:
    with open("output.txt", "w") as output_file:
        sets = int(input_file.readline())

        for s in range(sets):
            params          = input_file.readline().split()
            operationCount  = int(params[0])
            arrayLenght     = int(params[1])
            a               = int(params[2])
            b               = int(params[3])
            x0              = int(params[4])

            handler = Handler(a, b, x0)

            tree = LPSTree(arrayLenght)

            xorSmalls = 0
            xorBigs = 0
            xorSums = 0

            for operation in range(operationCount):
                    operationType   = handler.nextInt() % 3
                    begining        = handler.nextInt() % arrayLenght
                    end             = handler.nextInt() % arrayLenght
                    if begining > end:
                        b           = end
                        end         = begining
                        begining    = b
                    add             = handler.nextInt() % arrayLenght

                    end += 1
                    if(operationType == 0):
                            sumarize = int(tree.get(begining, end, sum))
                            minimum = int(tree.get(begining, end, min))
                            maximum = int(tree.get(begining, end, max))
                            xorSmalls = xorSmalls ^ minimum
                            xorBigs = xorBigs ^ maximum
                            xorSums = xorSums ^ sumarize
                    if operationType == 1:
                        tree.add(begining, end, add)
                    else:
                        tree.set(begining, end, add)
            output_file.write(str(xorSmalls) + '\n')
            output_file.write(str(xorBigs) + "\n")
            output_file.write(str(xorSums) + '\n')
            print('set ' + str(s) + ' / ' + str(sets) +' completed')
        print('done')
print(time.time() - tim)
