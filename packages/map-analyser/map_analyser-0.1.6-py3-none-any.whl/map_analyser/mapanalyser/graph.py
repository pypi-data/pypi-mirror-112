from collections import defaultdict

from .util import (convex_orientation, intersects, point_in_rectangle,
                   segment_intersection)


def _index(coords, index):
    if index == 0:
        i = len(coords) - 1
        j = index
    else:
        i = index - 1
        j = index
    return coords[i], coords[j]


def _get_common_edge(area1, area2, include_point_intersections):
    """Quadratic algorithm checking intersection of each edge from area1 agains each edge from area2."""
    if intersects(area1.get_bb(), area2.get_bb()):
        cs1 = area1.coords_zipped
        cs2 = area2.coords_zipped

        common_edges = []
        for i in range(len(cs1)):
            for j in range(len(cs2)):
                common_edge = segment_intersection(_index(cs1, i), _index(cs2, j))

                if common_edge is None:
                    continue
                elif len(common_edge) == 1:
                    common_edges.append(common_edge[0])
                else:
                    return common_edge
        if len(common_edges) > 0 and include_point_intersections:
            return common_edges[0], common_edges[0]
    return None


def _area_contains_point(area, point):
    if point_in_rectangle(point, area.get_bb()):
        prev_orient = convex_orientation(*_index(area.coords_zipped, 0), point)
        for i in range(len(area)):
            orient = convex_orientation(*_index(area.coords_zipped, i), point)
            if prev_orient != orient:
                return False
            prev_orient = orient
        return True
    else:
        return False


class Graph:
    def __init__(self, areas):
        self.areas = [a for a in areas if a.speed > 0]
        self.edges = {}

    def create(self, neighbours_by_point):
        # quadratic algorithm in polygons and n^4 in all vertices
        for a in self.areas:
            a.neighbours = set()

        for a1 in self.areas:
            for a2 in self.areas:
                if a1 != a2:
                    tmp_edge = _get_common_edge(a1, a2, neighbours_by_point)
                    if tmp_edge is not None:
                        a1.neighbours.add(a2)
                        a2.neighbours.add(a1)
                        self.edges[(a1, a2)] = tmp_edge
                        self.edges[(a2, a1)] = tmp_edge
        return self

    def set_start_end(self, start, end):
        self.start = start
        self.end = end
        self.start_area = self._localize(start)
        self.end_area = self._localize(end)

    def _localize(self, point):
        for area in self.areas:

            if _area_contains_point(area, point):
                return area
        raise Exception(f'Point {point} outside of all areas.')
