import logging
import sys

import map_analyser.mapanalyser as ma
from map_analyser.app.presenters import Viewer
from map_analyser.app.util import read_config
from map_analyser.maplib import load_map

DEBUG = False

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s (%(levelname)s): %(message)s'))

root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(handler)


def main(viewer, params):
    """This is the flow of a program."""

    if params["input"] is None:
        map_file = viewer.get_file()
    else:
        map_file = params["input"]

    yield 'Loading map'
    map = load_map(map_file)
    viewer.add_map(map)

    yield 'Extracting polygons'
    speeds = read_config(params['config_name'])
    areas = ma.map_to_areas(map, speeds)
    areas = ma.filter_areas(areas)

    yield 'Cleaning polygons'
    areas = ma.clean_areas(areas)
    tmp = ma.offset_areas(areas)
    areas = ma.create_default_area(areas)
    areas.extend(tmp)

    used_speeds = set()
    priorities = set()
    for area in areas:
        used_speeds.add(area.speed)
        priorities.add(area.priority)

    yield 'Clipping polygons'
    clipped_areas = ma.clip_areas(areas, priorities)

    yield 'Merging polygons'
    merged_areas = ma.merge_areas(clipped_areas, used_speeds)

    yield 'Partitioning polygons'
    partitioned_areas = ma.partition_areas(merged_areas)

    yield 'Creating graph'
    graph = ma.get_graph(partitioned_areas, params["neighbours_by_point"])

    viewer.add_graph(graph)

    viewer.prompt_start_end()
    yield 'Please add start and end:'
    start, end = viewer.get_start_and_end()

    yield 'Calculating path with A star'

    path = ma.find_good_path(graph, start, end)
    viewer.add_path(path, color="#00FF00")

    yield 'Calculating path with pruning'

    path = ma.find_fastest_path(graph,
                                start,
                                end,
                                max_speed=max(used_speeds),  # max speed is at most 100 (percent)
                                in_parallel=params["in_parallel"])
    viewer.add_path(path)

    yield 'Calculation finnished'


def run():
    params = {
        "in_parallel": False,
        "neighbours_by_point": False,
        "config_name": 'configISOM2017.csv',
        "input": None
    }

    vw = Viewer()
    vw.entry(lambda viewer: main(viewer, params))


if __name__ == "__main__":
    run()
