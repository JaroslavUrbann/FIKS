class Cycle:
    order = 0
    top = 0
    length = 0
    members = []


class Neighbor:
    def __init__(self, node, edge_index, cost):
        self.node = node
        self.edge_index = edge_index
        self.cost = cost


# build the dfs tree and prepare some infomation
def dfs(u):
    global cycle_count
    global _cycle_order
    for i in range(len(neighbors[u])):
        neighbor = neighbors[u][i]
        if visited_edge[neighbor.edge_index]:
            continue
        visited_edge[neighbor.edge_index] = True
        if not parent[neighbor.node]:
            distance_to_parent[neighbor.node] = neighbor.cost
            parent[neighbor.node] = u
            dfs(neighbor.node)
        else:
            # we got a cycle
            cycle_count += 1
            cycle[cycle_count].top = neighbor.node
            cycle[cycle_count].length = neighbor.cost
            distance_to_top[u] = neighbor.cost
            x = u
            while True:
                node_to_cycle_index[x] = cycle_count
                cycle[cycle_count].members = cycle[cycle_count].members + [x]
                if x == neighbor.node:
                    break
                cycle[cycle_count].length += distance_to_parent[x]
                distance_to_top[parent[x]] = distance_to_top[x] + distance_to_parent[x]
                x = parent[x]
    index = node_to_cycle_index[u]
    if index and cycle[index].top == u:
        # if the dfs of cycle index is complete we give it its order
        _cycle_order += 1
        cycle[index].order = _cycle_order


def get_cycle_order(u):
    index = node_to_cycle_index[u]
    if not index:
        return 0
    return cycle[index].order


def distance_same_cycle(u, v):
    index = node_to_cycle_index[u]
    distance = abs(distance_to_top[u] - distance_to_top[v])
    return min(distance, cycle[index].length - distance)


# prepare d[], lca and maxOrder information
def dfs2(u):
    visited[u] = True
    # LCA prep
    f[u][0] = parent[u]
    max_order[u][0] = max(get_cycle_order(u), get_cycle_order(parent[u]))
    for i in range(1, 18):
        f[u][i] = f[f[u][i - 1]][i - 1]
        max_order[u][i] = max(max_order[u][i - 1], max_order[f[u][i - 1]][i - 1])
    for i in range(len(neighbors[u])):
        neighbor = neighbors[u][i]
        if not visited[neighbor.node]:
            index = node_to_cycle_index[neighbor.node]
            if not index or cycle[index].top == neighbor.node:
                d[neighbor.node] = d[u] + neighbor.cost
            else:
                d[neighbor.node] = d[cycle[index].top] + distance_same_cycle(neighbor.node, cycle[index].top)
            depth[neighbor.node] = depth[u] + 1
            dfs2(neighbor.node)


def lca(u, v):
    if depth[u] > depth[v]:
        return lca(v, u)
    i = 17
    while i >= 0:
        if depth[f[v][i]] >= depth[u]:
            v = f[v][i]
        i -= 1
    if u == v:
        return u
    i = 17
    while i >= 0:
        if f[u][i] != f[v][i]:
            u = f[u][i]
            v = f[v][i]
        i -= 1
    return parent[u]


def distance_top_down(ancestor, u):
    index = node_to_cycle_index[ancestor]
    road = []

    def _distance_same_cycle(u, v):
        index = node_to_cycle_index[u]
        distance = distance_to_top[u] - distance_to_top[v]
        distance_2 = cycle[index].length - distance
        if distance > distance_2:
            x = cycle[index].members.index(v)
            while cycle[index].members[x] != u:
                road.append(cycle[index].members[x])
                x -= 1
            return distance_2
        x = v
        while x != u:
            road.append(x)
            x = parent[x]
        return distance

    # if ancestor does not belong to any cycle
    if not index:
        x = u
        while x != ancestor:
            road.append(x)
            x = parent[x]
        return d[u] - d[ancestor], road
    # if two vertices is in the same cycle
    if index == node_to_cycle_index[u]:
        return _distance_same_cycle(ancestor, u), road
    # we find b as the vertex in cycle index that is closest to u
    b = u
    i = 17
    while i >= 0:
        if max_order[b][i] < cycle[index].order:
            b = f[b][i]
        i -= 1
    b = parent[b]
    x = u
    road_2 = []
    while x != b:
        road_2.append(x)
        x = parent[x]
    dist = d[u] - d[b] + _distance_same_cycle(ancestor, b)
    return dist, road_2 + road


def calc(u, v):
    r = lca(u, v)
    dist, path = distance_top_down(r, u)
    dist_2, path_2 = distance_top_down(r, v)
    print(dist + dist_2)
    xd = [u]
    for i in range(len(path)):
        xd.append(path_2[i])
    x = len(path_2) - 1
    while x >= 0:
        xd.append(path_2[x])
        x -= 1
    print(xd)


if __name__ == "__main__":
    # n = 9
    # k = 12
    # q = 3
    # u = [1, 1, 1, 8, 8, 8, 2, 2, 3, 4, 4, 5]
    # v = [8, 2, 3, 6, 7, 2, 4, 3, 4, 7, 5, 6]
    # c = [2, 4, 7, 3, 14, 1, 9, 5, 1, 8, 6, 2]
    # _u = [1, 3, 1]
    # _v = [7, 5, 3]

    u = [1,1,2,3,4,4,5,6]
    v = [2,3,3,4,5,7,6,7]
    c = [2,4,1,1,1,1,2,1]
    _u = [1]
    _v = [6]
    n = max(max(u), max(v))
    k = len(u)
    q = len(_u)

    n += 1
    neighbors = [[] for x in range(n)]
    cycle = [Cycle() for _ in range(n)]
    parent = [0] * n
    node_to_cycle_index = [0] * n
    d = [0] * n
    depth = [0] * n
    max_order = [[0] * 20 for _ in range(n)]
    f = [[0] * 20 for _ in range(n)]
    visited = [False] * n
    distance_to_top = [0] * n
    distance_to_parent = [0] * n
    visited_edge = [False] * n**2
    cycle_count = 0
    _cycle_order = 0

    for i in range(k):
        neighbors[u[i]].append(Neighbor(v[i], i, c[i]))
        neighbors[v[i]].append(Neighbor(u[i], i, c[i]))

    parent[1] = 1
    dfs(1)
    dfs2(1)
    for i in range(q):
        calc(_u[i], _v[i])
    print(cycle[1].members)
    print(cycle[2].members)
