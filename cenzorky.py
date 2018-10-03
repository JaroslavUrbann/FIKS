import math
import random

l = random.sample(range(100), 10)


def SearchTable(l, mintable, maxtable, parity, a, b):
    o = b - a + 1
    k = math.floor(math.log(o, 2))
    moveby = o - 2 ** k
    if l[maxtable[k][a]] > l[maxtable[k][a + moveby]]:
        return min(l[mintable[k][a]], l[mintable[k][a + moveby]]), maxtable[k][a], parity[a] ^ parity[b + 1]
    else:
        return min(l[mintable[k][a]], l[mintable[k][a + moveby]]), maxtable[k][a + moveby], parity[a] ^ parity[b + 1]


def CreateTable(l):
    avariable = True
    mintable = []
    maxtable = []
    parity = [0]
    countparity = True
    j = 0
    x = 0
    y = 0
    i = 0
    while avariable:
        width = 2**j
        mintable.append([])
        maxtable.append([])
        while i + width <= len(l):
            mini = l.index(min(l[i:i + width]))
            maxi = l.index(max(l[i:i + width]))
            mintable[x].append(mini)
            maxtable[x].append(maxi)
            if countparity and i < len(l):
                parity.append(l[i] ^ parity[i])
            i += 1
            y += 1
        # if countparity:
        #     parity.append(0)
        countparity = False
        x += 1
        j += 1
        i = 0
        y = 0
        if width + width > len(l):
            avariable = False
    return mintable, maxtable, parity


print(l)
mintable, maxtable, parity = CreateTable(l)
minimum, maximum, par = SearchTable(l, mintable, maxtable, parity, 6, 9)
print(maximum)


# with open("input.txt", "r") as input, open("output.txt", "w") as output:
#     tasks = int(input.readline())
#     for i in range(tasks):
#         line = input.readline().split(" ")
#         n_requests = int(line[1])
#         cenzorky = list(map(int, input.readline().split(" ")))
#         mintable, maxtable, parity = CreateTable(cenzorky)
#         for a in range(n_requests):
#             line2 = input.readline().split(" ")
#             minimum, maximum, par = SearchTable(cenzorky, mintable, maxtable, parity, int(line2[0]), int(line2[1]))
#             output.write(str(int(minimum)))
#             output.write(str(int(maximum)))
#             output.write(str(int(par)) + "\n")
#         print(str(tasks - i))

