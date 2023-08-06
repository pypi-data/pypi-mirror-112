import logging

import numpy as np
import tripy
from func_timeout import FunctionTimedOut, func_timeout
from scipy.spatial import ConvexHull
from sect.decomposition import polygon_trapezoidal
from sect.triangulation import constrained_delaunay_triangles

from map_analyser.lib.poly_decomp import polygonDecomp, polygonQuickDecomp
from map_analyser.lib.py2D import Polygon
from .util import paths_to_areas


def _decomp1(area):
    ret = polygon_trapezoidal([(x, y) for x, y in area.coords_zipped])
    return paths_to_areas(ret, area)  # returns some graph object, which would have to be interpreted


def _decomp2(area):
    ret = polygonDecomp([(x, y) for x, y in area.coords_zipped])
    return paths_to_areas(ret, area)


def _decomp3(area):
    ret = polygonQuickDecomp([(x, y) for x, y in area.coords_zipped])
    return paths_to_areas(ret, area)


def _triangulate2(area):
    ret = constrained_delaunay_triangles(area.coords_zipped)
    return paths_to_areas(ret, area)


def _triangulate1(area):
    ret = tripy.earclip(area.coords_zipped)
    return paths_to_areas(ret, area)


def _decomp4(area):
    try:
        ret = func_timeout(10, Polygon.convex_decompose, args=(Polygon.from_tuples(area.coords_zipped),
                                                               [Polygon.from_tuples(hole) for hole in area.holes]))

    except FunctionTimedOut:
        logging.warning(f"Decomposition of {area} timed out.")
        return []
    convex_polygons = [[p.as_tuple() for p in polyg.points] for polyg in ret]
    ret = paths_to_areas(convex_polygons, area)

    return ret


def decompose(area):
    return _decomp4(area)


def convex_hull(areas, return_area):
    hull = ConvexHull(np.transpose(np.concatenate([np.asarray(a.coords) for a in areas], axis=1)))

    return paths_to_areas([hull.points[hull.vertices]], return_area)
