import concurrent.futures
import heapq
import itertools
import logging
from collections import OrderedDict
from multiprocessing import cpu_count

from .CPsolver import get_point, solve
from .util import average, distance, rect_point_distance


def find_good_path(graph, start, end, max_speed=100):
    dist, path = CentersAStar(graph, start, end).find_first_solution(max_speed)

    return path


def find_fastest_path(graph, start, end, max_speed=100, in_parallel=False):
    dist, path = CentersAStar(graph, start, end).find_first_solution(max_speed)

    path = Pruning(graph, start, end, max_speed, dist).find_best_path(in_parallel=in_parallel)

    return path


def solve_optimization(graph, areas, return_path=False):
    n = len(areas) - 1

    if n == 0:  # start and end are in same area
        common_edges, lambdas = [], []
        dist = 1 / areas[0].speed * distance(graph.start, graph.end)
    else:
        common_edges = [graph.edges[(areas[i], areas[i + 1])] for i in range(n)]
        speeds = [1 / a.speed for a in areas]
        dist, lambdas = solve(graph.start, graph.end, speeds, common_edges)

    if return_path:
        path = [graph.start] + [get_point(*e, l) for e, l in zip(common_edges, lambdas)] + [graph.end]
        return dist, path
    else:
        return dist


class CentersAStar():
    def __init__(self, graph, start, end):
        graph.set_start_end(start, end)
        self.graph = graph

    def find_first_solution(self, max_speed):
        frontier = [(0, 0, self.graph.start_area)]
        distances = {self.graph.start_area: 0}
        predecessors = {self.graph.start_area: None}

        while len(frontier) > 0:
            _, count, area = heapq.heappop(frontier)

            if area == self.graph.end_area:
                return self.build_solution(predecessors)

            for n in area.neighbours:
                dist = distances[area] + self.calculate_dist(area, n)
                if n not in distances or dist < distances[n]:
                    count += 1
                    distances[n] = dist
                    priority = dist + distance(area.get_center(), self.graph.end) / max_speed
                    heapq.heappush(frontier, (priority, count, n))
                    predecessors[n] = area

        raise Exception('No path found between start and end')

    def build_solution(self, predecessors):
        ordered_areas = [self.graph.end_area]
        while predecessors[ordered_areas[-1]] is not None:
            ordered_areas.append(predecessors[ordered_areas[-1]])

        dist, path = solve_optimization(self.graph, list(reversed(ordered_areas)), return_path=True)

        return dist, path

    def calculate_dist(self, area1, area2):
        """Calculates distance of two areas through middle of their common edge weighted by speeds of these areas."""
        a = area1.get_center()
        b = area2.get_center()
        if area1 == self.graph.start_area:
            a = self.graph.start
        if area2 == self.graph.end_area:
            b = self.graph.end

        if (area1, area2) not in self.graph.edges:
            raise Exception(f'{area1} and {area2} are not neighbors.')

        middle = average(*self.graph.edges[(area1, area2)])

        return distance(a, middle) / area1.speed + distance(middle, b) / area2.speed


class BrutForce:
    def __init__(self, graph, start, end):
        graph.set_start_end(start, end)
        self.graph = graph

    def iterate_paths_recursive(self, graph):
        path = OrderedDict([(graph.start_area, None)])
        yield from self.recursive(path)

    def recursive(self, path):
        for n in next(reversed(path)).neighbours:
            if n not in path:
                path[n] = None
                if n == self.graph.end_area:
                    yield list(path.keys())[:]
                else:
                    yield from self.recursive(path)
                del path[n]

    def find_best_path(self, initial=float('inf'), in_parallel=False):
        best = initial
        best_path = []

        if in_parallel:
            with concurrent.futures.ThreadPoolExecutor() as executor:

                def to_chunks(n, iterable):
                    it = iter(iterable)
                    while True:
                        chunk = tuple(itertools.islice(it, n))
                        if not chunk:
                            return
                        yield chunk

                solve_lamb = lambda path: solve_optimization(self.graph, path, return_path=True)

                for chunk in to_chunks(6 * cpu_count(), self.iterate_paths_recursive(self.graph)):
                    for value, path in executor.map(solve_lamb, chunk):
                        if value < best:
                            logging.debug(f'>>>>>> better value: {value}')
                            best = value
                            best_path = path

        else:
            for path in self.iterate_paths_recursive(self.graph):
                value = solve_optimization(self.graph, path)
                if value <= best:
                    logging.debug(f'>>>>>> better value: {value}')
                    best = value
                    best_path = path

        dist, path = solve_optimization(self.graph, best_path, return_path=True)

        return dist, path


class Pruning(BrutForce):
    def __init__(self, graph, start, end, max_speed, dist):
        self.max_speed = max_speed
        self.dist = dist
        graph.set_start_end(start, end)
        self.graph = graph

    def find_best_path(self, initial=None, in_parallel=False):
        self.prune(self.dist, self.max_speed)

        dist, path = super().find_best_path(initial=self.dist, in_parallel=in_parallel)

        return path

    def prune(self, dist, max_speed):
        self.max_speed = max_speed
        self.dist = dist

        unwanted = []
        for area in self.graph.areas:
            bb = area.get_bb()
            d1 = rect_point_distance(bb, self.graph.start)
            d2 = rect_point_distance(bb, self.graph.end)
            if 1 / max_speed * (d1 + d2) >= dist:
                unwanted.append(area)

        for area in unwanted:
            for a in area.neighbours:
                a.neighbours.remove(area)
                self.graph.edges.pop((a, area))
                self.graph.edges.pop((area, a))
            self.graph.areas.remove(area)
