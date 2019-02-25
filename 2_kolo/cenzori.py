import time
from multiprocessing import Array, Process


class LPSTree:
    def __init__(self, n):
        self.n = n
        size = 1
        while size < n:
            size *= 2
        size *= 2
        self.tree = [None] * size
        self.tree2 = [None] * size
        self.tree3 = [None] * size
        self.lazyset = [None] * size
        self.lazyadd = [None] * size
        self.nodef = (lambda val, n: val*n)
        self.nodef2 = (lambda val, n: val)
        self.reducef = sum
        self.reducef2 = min
        self.reducef3 = max
        array = [0] * n

        def construct(tree, array, sleft, sright, v):
            if sleft+1 == sright:
                tree[v] = array[sleft]
                return tree[v]
            smid = (sleft + sright) // 2
            tree[v] = self.reducef((construct(tree, array, sleft, smid, 2*v+1),
                    construct(tree, array, smid, sright, 2*v+2)))
            return tree[v]
        construct(self.tree, array, 0, n, 0)
        self.tree2 = self.tree.copy()
        self.tree3 = self.tree.copy()

    def _lazypropagate(self, v, vleft, vright):
        tree = self.tree
        tree2 = self.tree2
        tree3 = self.tree3
        lazyset = self.lazyset
        lazyadd = self.lazyadd
        vmid = (vleft + vright) // 2
        if lazyset[v] is not None:
            tree[2*v+1] = self.nodef(lazyset[v], vmid-vleft)
            tree[2*v+2] = self.nodef(lazyset[v], vright-vmid)
            tree2[2*v+1] = self.nodef2(lazyset[v], vmid-vleft)
            tree2[2*v+2] = self.nodef2(lazyset[v], vright-vmid)
            tree3[2*v+1] = self.nodef2(lazyset[v], vmid-vleft)
            tree3[2*v+2] = self.nodef2(lazyset[v], vright-vmid)
            lazyadd[2*v+1] = lazyadd[2*v+2] = None
            lazyset[2*v+1] = lazyset[2*v+2] = lazyset[v]
            lazyset[v] = None
        if lazyadd[v] is not None:
            tree[2*v+1] += self.nodef(lazyadd[v], vmid-vleft)
            tree[2*v+2] += self.nodef(lazyadd[v], vright-vmid)
            tree2[2*v+1] += self.nodef2(lazyadd[v], vmid-vleft)
            tree2[2*v+2] += self.nodef2(lazyadd[v], vright-vmid)
            tree3[2*v+1] += self.nodef2(lazyadd[v], vmid-vleft)
            tree3[2*v+2] += self.nodef2(lazyadd[v], vright-vmid)
            if lazyadd[2*v+1] is not None:
                lazyadd[2*v+1] += lazyadd[v]
            else:
                lazyadd[2*v+1] = lazyadd[v]
            if lazyadd[2*v+2] is not None:
                lazyadd[2*v+2] += lazyadd[v]
            else:
                lazyadd[2*v+2] = lazyadd[v]
            lazyadd[v] = None

    def get(self, start, stop):
        n = self.n
        tree = self.tree
        tree2 = self.tree2
        tree3 = self.tree3
        gucci = []
        armani = []

        def _get(sleft, sright, v, vleft, vright):
            if sleft>=vright or sright <= vleft:
                return
            if sleft<=vleft and sright >= vright:
                gucci.append(tree2[v])
                armani.append(tree3[v])
                return tree[v]
            vmid = (vleft + vright) // 2
            self._lazypropagate(v, vleft, vright)
            xd = [x for x in (_get(sleft, sright, 2*v+1, vleft, vmid), _get(sleft, sright, 2*v+2, vmid, vright)) if x != None]
            return self.reducef(xd)

        return _get(start, stop, 0, 0, n), min(gucci), max(armani)

    def set(self, start, stop, value):
        n = self.n
        tree = self.tree
        tree2 = self.tree2
        tree3 = self.tree3
        lazyadd = self.lazyadd
        lazyset = self.lazyset

        def _set(sleft, sright, v, vleft, vright, value):
            if sleft >= vright or sright <= vleft:
                return
            if sleft <= vleft and sright >= vright:
                tree[v] = self.nodef(value, vright-vleft)
                tree2[v] = self.nodef2(value, vright-vleft)
                tree3[v] = self.nodef2(value, vright-vleft)
                lazyadd[v] = None
                lazyset[v] = value
                return
            vmid = (vleft + vright) // 2
            self._lazypropagate(v, vleft, vright)
            _set(sleft, sright, 2*v+1, vleft, vmid, value)
            _set(sleft, sright, 2*v+2, vmid, vright, value)
            tree[v] = self.reducef((tree[2*v+1], tree[2*v+2]))
            tree2[v] = self.reducef2((tree2[2*v+1], tree2[2*v+2]))
            tree3[v] = self.reducef3((tree3[2*v+1], tree3[2*v+2]))
        _set(start, stop, 0, 0, n, value)

    def add(self, start, stop, diff):
        n = self.n
        tree = self.tree
        tree2 = self.tree2
        tree3 = self.tree3
        lazyadd = self.lazyadd

        def _add(sleft, sright, v, vleft, vright, diff):
            if sleft >= vright or sright <= vleft:
                return
            if sleft <= vleft and sright >= vright:
                tree[v] += self.nodef(diff, vright-vleft)
                tree2[v] += self.nodef2(diff, vright-vleft)
                tree3[v] += self.nodef2(diff, vright-vleft)
                if lazyadd[v] is not None:
                    lazyadd[v] += diff
                else:
                    lazyadd[v] = diff
                return
            vmid = (vleft + vright) // 2
            self._lazypropagate(v, vleft, vright)
            _add(sleft, sright, 2*v+1, vleft, vmid, diff)
            _add(sleft, sright, 2*v+2, vmid, vright, diff)
            tree[v] = self.reducef((tree[2*v+1], tree[2*v+2]))
            tree2[v] = self.reducef2((tree2[2*v+1], tree2[2*v+2]))
            tree3[v] = self.reducef3((tree3[2*v+1], tree3[2*v+2]))
        _add(start, stop, 0, 0, n, diff)


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
            xorSmalls = (xorSmalls ^ minimum) if xorSmalls is not None else minimum
            xorBigs = (xorBigs ^ maximum) if xorBigs is not None else maximum
            xorSums = (xorSums ^ sumarize) if xorSums is not None else sumarize
        if operationType == 1:
            tree.add(begining, end, add)
        if operationType == 2:
            tree.set(begining, end, add)
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
