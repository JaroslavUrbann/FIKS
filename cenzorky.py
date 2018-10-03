import random
import math

l = random.sample(range(100), 10)


def SearchTable(l, mintable, maxtable, parity, a, b):
    o = b - a + 1
    k = math.floor(math.log(o, 2))
    moveby = o - 2 ** k
    if l[maxtable[k][a]] > l[maxtable[k][a + moveby]]:
        return min(l[mintable[k][a]], l[mintable[k][a + moveby]]), maxtable[k][a], parity[a - 1] ^ parity[b]
    else:
        return min(l[mintable[k][a]], l[mintable[k][a + moveby]]), maxtable[k][a + moveby], parity[a - 1] ^ parity[b]


def CreateTable(l):
    avariable = True
    mintable = []
    maxtable = []
    parity = [l[0]]
    countparity = True
    j = 0
    x = 0
    y = 0
    i = 0
    while avariable:
        width = 2**j
        mintable.append([])
        maxtable.append([])
        while i + width < len(l):
            mini = l.index(min(l[i:i + width]))
            maxi = l.index(max(l[i:i + width]))
            mintable[x].append(mini)
            maxtable[x].append(maxi)
            if countparity and i < len(l) - 1:
                parity.append(l[i + 1] ^ parity[i])
            i += 1
            y += 1
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
print(parity)
print(l[1]^l[0])
print(parity[0]^parity[1])
print(SearchTable(l, mintable, maxtable, parity, 0, 2))
# result = []
# al = 0
# for x in l:
#     al ^= x
#     result.append(al)
    # print(al)

# print("-----")
# print(12^13^11)
# print(1^11)
# XOR done
# Range minimum query
# asi taky
# with open("input.txt", "r") as file:
#     tasks = file.readline()
#     for i in range(int(tasks)):
#         line = file.readline().split(" ")
#         n_cenzorek = int(line[0])
#         n_requests = int(line[1])
#         cenzorky = file.readline().split(" ")
#         for a in range(n_requests):
#             doShit()
# | 001011  1
# | 000100  1
# | 011010  1
# | 101000  0
# |   0
# |   0
# |   0
# |   1
