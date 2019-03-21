import sys
sys.setrecursionlimit(10000)


class Center:
    number = 0
    paths = []
    poisoned = False


def binary_search(low, high, nodes):
    while low <= high:
        mid = int((low + high) / 2)
        gets_poisoned = gets_poisoned_(mid, nodes)
        if mid == 1 and gets_poisoned:
            return 0
        if mid == high and not gets_poisoned:
            return -1
        previous_gets_poisoned = gets_poisoned_(mid-1, nodes)
        if gets_poisoned and not previous_gets_poisoned:
            return mid - 1
        elif gets_poisoned:
            high = mid - 1
        else:
            low = mid + 1


def gets_poisoned_(q, nodes):
    node = nodes[0]
    global got_poisoned
    global nodes_visited
    got_poisoned = False
    nodes_visited = [False] * len(nodes)

    def _probe_the_node(node):
        global got_poisoned
        global nodes_visited
        print(nodes_visited.count(False), nodes_visited.count(True))
        nodes_visited[node.number] = True
        if node.poisoned or got_poisoned:
            got_poisoned = True
            return
        for i in range(min(q, len(node.paths))):
            # print(node.number, nodes_visited[node.number])
            if nodes_visited[node.paths[i]]:
                continue
            _probe_the_node(nodes[node.paths[i]])

    _probe_the_node(node)
    return got_poisoned


centers = []
max_paths = 0

with open("input.txt") as input:
    n_lines = int(input.readline())
    for i in range(n_lines):
        xd = input.readline()
        whatever = list(map(int, input.readline().split()))
        n_centers = whatever[0]
        n_poisoned = whatever[1]
        poisoned_centers = list(map(int, input.readline().split()))
        for x in range(n_centers):
            node = Center()
            node.number = x
            node.paths = list(map(int, input.readline().split()))[1:]
            node.poisoned = bool(x in poisoned_centers)
            centers.append(node)
            max_paths = max(max_paths, len(node.paths))
        if i > 17:
            print(i)
            print(binary_search(1, max_paths, centers))
        max_paths = 0
        centers = []
