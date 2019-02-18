from __future__ import division


class LPSTree:
    def __init__(self, n, value=None, reducef=None, modulo=None):
        if n <= 0:
            raise ValueError("n most be greater than 0")
        self.n = n
        size = 1
        while(size < n):
            size *= 2
        size *= 2
        self.size = size
        self.tree = [None] * size
        self.tree2 = [None] * size
        self.tree3 = [None] * size
        self.boolset = [False] * size
        self.booladd = [False] * size
        self.lazyset = [None] * size
        self.lazyadd = [None] * size
        self.modulo = modulo
        if not reducef:
            reducef = sum
        if reducef == sum:
            self.nodef = (lambda val, n: val*n)
            self.nodef2 = (lambda val, n: val)
            self.reducef = reducef
            self.reducef2 = min
            self.reducef3 = max
        if value != None:
            array = [value] * n
        else:
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

        # def construct2(tree, array, sleft, sright, v):
        #     if sleft+1 == sright:
        #         tree[v] = array[sleft]
        #         return tree[v]
        #     smid = (sleft + sright) // 2
        #     tree[v] = self.reducef2((construct(tree, array, sleft, smid, 2*v+1),
        #             construct(tree, array, smid, sright, 2*v+2)))
        #     return tree[v]
        # construct2(self.tree2, array, 0, n, 0)
        #
        # def construct3(tree, array, sleft, sright, v):
        #     if sleft+1 == sright:
        #         tree[v] = array[sleft]
        #         return tree[v]
        #     smid = (sleft + sright) // 2
        #     tree[v] = self.reducef3((construct(tree, array, sleft, smid, 2*v+1),
        #             construct(tree, array, smid, sright, 2*v+2)))
        #     return tree[v]
        # construct3(self.tree3, array, 0, n, 0)

    def __len__(self):
        return self.n

    def _lazypropagate(self, v, vleft, vright):
        tree = self.tree
        tree2 = self.tree2
        tree3 = self.tree3
        boolset = self.boolset
        booladd = self.booladd
        lazyset = self.lazyset
        lazyadd = self.lazyadd
        vmid = (vleft + vright) // 2
        if boolset[v]:
            tree[2*v+1] = self.nodef(lazyset[v], vmid-vleft)
            tree[2*v+2] = self.nodef(lazyset[v], vright-vmid)
            tree2[2*v+1] = self.nodef2(lazyset[v], vmid-vleft)
            tree2[2*v+2] = self.nodef2(lazyset[v], vright-vmid)
            tree3[2*v+1] = self.nodef2(lazyset[v], vmid-vleft)
            tree3[2*v+2] = self.nodef2(lazyset[v], vright-vmid)
            boolset[2*v+1] = boolset[2*v+2] = True
            booladd[2*v+1] = booladd[2*v+2] = False
            lazyset[2*v+1] = lazyset[2*v+2] = lazyset[v]
            boolset[v] = False
        if booladd[v]:
            tree[2*v+1] += self.nodef(lazyadd[v], vmid-vleft)
            tree[2*v+2] += self.nodef(lazyadd[v], vright-vmid)
            tree2[2*v+1] += self.nodef2(lazyadd[v], vmid-vleft)
            tree2[2*v+2] += self.nodef2(lazyadd[v], vright-vmid)
            tree3[2*v+1] += self.nodef2(lazyadd[v], vmid-vleft)
            tree3[2*v+2] += self.nodef2(lazyadd[v], vright-vmid)
            if booladd[2*v+1]:
                lazyadd[2*v+1] += lazyadd[v]
            else:
                booladd[2*v+1] = True
                lazyadd[2*v+1] = lazyadd[v]
            if booladd[2*v+2]:
                lazyadd[2*v+2] += lazyadd[v]
            else:
                booladd[2*v+2] = True
                lazyadd[2*v+2] = lazyadd[v]
            booladd[v] = False

    def get(self, start, stop, what):
        n = self.n
        if not(start < stop and start >=0 and stop <= n):
            raise IndexError(start, stop)
        tree = self.tree
        tree2 = self.tree2
        tree3 = self.tree3

        def _get(sleft, sright, v, vleft, vright):
            if sleft>=vright or sright <= vleft:
                return
            if sleft<=vleft and sright >= vright:
                return tree[v]
            vmid = (vleft + vright) // 2
            self._lazypropagate(v, vleft, vright)
            return self.reducef([x for x in
                                (_get(sleft, sright, 2*v+1, vleft, vmid),
                                _get(sleft, sright, 2*v+2, vmid, vright))
                                if x != None])

        def _get2(sleft, sright, v, vleft, vright):
            if sleft>=vright or sright <= vleft:
                return
            if sleft<=vleft and sright >= vright:
                return tree2[v]
            vmid = (vleft + vright) // 2
            # self._lazypropagate(v, vleft, vright)
            return self.reducef2([x for x in
                                (_get2(sleft, sright, 2*v+1, vleft, vmid),
                                _get2(sleft, sright, 2*v+2, vmid, vright))
                                if x != None])

        def _get3(sleft, sright, v, vleft, vright):
            if sleft>=vright or sright <= vleft:
                return
            if sleft<=vleft and sright >= vright:
                return tree3[v]
            vmid = (vleft + vright) // 2
            # self._lazypropagate(v, vleft, vright)
            return self.reducef3([x for x in
                                (_get3(sleft, sright, 2*v+1, vleft, vmid),
                                _get3(sleft, sright, 2*v+2, vmid, vright))
                                if x != None])

        if what == sum:
            return _get(start, stop, 0, 0, n)
        if what == min:
            return _get2(start, stop, 0, 0, n)
        if what == max:
            return _get3(start, stop, 0, 0, n)

    def set(self, start, stop, value):
        n = self.n
        if not(start < stop and start >=0 and stop <= n):
            raise IndexError(start, stop)
        tree = self.tree
        tree2 = self.tree2
        tree3 = self.tree3
        boolset = self.boolset
        booladd = self.booladd
        lazyset = self.lazyset
        lazyadd = self.lazyadd
        def _set(sleft, sright, v, vleft, vright, value):
            # print v, start, stop, vleft, vright, value, tree
            if sleft >= vright or sright <= vleft:
                return
            if sleft <= vleft and sright >= vright:
                tree[v] = self.nodef(value, vright-vleft)
                tree2[v] = self.nodef2(value, vright-vleft)
                tree3[v] = self.nodef2(value, vright-vleft)
                if self.modulo:
                    tree[v] %= self.modulo
                boolset[v] = True
                booladd[v] = False
                lazyset[v] = value
                # print v, tree, tree[v], tree[v] % self.modulo
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
        if not(start < stop and start >=0 and stop <= n):
            raise IndexError(start, stop)
        tree = self.tree
        tree2 = self.tree2
        tree3 = self.tree3
        boolset = self.boolset
        booladd = self.booladd
        lazyset = self.lazyset
        lazyadd = self.lazyadd
        def _add(sleft, sright, v, vleft, vright, diff):
            if sleft >= vright or sright <= vleft:
                return
            if sleft <= vleft and sright >= vright:
                tree[v] += self.nodef(diff, vright-vleft)
                tree2[v] += self.nodef2(diff, vright-vleft)
                tree3[v] += self.nodef2(diff, vright-vleft)
                if self.modulo:
                    tree[v] %= self.modulo
                if booladd[v]:
                    lazyadd[v] += diff
                else:
                    booladd[v] = True
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