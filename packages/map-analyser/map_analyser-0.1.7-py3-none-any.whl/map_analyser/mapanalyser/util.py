import numpy as np

from map_analyser import maplib as ml

EPSILON = 0.1


def get_point(start, end, step):
    assert step >= 0 and step <= 1
    x = start[0] + (end[0] - start[0]) * step
    y = start[1] + (end[1] - start[1]) * step
    return ml.Coord(x, y)


def distance(a, b):
    return np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def rect_point_distance(bb, p):
    dx = np.max((bb[0].x - p.x, 0, p.x - bb[1].x))
    dy = np.max((bb[0].y - p.y, 0, p.y - bb[1].y))
    if dx ** 2 + dy ** 2 < 0 \
            or np.isnan(dx ** 2 + dy ** 2):
        pass
    return np.sqrt(dx ** 2 + dy ** 2)


def average(a, b):
    return (a + b) * 0.5


def length_of_curve(curve):
    x = np.asarray(curve)
    return np.sum(np.linalg.norm(x[1:] - x[:-1], axis=1))


def intersects(bb1, bb2):
    if bb1 is None or bb2 is None:
        return False
    return not (bb1[0][0] > bb2[1][0] and bb1[1][0] < bb2[0][0] and bb1[0][1] > bb2[1][1] and bb1[1][1] < bb2[0][1])


def det(a, b, o):
    return (a.x - o.x) * (b.y - o.y) - (b.x - o.x) * (a.y - o.y)


def cross(a, b):
    return a.x * b.y - a.y * b.x


def dot(a, b):
    return a.x * b.x + a.y * b.y


def convex_orientation(a, b, c):
    return cross(b - a, b - c) >= 0


def point_in_rectangle(point, rect):
    return point[0] >= rect[0][0] and point[0] <= rect[1][0] and point[1] >= rect[0][1] and point[1] <= rect[1][1]


def point_on_segmentPRECISE(p, a, b):
    return distance(p, a) + distance(p, b) == distance(a, b)


def point_on_segment(p, a, b):
    d = distance(a, b)
    return d - EPSILON < distance(p, a) + distance(p, b) < d + EPSILON


def seg_bb(seg):
    (x1, y1), (x2, y2) = seg
    return (min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2))


def segment_intersection(seg1, seg2):
    """Return None if no intersection, one tuple for intersection in point and two tuple for intersection in segment"""
    if not intersects(seg_bb(seg1), seg_bb(seg2)):
        return None

    a, b, c, d = *seg1, *seg2

    ret = []
    if point_on_segment(a, c, d):
        ret.append(a)
    if point_on_segment(b, c, d):
        ret.append(b)
    if point_on_segment(c, a, b):
        ret.append(c)
    if point_on_segment(d, a, b):
        ret.append(d)

    if len(ret) == 0:
        return None
    else:
        return tuple(set(ret))  # returns just distinct points


def segment_intersectionNOT_WORKING(seg1, seg2):
    if seg1 == seg2:
        if seg1[0] == seg1[1]:
            return seg1[0],
        else:
            return seg1

    a, b, c, d = ml.Coord(*seg1[0]), ml.Coord(*seg1[1]), ml.Coord(*seg2[0]), ml.Coord(*seg2[1])

    # degenerate cases:
    if a == b and c == d:
        return None
    elif a == b:
        if point_on_segment(a, c, d):
            return a
        return None
    elif c == d:
        if point_on_segment(c, a, b):
            return c
        return None

    r, s = b - a, d - c

    cross_product = abs(cross(r, s))
    if cross_product < EPSILON:  # same (or opposite) direction
        if abs(cross(c - a, r)) < EPSILON:  # collinear

            t1 = dot(c - a, r) / dot(r, r)  # c on ab (=r)
            t2 = t1 + dot(s, r) / dot(r, r)  # d on ab (=r)

            # s · r < 0 and so the interval to be checked is [t1, t0] rather than [t0, t1].
            if dot(s, r) < 0:
                t1, t2 = t2, t1

            if 0 <= t1 <= 1:
                if t2 <= 1:
                    return c, d
                else:
                    return c, b
            elif t1 < 0:
                if 0 <= t2 <= 1:
                    return a, d
                elif t2 > 1:
                    return a, b
    else:
        t = cross(c - a, s) / cross_product
        u = cross(c - a, r) / cross_product

        if t >= 0 and t <= 1 and u >= 0 and u <= 1:  # intersecting
            # DOES NOT WORK when orientation changes

            n = c + s * u  # calculates intersection
            # NOTE: m and n should be same(except rounding errors)
            # m = a + r * t
            # print("========== check intersection: " << n.x << " " << n.y << " ?=? " << m.x << " " << m.y << std::endl)

            if t > 0 and t < 1 and u > 0 and u < 1:  # intersecting in interiors
                print(f'Should not intersect!!! {seg1} {seg2}')  # means neigboring polygons have crossing edges
                return n,
            # following are all "T" cases:
            elif t == 0 and u > 0 and u < 1:
                return a,
            elif t == 1 and u > 0 and u < 1:
                return b,
            elif u == 0 and t > 0 and t < 1:
                return c,
            elif u == 1 and t > 0 and t < 1:
                return d,
            else:
                # segments have common endpoint
                return n,
    return None


def segment_intersectionPRECISE(seg1, seg2):
    if seg1 == seg2:
        return seg1

    a, b, c, d = ml.Coord(*seg1[0]), ml.Coord(*seg1[1]), ml.Coord(*seg2[0]), ml.Coord(*seg2[1])

    # degenerate cases:
    if a == b and c == d:
        return None
    elif a == b:
        if point_on_segment(a, c, d):
            return a
        return None
    elif c == d:
        if point_on_segment(c, a, b):
            return c
        return None

    r, s = b - a, d - c

    cross_product = cross(r, s)
    if cross_product == 0:  # same (or opposite) direction
        if cross(c - a, r) == 0:  # collinear

            t1 = dot(c - a, r) / dot(r, r)  # c on ab (=r)
            t2 = t1 + dot(s, r) / dot(r, r)  # d on ab (=r)

            # s · r < 0 and so the interval to be checked is [t1, t0] rather than [t0, t1].
            if dot(s, r) < 0:
                t1, t2 = t2, t1

            if 0 <= t1 <= 1:
                if t2 <= 1:
                    return c, d
                else:
                    return c, b
            elif t1 < 0:
                if 0 <= t2 <= 1:
                    return a, d
                elif t2 > 1:
                    return a, b
    else:
        t = cross(c - a, s) / cross_product
        u = cross(c - a, r) / cross_product

        if t >= 0 and t <= 1 and u >= 0 and u <= 1:  # intersecting
            n = c + s * u  # calculates intersection
            # NOTE: m and n should be same(except rounding errors)
            # m = a + r * t
            # print("========== check intersection: " << n.x << " " << n.y << " ?=? " << m.x << " " << m.y << std::endl)

            if t > 0 and t < 1 and u > 0 and u < 1:  # intersecting in interiors
                print(f'Should not intersect!!! {seg1} {seg2}')  # means neigboring polygons have crossing edges
                return n
            # following are all "T" cases:
            elif t == 0 and u > 0 and u < 1:
                return a
            elif t == 1 and u > 0 and u < 1:
                return b
            elif u == 0 and t > 0 and t < 1:
                return c
            elif u == 1 and t > 0 and t < 1:
                return d
            else:
                # segments have common endpoint
                return n
    return None


def poly_tree_to_areas(poly_tree, area):
    ret = []
    stack = [poly_tree]
    while len(stack) > 0:
        p = stack.pop()
        if len(p.Contour) > 0:
            if p.IsHole:
                p.Parent.Area.add_hole(p.Contour)
            else:
                tmp = area.copy()
                tmp.drop_holes()
                tmp.set_coords(p.Contour)
                ret.append(tmp)
                for child in p.Childs:
                    child.Parent.Area = tmp

        for child in p.Childs:
            stack.append(child)
    return ret


def paths_to_holes(paths, area):
    for p in paths:
        area.add_hole(p)
    return area


def paths_to_areas(paths, area):
    ret = []

    for p in paths:
        tmp = area.copy()
        tmp.drop_holes()
        tmp.set_coords(p)
        ret.append(tmp)

    return ret


def UNUSED(this_is_test_of_distance_calculation):
    import time
    t0 = time.time()
    for i in range(1, 1000):
        x = np.asarray([(j, j) for j in range(i)])
        t = time.time()
        for _ in range(1000):
            np.sum(np.sqrt(np.sum(np.diff(x, axis=0) ** 2, axis=1)))
        print(time.time() - t, end=', ')

    print()
    print(time.time() - t0)

    t0 = time.time()
    for i in range(1, 1000):
        x = np.asarray([(j, j) for j in range(i)])
        t = time.time()
        for _ in range(1000):
            np.sum(np.linalg.norm(x[1:] - x[:-1], axis=1))
        print(time.time() - t, end=', ')
    print()
    print(time.time() - t0)

    return np.sum(np.sqrt(np.sum(np.diff(curve, axis=0) ** 2, axis=1)))
    np.sum(np.linalg.norm(curve[1:] - curve[:-1], axis=1))
