import logging

import pyclipper as pcl

from map_analyser import maplib as ml

from .util import (intersects, paths_to_areas, paths_to_holes,
                   poly_tree_to_areas)


def orientation(coords):
    return pcl.Orientation(coords)


def merge(areas, return_area=None):
    """
    Performs union on list of Areas
    :param areas: list of Areas
    :param return_area: Sample area, whose properties determine returned areas
    :return: list of Areas
    """
    if len(areas) == 0:
        return []
    if return_area is None:
        return_area = areas[0]

    pc = pcl.Pyclipper()
    pc.StrictlySimple = True

    for area in areas:
        try:
            pc.AddPath(area.coords_zipped, pcl.PT_SUBJECT, True)
        except Exception as ex:
            logging.warn(f"Skipping {area.coords_zipped} because of {ex}")
            continue
        for hole in area.holes:
            try:
                pc.AddPath(hole, pcl.PT_SUBJECT, True)
            except Exception as ex:
                logging.warn(f"Skipping hole {hole} because of {ex}")
                continue

    if areas[0].ORIENTATION:
        solution = pc.Execute2(pcl.CT_UNION, pcl.PFT_POSITIVE, pcl.PFT_POSITIVE)
    else:
        solution = pc.Execute2(pcl.CT_UNION, pcl.PFT_NEGATIVE, pcl.PFT_NEGATIVE)

    return poly_tree_to_areas(solution, return_area)


def clip(areas, cropped_areas):
    """
    Crops all cropped areas by all areas
    :param areas: Areas which are subtracted
    :param cropped_areas: Areas which are cropped
    :return: all cropped_areas after subtraction of all areas
    """

    if len(cropped_areas) == 0:
        return []

    for clip in areas:
        tmp = []

        for subject in cropped_areas:
            if intersects(clip.get_bb(), subject.get_bb()):
                pc = pcl.Pyclipper()
                pc.StrictlySimple = True

                pc.AddPath(subject.coords_zipped, pcl.PT_SUBJECT, True)
                pc.AddPath(clip.coords_zipped, pcl.PT_CLIP, True)

                for hole in subject.holes:
                    pc.AddPath(hole, pcl.PT_SUBJECT, True)
                for hole in clip.holes:
                    pc.AddPath(hole, pcl.PT_CLIP, True)

                # even odd rule makes sence for single polygon
                solution = pc.Execute2(pcl.CT_DIFFERENCE, pcl.PFT_EVENODD, pcl.PFT_EVENODD)

                solution = poly_tree_to_areas(solution, subject)

                # there were some dead end edges left
                tmp.extend(clean(solution))
            else:
                tmp.extend(clean([subject]))
        cropped_areas = tmp

    return cropped_areas


def simplify(area):
    """
    Removes self intersections.
    :param area: Area
    :return: list of Areas
    """
    return merge([area], area)


def clean(areas):
    """
    Removes unnecessary edges and vertices.
    :param areas: list of Areas
    :return: list of Areas
    """
    ret = []
    for area in areas:
        tmp = paths_to_areas([pcl.CleanPolygon(area.coords_zipped)], area)[0]

        tmp = paths_to_holes([pcl.CleanPolygon(h) for h in area.holes], tmp)
        ret.append(tmp)

    # delete invalid holes
    for a in ret:
        holes = []
        for h in a.holes:
            if len(h) > 2:
                holes.append(h)
        a.holes = holes

    return ret


def offset(area, off=200):
    """
    Offsets area (line or area symbol) by off
    :param area: Area to be offset
    :param off: width of offset
    :return: list of offseted areas
    """
    pco = pcl.PyclipperOffset()

    if area.symbol_type == ml.Symbol.AREA_SYMBOL:
        pco.AddPath(area.coords_zipped, pcl.JT_SQUARE, pcl.ET_CLOSEDPOLYGON)
    elif area.symbol_type == ml.Symbol.LINE_SYMBOL:
        pco.AddPath(area.coords_zipped + area.coords_zipped[::-1], pcl.JT_SQUARE, pcl.ET_OPENSQUARE)
        area.symbol_type = ml.Symbol.AREA_SYMBOL
    solution = pco.Execute2(off)

    return poly_tree_to_areas(solution, area)
