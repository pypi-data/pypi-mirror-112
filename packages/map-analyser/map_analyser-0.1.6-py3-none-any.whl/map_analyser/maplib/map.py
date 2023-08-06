import logging
import xml.etree.ElementTree as et

import numpy as np
from PIL import Image, ImageTk

from . import xmlmap as xm
from .util import Coord, ParseError


def load_map(file_name):
    ext = file_name.split('.')[-1]

    try:
        if ext in ['omap', 'xmap']:
            return OOMapperMap(file_name, ext).parse()
        elif ext in ['ocd']:
            raise NotImplementedError
        else:
            return RasterMap(file_name)
    except Exception as ex:
        logging.error(ex)
        raise ex


class Map:
    def __init__(self):
        pass

    def get_photo_image(self, scale=1.0):
        raise NotImplementedError


class RasterMap(Map):
    def __init__(self, file_name):
        super().__init__()
        self.map = Image.open(file_name)
        self.bounding_box = (800, 600)

    def get_photo_image(self, scale=1.0):
        w, h = int(scale * self.map.size[0]), int(scale * self.map.size[1])
        return ImageTk.PhotoImage(self.map.resize((w, h)))


class OOMapperMap(Map):
    def __init__(self, name, ext):
        super().__init__()
        self.ext = ext
        self.name = name

        self.file = self._read_file(name)

    def _read_file(self, name):
        try:
            with open(name, 'rb') as f:
                file = f.read()
                # get rid of namespace (hacky)
                file = file.replace(b'xmlns="http://openorienteering.org/apps/mapper/xml/v2"', b'')
                file = file.replace(b'xmlns="http://openorienteering.org/apps/mapper/xml/v1"', b'')
                file = file.replace(b'xmlns="http://openorienteering.org/apps/mapper/xml"', b'')
        except:
            raise ParseError(f'Could not read file: {name}')
        return file

    def parse(self):
        try:
            self.file = et.fromstring(self.file)
        except:
            raise ParseError(f'Could not parse file: {self.name}')

        # list of objects
        self.objects = [xm.Object(o).parse() for o in self.file.findall('.//objects/object')]
        # dict of symbols by id
        self.symbols = dict(xm.Symbol(s).parse() for s in self.file.findall('.//symbols/symbol'))
        self.symbols = self._find_additional_info_symbols(self.symbols)
        # dict of symbols by code
        self.symbols_by_code = {s.code: s for _, s in self.symbols.items() if s}
        # dict of colors by priority
        self.colors = dict(xm.Color(c).parse() for c in self.file.findall('.//colors/color'))

        return self

    def get_bounding_box(self):
        if not hasattr(self, '_bounding_box'):
            mins_x = np.asarray([o.coords.x.min() for o in self.objects])
            maxs_x = np.asarray([o.coords.x.max() for o in self.objects])
            mins_y = np.asarray([o.coords.y.min() for o in self.objects])
            maxs_y = np.asarray([o.coords.y.max() for o in self.objects])
            self._bounding_box = Coord(mins_x.min(), mins_y.min()), Coord(maxs_x.max(), maxs_y.max())
        return self._bounding_box

    def _find_additional_info_symbols(self, symbols):
        symbols = {k: v for k, v in symbols.items() if v is not None}
        for s_id, s in symbols.items():
            if s.symbol_appearance:
                if s.symbol_appearance['color'] == 'Calculate':
                    sub_symbols = [symbols[key] if isinstance(key, int) else key for key in
                                   s.symbol_appearance['symbols']]
                    area_sub_symbols = [s for s in sub_symbols if s.type == xm.Symbol.AREA_SYMBOL]
                    if len(area_sub_symbols) == 1:
                        symbols[s_id].symbol_appearance['color'] = area_sub_symbols[0].symbol_appearance['color']
                    # some ad hoc extractions:
                    elif s.code in ['508.1', '508.2', '508.3',
                                    '508.4']:  # '502.2', '508.1', '508.2', '508.3', '508.4', '509', '511.2'
                        symbols[s_id].symbol_appearance['color'] = sub_symbols[-1].symbol_appearance['color']
                    else:
                        logging.warning(f'Cannot find color for symbol {s} \n\t - not using objects of this symbol.')
                        symbols[s_id] = None
        return {k: v for k, v in symbols.items() if v is not None}

    def get_photo_image(self, scale=1 / 1000.0):
        # TODO export map
        # TODO cache different sizes of image
        # TODO check the midlle
        bb = self.get_bounding_box()
        img = Image.new('L', (int(abs(scale * (bb[0].x - bb[1].x))), int(abs((scale * (bb[0].y - bb[1].y))))), 255)
        return ImageTk.PhotoImage(img)
