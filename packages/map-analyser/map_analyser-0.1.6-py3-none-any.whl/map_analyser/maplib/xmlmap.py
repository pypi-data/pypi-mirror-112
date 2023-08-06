import logging

import numpy as np

from .util import Coord, CoordsLists


class Object:
    class Flags:
        NONE = 0
        CURVE_START = 1 << 0
        CLOSE_POINT = 1 << 1
        GAP_POINT = 1 << 2
        HOLE_POINT = 1 << 4
        DASH_POINT = 1 << 5

    class Type:
        UNKNOWN = -1
        POINT = 0
        PATH = 1
        TEXT = 4

    def __str__(self):
        if hasattr(self, 'symbol'):
            if len(self.coords) == 0:
                return f'{self.symbol}, {self.type}: >empty< '
            else:
                return f'{self.symbol}, {self.type}: {self.coords_zipped[0]} <--> {self.coords_zipped[-1]}'

    def __repr__(self):
        return self.__str__()

    def __init__(self, data):
        self.data = data

    def parse(self):
        self.type = int(self.data.attrib['type'])
        self.symbol = int(self.data.attrib['symbol'])

        # parse omap as well as xmap:
        if len(self.data[0]) == 0:  # omap
            x, y, flags = [], [], []
            for s in self.data[0].text.split(';'):
                if s:
                    l = s.split()
                    x.append(float(l[0]))
                    y.append(float(l[1]))
                    if len(l) > 2:
                        flags.append(float(l[2]))
                    else:
                        flags.append(Object.Flags.NONE)
            coords, coords_flags = (np.asarray(x), np.asarray(y)), np.asarray(flags)
        else:  # xmap
            coords = (np.asarray([float(c.attrib['x']) for c in self.data[0]]), \
                      np.asarray([float(c.attrib['y']) for c in self.data[0]]))

            coords_flags = np.asarray(
                [(Object.Flags.NONE if c.find('flag') is None else int(c.attrib['flag'])) for c in self.data[0]])

        self.coords_flags = coords_flags
        self.coords = CoordsLists(coords[0], coords[1])
        self.coords_zipped = [Coord(x, y) for x, y in zip(coords[0], coords[1])]

        return self


class Symbol:
    private_count = 0

    NO_SYMBOL = 0
    POINT_SYMBOL = 1
    LINE_SYMBOL = 2
    AREA_SYMBOL = 4
    TEXT_SYMBOL = 8
    COMBINED_SYMBOL = 16

    def __init__(self, data):
        self.data = data

    def __str__(self):
        if not hasattr(self, 'id'):
            ret = 'not parsed'
        elif hasattr(self, 'private'):
            ret = f'private: {self.code}, {self.type}, {self.name}'
        else:
            try:
                ret = f'{self.id}: {self.code}, {self.type}, {self.name}'
            except:
                ret = 'unknown symbol'
        return ret

    def __repr__(self):
        return self.__str__()

    def parse(self, private=False):
        if not private:
            self.id = int(self.data.attrib['id'])
        else:
            self.private = True
            self.id = 'private' + str(Symbol.private_count)
            Symbol.private_count += 1

        try:
            self.type = int(self.data.attrib['type'])
            self.code = self.data.attrib['code']

            self.name = self.data.attrib['name']

            self.symbol_appearance = self.parse_symbol_appearance(self.type)

        except Exception as e:
            logging.warning(f'Problem parsing symbol: {self}')
            return self.id, None

        if private:
            return self

        return self.id, self

    def parse_symbol_appearance(self, t):
        if t == Symbol.POINT_SYMBOL:
            return {'color': int(self.data.findall('./point_symbol[@inner_color]')[0].attrib['inner_color'])}
        if t == Symbol.LINE_SYMBOL:
            return {'color': int(self.data.findall('./line_symbol[@color]')[0].attrib['color']),
                    'width': int(self.data.findall('./line_symbol[@color]')[0].attrib['line_width'])}
        if t == Symbol.AREA_SYMBOL:
            return {'color': int(self.data.findall('./area_symbol[@inner_color]')[0].attrib['inner_color'])}
        if t == Symbol.TEXT_SYMBOL:
            return None
        if t == Symbol.COMBINED_SYMBOL:
            sub_symbols = []
            for part in self.data.findall('./combined_symbol/part'):
                if 'symbol' in part.attrib:
                    sub_symbols.append(int(part.attrib['symbol']))
                if 'private' in part.attrib:
                    sub_symbols.append(Symbol(part.find('symbol')).parse(private=True))
            return {'color': 'Calculate', 'symbols': sub_symbols}
        return {}


class Color:

    def __init__(self, data):
        self.data = data

    def parse(self):
        d = self.data
        self.priority = int(d.attrib['priority'])
        self.name = d.attrib['name']

        self.c = d.attrib['c']
        self.m = d.attrib['m']
        self.y = d.attrib['y']
        self.k = d.attrib['k']
        self.opacity = d.attrib['opacity']

        tmp = d.findall('.//rgb')[0]
        self.r = tmp.attrib['r']
        self.g = tmp.attrib['g']
        self.b = tmp.attrib['b']

        return self.priority, self
