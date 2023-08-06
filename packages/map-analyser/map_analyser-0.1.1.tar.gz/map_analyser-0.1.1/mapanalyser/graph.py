from .util import intersects, segment_intersection, convex_orientation, point_in_rectangle
from collections import defaultdict

def index(coords, index):
    if index == 0:
        i = len(coords) - 1
        j = index
    else:
        i = index - 1
        j = index
    return coords[i], coords[j]


def get_common_edge(area1, area2, include_point_intersections):
    """Quadratic algorithm checking intersection of each edge from area1 agains each edge from area2."""
    if intersects(area1.get_bb(), area2.get_bb()):
        cs1 = area1.coords_zipped
        cs2 = area2.coords_zipped

        common_edges = []
        for i in range(len(cs1)):
            for j in range(len(cs2)):
                common_edge = segment_intersection(index(cs1, i), index(cs2, j))

                if common_edge is None:
                    continue
                elif len(common_edge) == 1:
                    common_edges.append(common_edge[0])
                else:
                    return common_edge
        if len(common_edges) > 0 and include_point_intersections:
            return common_edges[0], common_edges[0]
    return None


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
                    tmp_edge = get_common_edge(a1, a2, neighbours_by_point)
                    if tmp_edge is not None:
                        a1.neighbours.add(a2)
                        a2.neighbours.add(a1)
                        self.edges[(a1, a2)] = tmp_edge
                        self.edges[(a2, a1)] = tmp_edge
        return self

    def _area_contains_point(self, area, point):
        if point_in_rectangle(point, area.get_bb()):
            prev_orient = convex_orientation(*index(area.coords_zipped, 0), point)
            for i in range(len(area)):
                orient = convex_orientation(*index(area.coords_zipped, i), point)
                if prev_orient != orient:
                    return False
                prev_orient = orient
            return True
        else:
            return False

    def set_start_end(self, start, end):
        self.start = start
        self.end = end
        self.start_area = self._localize(start)
        self.end_area = self._localize(end)

    def _localize(self, point):
        for area in self.areas:

            # global VIEWER_FOR_DEBUGGING
            # VIEWER_FOR_DEBUGGING.add_path(area.coords_zipped, color='#FF00BB')

            if self._area_contains_point(area, point):
                return area
        raise Exception(f'Point {point} outside of all areas.')

    # def create_edge_graph(self):
    #     self.edges = defaultdict(set)
    #
    #     # quadratic algorithm
    #     for a1 in self.areas:
    #         for a2 in self.areas:
    #             tmp_edge = get_common_edge(a1, a2)
    #             if tmp_edge is not None:
    #                 a1.edges.add((tmp_edge, a2))
    #                 a2.edges.add((tmp_edge, a1))
    #     return self

    # def _get_common_edges(self, ordered_areas):
    #     # could be done better with dynamic programming ??
    #     # could be done with sets
    #
    #     common_edges = []
    #     from itertools import product
    #     for i in range(len(ordered_areas) - 1):
    #         p1, p2 = ordered_areas[i], ordered_areas[i + 1]
    #         for j, k in product(range(len(p1) - 1), range(len(p2) - 1)):
    #             if p1[j] == p2[k] and p1[j + 1] == p2[k + 1]:
    #                 common_edges.append((p1[j], p1[j + 1]))
    #                 break
    #         # if p1[j] == p2[k] and p1[0] == p2[0]:
    #         #     common_edges.append((p1[j], p1[0]))
    #     return common_edges

