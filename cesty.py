# https://www.codechef.com/problems/TACTQUER


class Cycle:
    top = 0
    order = 0
    length = 0


def dfs(cur, pre):
    global timer
    global cc
    timer += 1
    tin[cur] = timer
    vis[cur] = True
    L[cur] = 0 if pre == -1 else L[pre] + 1
    pc[0][cur] = cur if pre == -1 else pre
    for i in range(len(adj[cur]) - 1):
        t1 = adj[cur][i]
        if t1 == pre:
            continue
        if vis[t1]:
            if tin[t1] > tin[cur]:
                continue
            cc += 1
            cycle[cc].top = t1
            cycle[cc].length = wt[cur][i]
            CI[t1] = cc
            DFT[t1] = 0
            t2 = cur
            while t2 != t1:
                CI[t2] = cc
                DFT[t2] = cycle[cc].length
                cycle[cc].length += DFP[t2]
                t2 = pc[0][t2]
        else:
            DFP[t1] = wt[cur][i]
            dfs(t1, cur)
        i += 1
    timer += 1
    tout[cur] = timer


def dfs2(cur):
    MO[0][cur] = max(cycle[CI[cur]].order, cycle[CI[pc[0][cur]]].order)
    vis[cur] = True
    for i in range(len(adj[cur]) - 1):
        t1 = adj[cur][i]
        if vis[t1]:
            continue
        dist[t1] = dist[cur] + wt[cur][i]
        if CI[t1]:
            dist[t1] = min(dist[t1], dist[cycle[CI[t1]].top] + min(DFT[t1], cycle[CI[t1]].length - DFT[t1]))
        dfs2(t1)


def anc(x, y):
    if tin[x] <= tin[y] and tout[x] >= tout[y]:
        return True
    return False


def LCA(x, y):
    if L[x] > L[y]:
        return LCA(y, x)
    if anc(x, y):
        return x
    i = 20
    while i >= 0:
        if not anc(pc[i][y], x):
            y = pc[i][x]
        i -= 1
    return pc[0][y]


def find_b(x, y):
    ord = cycle[CI[x]].order
    i = 20
    while i >= 0:
        if MO[i][y] < ord:
            y = pc[i][y]
        i -= 1
    return pc[0][y]


def DTD(x, y):
    if not CI[x]:
        return dist[y] - dist[x]
    if CI[x] == CI[y]:
        return min(abs(DFT[x] - DFT[y]), cycle[CI[x]].length - abs(DFT[x] - DFT[y]))
    b = find_b(x, y)
    return dist[y] - dist[b] + DTD(x, b)


if __name__ == "__main__":
    cp = [0] * 100005
    cycle = [Cycle] * 100005
    DFT = cp.copy()
    dist = cp.copy()
    pc = [[0] * 22] * 100005
    MO = [[0] * 22] * 100005
    tin = cp.copy()
    tout = cp.copy()
    L = cp.copy()
    vis = [False] * 100005
    DFP = cp.copy()
    CI = cp.copy()
    adj = [[]] * 100005
    wt = [[]] * 100005
    timer = 0
    cc = 0
    mo = 0

    n = 2
    m = 1
    x = [1]
    y = [2]
    z = [10]
    q = 1
    x_ = 1
    y_ = 2
    for i in range(m):
        adj[x[i]].append(y[i])
        adj[y[i]].append(x[i])
        wt[x[i]].append(z[i])
        wt[y[i]].append(z[i])
    cycle[0].order = 0
    dfs(1, -1)
    dfs2(1)
    for i in range(20):
        for a in range(n):
            pc[i][a] = pc[i - 1][pc[i - 1][a]]
            MO[i][a] = max(MO[i - 1][a], MO[i - 1][pc[i - 1][a]])
    for i in range(q):
        lc = LCA(x_, y_)
        print(DTD(lc, x_) + DTD(lc, y_))
