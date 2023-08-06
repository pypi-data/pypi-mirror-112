import logging

import numpy as np

from map_analyser import maplib as ml

from .clipper import *
from .geometry import convex_hull, decompose
from .graph import Graph
from .util import get_point


def clean_areas(areas):
    cleaned_areas = []
    for area in areas:
        tmp_areas = simplify(area)
        tmp_areas = clean(tmp_areas)

        cleaned_areas.extend(tmp_areas)

    return cleaned_areas


def offset_areas(areas):
    ret = []

    for area in areas:
        # offset with speed 0
        if area.speed == 0:
            ret.extend(offset(area, 100))
        else:
            ret.append(area)

    return ret


def clip_areas(areas, priorities):
    clipped_areas = []

    # clip by color priority
    for c in sorted(priorities):
        clip_areas = [a for a in areas if a.priority == c]
        areas = clip(clip_areas, [a for a in areas if a.priority > c])

        clipped_areas.extend(clip_areas)
        logging.debug(f"priority {c} clipped")

    return clipped_areas


def merge_areas(areas, speeds):
    merged_areas = []
    for s in speeds:
        tmp = merge([a for a in areas if a.speed == s], return_area=Area.get_speed_area(s))
        merged_areas.extend(tmp)

    return clean(merged_areas)


def create_default_area(areas):
    default_area = Area.get_speed_area(90)
    default_area.priority = max(a.priority for a in areas) + 1

    default_area = convex_hull(areas, return_area=default_area)

    return default_area


def get_graph(areas, neighbours_by_point=True):
    """Areas have to be convex, simple, no holes."""
    return Graph(areas).create(neighbours_by_point)


def partition_areas(areas):
    ret = []
    for a in areas:
        tmp = decompose(a)
        ret.extend(tmp)
        logging.debug(f"Decomposed areas: {len(ret)}")
    return ret


def map_to_areas(map, speeds):
    all_objects = []
    for o in map.objects:
        if o.symbol not in map.symbols:
            continue
        symbol = map.symbols[o.symbol]

        code = symbol.code.split('.')[0] if '.' in symbol.code else symbol.code
        if code in speeds:
            if speeds[code] >= 0:
                all_objects.append(Area(o, symbol, colors=map.colors, speed=speeds[code]))
        # else:
        #     logging.warning(f"Code {code} not in config.")

    ret = []
    for area in all_objects:
        if area.symbol_type == ml.Symbol.LINE_SYMBOL:
            ret.extend(offset(area, area.width))
        else:
            ret.append(area)

    return ret


def filter_areas(areas):
    return [a for a in areas if
            a.symbol_type in (ml.Symbol.LINE_SYMBOL, ml.Symbol.AREA_SYMBOL, ml.Symbol.COMBINED_SYMBOL)]


class Area():
    HOLES_ORIENTATION = False
    ORIENTATION = True

    @classmethod
    def get_speed_area(cls, speed):
        ret = cls.__new__(cls)
        ret.speed = speed

        ret.r = int(speed * 2.55)
        ret.g = int(speed * 2.55)
        ret.b = int(speed * 2.55)

        ret.coords = ([], [])
        ret.coords_zipped = []

        ret.holes = []

        return ret

    def __init__(self, object, symbol, colors=None, speed=0):
        if colors is None:
            colors = []
        self.speed = speed
        self.symbol_type = symbol.type
        self.holes = []

        coords, holes = self._parse_coords(object.coords_zipped, object.coords_flags)
        self.set_coords(coords)
        # self.coords = ml.CoordsLists(np.asarray([p.x for p in coords]), np.asarray([p.y for p in coords]))
        # self.coords_zipped = coords

        for hole in holes:
            self.add_hole(hole)

        col = symbol.symbol_appearance['color']
        self.priority = col
        if col != -1:
            c = colors[col]
            self.r = int(float(c.r) * 255)
            self.g = int(float(c.g) * 255)
            self.b = int(float(c.b) * 255)
        else:
            # logging.warning(f'No color found for symbol {symbol}')
            self.r = 255
            self.g = 192
            self.b = 203

        if self.symbol_type == ml.Symbol.LINE_SYMBOL:
            self.width = symbol.symbol_appearance['width']

    def __len__(self):
        # return len(self.coords[0])
        return len(self.coords_zipped)

    def __iter__(self):
        # return zip(self.coords[0], self.coords[1])
        return iter(self.coords_zipped)

    def __getitem__(self, key):
        return self.coords_zipped[key]
        # return (self.coords[0][key], self.coords[1][key])

    def __str__(self):
        if len(self) == 0:
            return f'{self.speed}:  >empty< '
        else:
            return f'speed: {self.speed}: {self.get_center()}'

    def __repr__(self):
        return self.__str__()

    def orientation(self):
        return orientation(self.coords_zipped)

    def copy(self):
        ret = Area.__new__(Area)
        ret.r, ret.g, ret.b = self.r, self.g, self.b
        if hasattr(self, 'symbol_type'):
            ret.symbol_type = self.symbol_type
        if hasattr(self, 'priority'):
            ret.priority = self.priority

        ret.holes = self.holes
        ret.speed = self.speed

        ret.coords = self.coords
        ret.coords_zipped = self.coords_zipped

        return ret

    def get_bb(self):
        if not hasattr(self, '_bb'):
            if len(self) == 0:
                self._bb = None
            else:
                self._bb = (ml.Coord(self.coords.x.min(), self.coords.y.min()),
                            ml.Coord(self.coords.x.max(), self.coords.y.max()))
        return self._bb

    def get_center(self):
        if not hasattr(self, '_center'):
            self._center = ml.Coord(self.coords.x.mean(), self.coords.y.mean())
        return self._center

    def add_hole(self, hole, orient=None):
        if orient is None:
            orient = orientation(hole)
        if orient == Area.ORIENTATION:
            hole = reversed(hole)

        self.holes.append([ml.Coord(p[0], p[1]) for p in hole])

    def drop_holes(self):
        self.holes = []

    def set_coords(self, coords, orient=None):
        if orient is None:
            orient = orientation(coords)
        if orient != Area.ORIENTATION:
            coords = list(reversed(coords))

        self.coords_zipped = [ml.Coord(p[0], p[1]) for p in coords]
        self.coords = ml.CoordsLists(np.asarray([p[0] for p in coords]), np.asarray([p[1] for p in coords]))

        if hasattr(self, '_bb'):
            del self._bb

    def _aprox_bezier(self, start, p1, p2, end):
        def calculate_bezier(steps):
            ret = []
            for d in np.linspace(0, 1, steps, endpoint=False):
                x, y, z = get_point(start, p1, d), get_point(p1, p2, d), get_point(p2, end, d)
                m, n = get_point(x, y, d), get_point(y, z, d)
                ret.append(get_point(m, n, d))
            return ret

        return calculate_bezier(4)

    def _parse_coords(self, coords, flags):
        ret = []
        i = -1
        while i + 1 < len(coords):
            i += 1
            c = coords[i]
            f = int(flags[i])
            if f & ml.Object.Flags.CURVE_START:
                ret.extend(self._aprox_bezier(c, coords[i + 1], coords[i + 2], coords[i + 3]))
                i += 2
            elif f & ml.Object.Flags.HOLE_POINT:
                ret.append(c)
                break  # outline ended... # TODO
            else:
                ret.append(c)

        holes = []
        if i + 1 < len(coords):
            hole = []
            while i + 1 < len(coords):
                i += 1
                c = coords[i]
                f = int(flags[i])
                if f & ml.Object.Flags.CURVE_START:
                    hole.extend(self._aprox_bezier(c, coords[i + 1], coords[i + 2], coords[i + 3]))
                    i += 2
                elif f & ml.Object.Flags.CLOSE_POINT or i + 1 >= len(coords):
                    hole.append(c)
                    if len(hole) > 2:
                        holes.append(hole)
                    hole = []
                else:
                    hole.append(c)

        return ret, holes
