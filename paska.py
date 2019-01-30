import fileinput
import sys

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)


# kam zatáčí přímka o třech bodech
def turn(p, q, r):
    a = (q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])
    return (a > 0) - (a < 0)


# vzdálenost dvou bodů
def dist(p, q):
    return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5


# přidá bod do pod-obalu
def add_hull_point(hull, r):
    # dokud nezatáčí doleva odstraňuje elementy z hull
    while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
        hull.pop()
    # pokud tenhle bod neni ten první tak ho přidej
    if not len(hull) or hull[-1] != r:
        hull.append(r)
    return hull


# vytvoření pod-obalu
def monotone_chain(points):
    points.sort()
    right_hull = []
    left_hull = []
    for point1, point2 in zip(points, reversed(points)):
        right_hull = add_hull_point(right_hull, point1)
        left_hull = add_hull_point(left_hull, point2)
    return right_hull + left_hull[1:-1]


# získání prvního bodu do celkového obalu
def min_hull_pt_pair(hulls):
    h, p = 0, 0
    for i in range(len(hulls)):
        j = min(range(len(hulls[i])), key=lambda l: hulls[i][l])
        if hulls[i][j] < hulls[h][p]:
            h, p = i, j
    return h, p


# získání optimálního bodu z pod-obalu
def rtangent(hull, p):
    l, r = 0, len(hull)
    l_prev = turn(p, hull[0], hull[-1])
    l_next = turn(p, hull[0], hull[1 % r])
    while l < r:
        c = (l + r) // 2
        c_prev = turn(p, hull[c], hull[(c - 1) % len(hull)])
        c_next = turn(p, hull[c], hull[(c + 1) % len(hull)])
        c_side = turn(p, hull[l], hull[c])
        # pokud ani předchozí, ani následující bod nejde doleva, tak jsem v optimálním bodu
        if c_prev != TURN_RIGHT and c_next != TURN_RIGHT:
            return c % len(hull)
        elif c_side == TURN_LEFT and (l_next == TURN_RIGHT or l_prev == l_next) or \
                (c_side == TURN_RIGHT and c_prev == TURN_RIGHT):
            r = c
        else:
            l = c + 1
            l_prev = -c_next
            l_next = turn(p, hull[l % len(hull)], hull[(l + 1) % len(hull)])
    return l % len(hull)


# získání dalšího bodu do celkového obalu
def next_hull_pt_pair(hulls, pair):
    p = hulls[pair[0]][pair[1]]
    next_p = (pair[0], (pair[1] + 1) % len(hulls[pair[0]]))
    # projede optimální bod všech pod-obalů a zjistí který z nich jde nejvíce doprava
    for h in range(len(hulls)):
        if h != pair[0]:
            s = rtangent(hulls[h], p)
            q, r = hulls[next_p[0]][next_p[1]], hulls[h][s]
            t = turn(p, q, r)
            if t == TURN_RIGHT or (t == TURN_NONE and dist(p, r) > dist(p, q)):
                next_p = (h, s)
    return next_p


# hlavní funkce
def hull(points):
    for t in range(len(points)):
        # určení parametru m
        m = min(len(points), 1 << (1 << t))
        diameter = 0
        hulls = []
        i = 0
        # rozdělení do skupin a vytvoření pod-obalů
        while i < len(points):
            hulls.append(monotone_chain(points[i:i + m]))
            i += m
        # získání prvního bodu do celkového obalu
        main_hull = [min_hull_pt_pair(hulls)]
        # vytváření hlavního obalu po dobu m iterací
        for a in range(m):
            p = next_hull_pt_pair(hulls, main_hull[-1])
            diameter += dist(hulls[main_hull[-1][0]][main_hull[-1][1]], hulls[p[0]][p[1]])
            if p == main_hull[0]:
                return "%.2f" % diameter
            main_hull.append(p)


if __name__ == "__main__":
    unique_coordinates = set()
    for line in fileinput.input():
        if not fileinput.isfirstline():
            numbers = map(int, line.split(" ")[1:])
            it = iter(numbers)
            unique_coordinates.update(zip(it, it))
    sys.stdout.write(hull(list(unique_coordinates)) + "\n")
