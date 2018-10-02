# M = výška
# N = šířka
# Nejkratsi = M + N - 1
#     bez kosticek: 1, 5, 9
#     s 1 kostickou: 2, 6, 10
#     s 2 kostickama: 3, 7, 11
#     s 3 kostickama: 4, 8, 12
# Nejdelsi:
#     1)  (N * M) - ( M - 1) * (N - 1) / 2
#     2) ((N * M) - (M - 2) * (N - 1) / 2) +
#         1 + int((N - 1) / 4) * 2 + N
#     3) ((N * M) - ((M - 3) * (N - 1) / 2) + ((3 * N) - (2 + int((N - 1) / 4) * 4 + N))
#
#     4) ((N * M) - (M - 4) * (N - 1) / 2) +
#         3 + int((N - 1) / 4) * 6 + N
import os


def jezdi2(M, N, k, kosticek, min_path):
    tamper_with = True
    vyska = M + 1
    pridat = int((k - min_path) / 2)
    stalagmit = False
    with open("output.txt", "a") as output:
        for i in range(1, vyska):
            if i % 2 != 0 and i + kosticek - 1 < M:
                output.write(str("".join(["."] * N)) + "\n")
                continue
            if i % 2 == 0 and i + kosticek - 1 < M:
                l = ["#"] * N
                posun_na = 0
                if tamper_with:
                    posun_na = pridat
                    if posun_na > N - 1:
                        posun_na = N - 1
                    pridat = pridat - posun_na
                l[posun_na] = "."
                tamper_with = not tamper_with
                output.write(str("".join(l)) + "\n")
                continue
            if i + kosticek - 1 >= M:
                mezera_stalagtitu = 2
                mezera_stalagmitu = 0
                row = []
                for a in range(N):
                    mezera_stalagtitu += 1
                    mezera_stalagmitu += 1
                    if mezera_stalagtitu == 4 and pridat > 0 and a + 3 < N:
                        print(a+3)
                        print(N)
                        pridat -= 1
                        mezera_stalagtitu = 0
                        row.append("#")
                    elif mezera_stalagmitu == 4 and stalagmit and a != N - 1:
                        mezera_stalagmitu = 0
                        row.append("#")
                    else:
                        row.append(".")
                output.write(str("".join(row)) + "\n")
                stalagmit = True


def jezdi(M, N, k):
    min_path = M + N - 1
    max_path = 0
    with open("output.txt", "a") as output:
        if min_path > k:
            output.write("Nejde to." + "\n")
            return

        if not ((min_path % 2 == 0 and k % 2 == 0) or (min_path % 2 != 0 and k % 2 != 0)):
            output.write("Nejde to." + "\n")
            return

        sort = M
        while sort > 4:
            sort = sort - 4

        if sort == 1:
            max_path = (N * M) - (M - 1) * (N - 1) / 2
        if sort == 2:
            max_path = (N * M) - (((M - sort) * (N - 1) / 2) + (sort * N) - (sort - 1 + int((N - 1) / 4) * 2 + N))
        if sort == 3:
            max_path = (N * M) - (((M - sort) * (N - 1) / 2) + (sort * N) - (sort - 1 + int((N - 1) / 4) * 4 + N))
        if sort == 4:
            max_path = (N * M) - (((M - sort) * (N - 1) / 2) + (sort * N) - (sort - 1 + int((N - 1) / 4) * 6 + N))

        if k > max_path:
            output.write("Nejde to." + "\n")
            return
    print(sort)
    print(min_path)
    print(max_path)
    jezdi2(M, N, k, sort, min_path)


os.remove("output.txt")
# M = 8
# N = 11
# k = 48
#
# jezdi(M, N, k)
with open("input.txt", "r") as file:
    lines = file.readline()
    for i in range(int(lines)):
        line = file.readline()
        parameters = str(line).split(" ")
        jezdi(int(parameters[0]), int(parameters[1]), int(parameters[2]))
# 2: 2
# 3: 3
# 4: 4
# 5: 7
# 6: 8
# 7: 9
# 8: 10
# 9: 13
# for N in range(1, 10):
# #     # 1 +
# #     kodér = int((N - 1) / 4) * 6 + N
# #     print(str(N) + ": " + str(kodér))





