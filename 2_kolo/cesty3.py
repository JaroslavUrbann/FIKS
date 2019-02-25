class Cycle:
    order = 0
    top = 0
    length = 0
    first_member = 0


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
            cycle[cycle_count].first_member = u
            distance_to_top[u] = neighbor.cost
            x = u
            while True:
                node_to_cycle_index[x] = cycle_count
                if x == neighbor.node:
                    break
                cycle[cycle_count].length = max(distance_to_parent[x], cycle[cycle_count].length)
                distance_to_top[parent[x]] = max(distance_to_top[x], distance_to_parent[x])
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


def distance_same_cycle(u, top, neighbor):
    if distance_to_top[top] > distance_to_top[u]:
        xd = []
        x = cycle[node_to_cycle_index[neighbor.node]].first_member
        xd.append([distance_to_top[x], x])
        while x != u:
            xd.append([distance_to_parent[x], parent[x]])
            x = parent[x]
        return d[top] + xd
    else:
        return d[parent[u]] + [[neighbor.cost, neighbor.node]]


# prepare d[], lca and maxOrder information
def dfs2(u):
    visited[u] = True
    print(u)
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
                d[neighbor.node] = d[u] + [[neighbor.cost, neighbor.node]]
            else:
                d[neighbor.node] = distance_same_cycle(neighbor.node, cycle[index].top, neighbor)
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
    if ancestor == u:
        return [ancestor], 0

    def _distance_same_cycle(ancestor, v):
        path = []
        cost = 0
        ancestor_last = len(d[ancestor]) - 1
        v_last = len(d[v]) - 1
        print(node_to_cycle_index)
        print(depth)
        print(ancestor)
        print(v)
        if node_to_cycle_index[ancestor] != node_to_cycle_index[v] or v_last > 0 and d[v][v_last-1][1] == parent[v]:
            while d[v][v_last][1] != ancestor:
                path = [d[v][v_last][1]] + path
                cost = max(cost, d[v][v_last][0])
                v_last -= 1
            path = [d[v][v_last][1]] + path
        elif ancestor_last > 0 and d[ancestor][ancestor_last-1][1] != parent[ancestor]:
            while d[ancestor][ancestor_last][1] != v:
                path.append(d[ancestor][ancestor_last][1])
                cost = max(d[ancestor][ancestor_last][0], cost)
                ancestor_last -= 1
            path.append(d[ancestor][ancestor_last][1])
        elif len(d[v]) > 1 and d[v][1][1] != parent[v]:
            while d[ancestor][ancestor_last][1] != cycle[index].top:
                path.append(d[ancestor][ancestor_last][1])
                cost = max(d[ancestor][ancestor_last][0], cost)
                ancestor_last -= 1
            path.append(cycle[index].top)
            member = cycle[index].first_member
            while member != v:
                path.append(member)
                member = parent[member]
            path.append(member)
            cost = max(distance_to_top[v], cost)
        return path, cost

    if not index or index == node_to_cycle_index[u]:
        return _distance_same_cycle(ancestor, u)
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
    p, c = _distance_same_cycle(ancestor, b)
    # p_2, c_2 = _distance_same_cycle(b, u)
    # return p + p_2[1:], max(c, c_2)


def calc(u, v):
    r = lca(u, v)
    print(r)
    p, c = distance_top_down(r, u)
    p_2, c_2 = distance_top_down(r, v)
    if p[0] == p_2[0]:
        p_2 = p_2[1:]
    print("-----------")
    for i in reversed(p):
        print(i)
    for i in p_2:
        print(i)
    print("------------------")
    print(max(c, c_2))


if __name__ == "__main__":
    u = [1, 1, 1, 8, 8, 8, 2, 2, 3, 4, 4, 5]
    v = [8, 2, 3, 6, 7, 2, 4, 3, 4, 7, 5, 6]
    c = [2, 4, 7, 3, 14, 1, 9, 5, 1, 8, 6, 2]
    _u = [3]
    _v = [5]

    # u = [1,1,2,3,4,4,5,6]
    # v = [2,3,3,4,5,7,6,7]
    # c = [2,4,1,1,1,1,2,1]
    # _u = [4]
    # _v = [3]
    n = max(max(u), max(v))
    k = len(u)
    q = len(_u)

    n += 1
    neighbors = [[] for _ in range(n)]
    cycle = [Cycle() for _ in range(n)]
    parent = [0] * n
    node_to_cycle_index = [0] * n
    d = [[] for x in range(n)]
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

    d[1].append([0, 1])
    parent[1] = 1
    dfs(1)
    dfs2(1)
    # for i in range(q):
    #     calc(_u[i], _v[i])
    # print(d[5])
