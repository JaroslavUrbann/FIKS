l = []
for i in range(15):
    l.append(i)

result = []
al = 0
for x in l:
    al ^= x
    result.append(al)
    print(al)

print("-----")
print(12^13^11)
print(1^11)
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
