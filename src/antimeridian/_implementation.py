"""Implementation module for the antimeridian package.

This is a "private" module that is not part of our public API. Downstream users
should not use these functions and objects directly; instead, use the functions
explicitly imported into the top-level of the package. The interfaces in this
module can change at any time without warning.
"""

from __future__ import annotations

import copy
import itertools
import warnings
from collections import namedtuple
from typing import Any, Dict, List, Optional, Protocol, Tuple, Union, cast

import numpy
import shapely
import shapely.affinity
import shapely.geometry
import shapely.validation
from shapely.geometry import (
    LinearRing,
    LineString,
    MultiLineString,
    MultiPolygon,
    Point,
    Polygon,
)

XY = Tuple[float, float]


class AntimeridianWarning(UserWarning):
    """Base class for all package-specific warnings."""


class FixWindingWarning(AntimeridianWarning):
    """The input shape is wound clockwise (instead of counter-clockwise), so
    this package is reversing the winding order before fixing the shape.
    """

    MESSAGE = (
        "The exterior ring of this shape is wound "
        "clockwise. Since this is a common error in real-world "
        "geometries, this package is reversing the exterior coordinates of the "
        "input shape before running its algorithm. If you know that your input "
        "shape is correct (i.e. if your data encompasses both poles), pass "
        "`fix_winding=False`."
    )

    @classmethod
    def warn(cls) -> None:
        warnings.warn(cls.MESSAGE, cls, stacklevel=2)


class GeoInterface(Protocol):
    """A simple protocol for things that have a `__geo_interface__` method.

    The `__geo_interface__` protocol is described
    [here](https://gist.github.com/sgillies/2217756>), and is used within
    [shapely](https://shapely.readthedocs.io/en/stable/manual.html) to extract
    geometries from objects.
    """

    @property
    def __geo_interface__(self) -> Dict[str, Any]: ...


def fix_geojson(
    geojson: Dict[str, Any],
    *,
    force_north_pole: bool = False,
    force_south_pole: bool = False,
    fix_winding: bool = True,
) -> Dict[str, Any]:
    """Fixes a GeoJSON object that crosses the antimeridian.

    If the object does not cross the antimeridian, it is returned unchanged.

    See [antimeridian.fix_polygon][] for a description of the `force_north_pole`
    `force_south_pole` and `fix_winding` arguments.

    Args:
        geojson: A GeoJSON object as a dictionary
        force_north_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the north pole.
        force_south_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the south pole.
        fix_winding: If the polygon is wound clockwise, reverse its
            coordinates before applying the algorithm.

    Return:
        The same GeoJSON with a fixed geometry or geometries
    """
    type_ = geojson.get("type", None)
    if type_ is None:
        raise ValueError("no 'type' field found in GeoJSON")
    elif type_ == "Feature":
        geometry = geojson.get("geometry", None)
        if geometry is None:
            raise ValueError("no 'geometry' field found in GeoJSON Feature")
        geojson["geometry"] = fix_shape(
            geometry,
            force_north_pole=force_north_pole,
            force_south_pole=force_south_pole,
            fix_winding=fix_winding,
        )
        return geojson
    elif type_ == "FeatureCollection":
        features = geojson.get("features", None)
        if features is None:
            raise ValueError("no 'features' field found in GeoJSON FeatureCollection")
        for i, feature in enumerate(features):
            features[i] = fix_geojson(
                feature,
                force_north_pole=force_north_pole,
                force_south_pole=force_south_pole,
                fix_winding=fix_winding,
            )
        geojson["features"] = features
        return geojson
    else:
        return fix_shape(
            geojson,
            force_north_pole=force_north_pole,
            force_south_pole=force_south_pole,
            fix_winding=fix_winding,
        )


def segment_geojson(geojson: Dict[str, Any]) -> MultiLineString:
    """Segments a GeoJSON object into a MultiLineString.

    If the object does not cross the antimeridian, its exterior and interior
    line strings are returned unchanged.

    Args:
        geojson: A GeoJSON object as a dictionary

    Return:
        A MutliLineString of segments.
    """
    type_ = geojson.get("type", None)
    if type_ is None:
        raise ValueError("no 'type' field found in GeoJSON")
    elif type_ == "Feature":
        geometry = geojson.get("geometry", None)
        if geometry is None:
            raise ValueError("no 'geometry' field found in GeoJSON Feature")
        return MultiLineString(segment_shape(geometry))
    elif type_ == "FeatureCollection":
        features = geojson.get("features", None)
        if features is None:
            raise ValueError("no 'features' field found in GeoJSON FeatureCollection")
        segments = list()
        for feature in features:
            segments.extend(segment_geojson(feature))
        return MultiLineString(segments)
    else:
        return MultiLineString(segment_shape(geojson))


def fix_shape(
    shape: Dict[str, Any] | GeoInterface,
    *,
    force_north_pole: bool = False,
    force_south_pole: bool = False,
    fix_winding: bool = True,
) -> Dict[str, Any]:
    """Fixes a shape that crosses the antimeridian.

    See [antimeridian.fix_polygon][] for a description of the `force_north_pole`
    `force_south_pole` and `fix_winding` arguments.

    Args:
        shape: A polygon, multi-polygon, line string, or multi-line string,
            either as a dictionary or as a [antimeridian.GeoInterface][]. Uses
            [shapely.geometry.shape][] under the hood.
        force_north_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the north pole.
        force_south_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the south pole.
        fix_winding: If the polygon is wound clockwise, reverse its
            coordinates before applying the algorithm.

    Returns:
        The fixed shape as a dictionary
    """
    geom = shapely.geometry.shape(shape)
    if geom.geom_type == "Polygon":
        return cast(
            Dict[str, Any],
            shapely.geometry.mapping(
                fix_polygon(
                    geom,
                    force_north_pole=force_north_pole,
                    force_south_pole=force_south_pole,
                    fix_winding=fix_winding,
                )
            ),
        )
    elif geom.geom_type == "MultiPolygon":
        return cast(
            Dict[str, Any],
            shapely.geometry.mapping(
                fix_multi_polygon(
                    geom,
                    force_north_pole=force_north_pole,
                    force_south_pole=force_south_pole,
                    fix_winding=fix_winding,
                )
            ),
        )
    elif geom.geom_type == "LineString":
        return cast(Dict[str, Any], shapely.geometry.mapping(fix_line_string(geom)))
    elif geom.geom_type == "MultiLineString":
        return cast(
            Dict[str, Any], shapely.geometry.mapping(fix_multi_line_string(geom))
        )
    else:
        raise ValueError(f"unsupported geom_type: {geom.geom_type}")


def segment_shape(shape: Dict[str, Any] | GeoInterface) -> List[List[XY]]:
    geom = shapely.geometry.shape(shape)
    if geom.geom_type == "Polygon":
        return segment_polygon(geom)
    elif geom.geom_type == "MultiPolygon":
        segments = list()
        for polygon in geom.geoms:
            segments += segment_polygon(polygon)
        return segments
    else:
        raise ValueError(f"unsupported geom_type: {geom.geom_type}")


def fix_multi_polygon(
    multi_polygon: MultiPolygon,
    *,
    force_north_pole: bool = False,
    force_south_pole: bool = False,
    fix_winding: bool = True,
) -> MultiPolygon:
    """Fixes a [shapely.MultiPolygon][].

    See [antimeridian.fix_polygon][] for a description of the `force_north_pole`
    `force_south_pole` and `fix_winding` arguments.

    Args:
        multi_polygon: The multi-polygon
        force_north_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the north pole.
        force_south_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the south pole.
        fix_winding: If the polygon is wound clockwise, reverse its
            coordinates before applying the algorithm.

    Returns:
        The fixed multi-polygon
    """
    polygons = list()
    for polygon in multi_polygon.geoms:
        polygons += fix_polygon_to_list(
            polygon,
            force_north_pole=force_north_pole,
            force_south_pole=force_south_pole,
            fix_winding=fix_winding,
        )
    return MultiPolygon(polygons)


def fix_polygon(
    polygon: Polygon,
    *,
    force_north_pole: bool = False,
    force_south_pole: bool = False,
    fix_winding: bool = True,
) -> Union[Polygon, MultiPolygon]:
    """Fixes a [shapely.Polygon][].

    If the input polygon is wound clockwise, it will be fixed to be wound
    counterclockwise _unless_ `fix_winding` is `False` in which case it
    will be corrected by adding a counterclockwise polygon from (-180, -90) to
    (180, 90) as its exterior.

    In rare cases, the underlying algorithm might need a little help to fix the polygon.
    For example, a polygon that just barely crosses over a pole might have very
    few points at high latitudes, leading to ambiguous antimeridian crossing
    points and invalid geometries. We provide two flags, `force_north_pole`
    and `force_south_pole` for those cases. Most users can ignore these
    flags.

    If either `force_north_pole` or `force_south_pole` is `True`
    `fix_winding` is set to `False`

    Args:
        polygon: The input polygon
        force_north_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the north pole.
        force_south_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the south pole.
        fix_winding: If the polygon is wound clockwise, reverse its
            coordinates before applying the algorithm.

    Returns:
        The fixed polygon, either as a single polygon or a multi-polygon (if it
        was split)
    """
    if force_north_pole or force_south_pole:
        fix_winding = False
    polygons = fix_polygon_to_list(
        polygon,
        force_north_pole=force_north_pole,
        force_south_pole=force_south_pole,
        fix_winding=fix_winding,
    )
    if len(polygons) == 1:
        polygon = polygons[0]
        if shapely.is_ccw(polygon.exterior):
            return polygon
        else:
            return Polygon(
                [(-180, 90), (-180, -90), (180, -90), (180, 90)],
                [polygon.exterior.coords],
            )
    else:
        return MultiPolygon(polygons)


def fix_line_string(line_string: LineString) -> Union[LineString, MultiLineString]:
    """Fixes a [shapely.LineString][].

    Args:
        line_string: The input line string

    Returns:
        The fixed line string, either as a single line string or a multi-line
        string (if it was split)
    """
    segments = segment(list(line_string.coords))
    if not segments:
        return line_string
    else:
        return MultiLineString(segments)


def fix_multi_line_string(multi_line_string: MultiLineString) -> MultiLineString:
    """Fixes a [shapely.MultiLineString][].

    Args:
        multi_line_string: The input multi line string

    Returns:
        The fixed multi line string
    """
    line_strings = list()
    for line_string in multi_line_string.geoms:
        fixed = fix_line_string(line_string)
        if isinstance(fixed, LineString):
            line_strings.append(fixed)
        else:
            line_strings.extend(fixed.geoms)
    return MultiLineString(line_strings)


def segment_polygon(polygon: Polygon) -> List[List[XY]]:
    segments = segment(list(polygon.exterior.coords))
    if not segments:
        segments = [list(polygon.exterior.coords)]
    for interior in polygon.interiors:
        interior_segments = segment(list(interior.coords))
        if interior_segments:
            segments.extend(interior_segments)
        else:
            segments.append(list(interior.coords))
    return segments


def fix_polygon_to_list(
    polygon: Polygon,
    *,
    force_north_pole: bool,
    force_south_pole: bool,
    fix_winding: bool,
) -> List[Polygon]:
    exterior = normalize(list(polygon.exterior.coords))
    segments = segment(exterior)
    if not segments:
        polygon = Polygon(shell=exterior, holes=polygon.interiors)
        if fix_winding and (
            not shapely.is_ccw(polygon.exterior)
            or any(shapely.is_ccw(interior) for interior in polygon.interiors)
        ):
            FixWindingWarning.warn()
            return [shapely.geometry.polygon.orient(polygon)]
        else:
            return [polygon]
    else:
        interiors = []
        for interior in polygon.interiors:
            interior_segments = segment(list(interior.coords))
            if interior_segments:
                if fix_winding:
                    unwrapped_linearring = LinearRing(
                        list((x % 360, y) for x, y in interior.coords)
                    )
                    if shapely.is_ccw(unwrapped_linearring):
                        FixWindingWarning.warn()
                        interior_segments = segment(list(reversed(interior.coords)))
                segments.extend(interior_segments)
            else:
                interiors.append(interior)
    segments = extend_over_poles(
        segments,
        force_north_pole=force_north_pole,
        force_south_pole=force_south_pole,
        fix_winding=fix_winding,
    )
    polygons = build_polygons(segments)
    assert polygons
    for i, polygon in enumerate(polygons):
        for j, interior in enumerate(interiors):
            if polygon.contains(interior):
                interior = interiors.pop(j)
                polygon_interiors = list(polygon.interiors)
                polygon_interiors.append(interior)
                polygons[i] = Polygon(polygon.exterior, polygon_interiors)
    assert not interiors
    return polygons


def normalize(coords: List[XY]) -> List[XY]:
    original = list(coords)
    all_are_on_antimeridian = True
    for i, point in enumerate(coords):
        # Ensure all longitudes are between -180 and 180, and that tiny floating
        # point differences are ignored.
        if numpy.isclose(point[0], 180):
            # https://github.com/gadomski/antimeridian/issues/81
            if abs(coords[i][1]) != 90 and numpy.isclose(
                coords[(i - 1) % len(coords)][0], -180
            ):
                coords[i] = (-180, point[1])
            else:
                coords[i] = (180, point[1])
        elif numpy.isclose(point[0], -180):
            # https://github.com/gadomski/antimeridian/issues/81
            if abs(coords[i][1]) != 90 and numpy.isclose(
                coords[(i - 1) % len(coords)][0], 180
            ):
                coords[i] = (180, point[1])
            else:
                coords[i] = (-180, point[1])
        else:
            coords[i] = (((point[0] + 180) % 360) - 180, point[1])
            all_are_on_antimeridian = False
        if len(point) > 2:
            point_as_list = list(coords[i])
            point_as_list.extend(point[2:])
            coords[i] = tuple(point_as_list)
    if all_are_on_antimeridian:
        return original
    else:
        return coords


def segment(coords: List[XY]) -> List[List[XY]]:
    segment = []
    segments = []
    for start, end in itertools.pairwise(coords):
        segment.append(start)
        if (end[0] - start[0] > 180) and (end[0] - start[0] != 360):  # left
            latitude = crossing_latitude(start, end)
            segment.append((-180, latitude))
            segments.append(segment)
            segment = [(180, latitude)]
        elif (start[0] - end[0] > 180) and (start[0] - end[0] != 360):  # right
            latitude = crossing_latitude(end, start)
            segment.append((180, latitude))
            segments.append(segment)
            segment = [(-180, latitude)]
    if not segments:
        # No antimeridian crossings
        return []
    elif coords[-1] == segments[0][0]:
        # Join polygons
        segments[0] = segment + segments[0]
    else:
        segment.append(coords[-1])
        segments.append(segment)
    return segments


def crossing_latitude(start: XY, end: XY) -> float:
    if abs(start[0]) == 180:
        return start[1]
    elif abs(end[0]) == 180:
        return end[1]
    latitude_delta = end[1] - start[1]
    if end[0] > 0:
        return round(
            start[1]
            + (180.0 - start[0]) * latitude_delta / (end[0] + 360.0 - start[0]),
            7,
        )
    else:
        return round(
            start[1]
            + (start[0] + 180.0) * latitude_delta / (start[0] + 360.0 - end[0]),
            7,
        )


IndexAndLatitude = namedtuple("IndexAndLatitude", "index latitude")


def extend_over_poles(
    segments: List[List[XY]],
    *,
    force_north_pole: bool,
    force_south_pole: bool,
    fix_winding: bool,
) -> List[List[XY]]:
    left_start = None
    right_start = None
    left_end = None
    right_end = None
    for i, segment in enumerate(segments):
        if segment[0][0] == -180 and (
            left_start is None or segment[0][1] < left_start.latitude
        ):
            left_start = IndexAndLatitude(i, segment[0][1])
        elif segment[0][0] == 180 and (
            right_start is None or segment[0][1] > right_start.latitude
        ):
            right_start = IndexAndLatitude(i, segment[0][1])
        if segment[-1][0] == -180 and (
            left_end is None or segment[-1][1] < left_end.latitude
        ):
            left_end = IndexAndLatitude(i, segment[-1][1])
        elif segment[-1][0] == 180 and (
            right_end is None or segment[-1][1] > right_end.latitude
        ):
            right_end = IndexAndLatitude(i, segment[-1][1])

    is_over_north_pole = False
    is_over_south_pole = False
    original_segments = copy.deepcopy(segments)

    # If there's no segment ends between a start and the pole, extend the
    # segment over the pole.
    if left_end:
        if (
            (force_north_pole and not force_south_pole)
            and not right_end  # Total hack to skip the force if we're going to
            # add points later from the right side
            and (not left_start or left_end.latitude > left_start.latitude)
        ):
            is_over_north_pole = True
            segments[left_end.index] += [(-180, 90), (180, 90)]
            segments[left_end.index].reverse()
        elif (
            force_south_pole
            or not left_start
            or left_end.latitude < left_start.latitude
        ):
            is_over_south_pole = True
            segments[left_end.index] += [(-180, -90), (180, -90)]
    if right_end:
        if (force_south_pole and not force_north_pole) and (
            not right_start or right_end.latitude < right_start.latitude
        ):
            is_over_south_pole = True
            segments[right_end.index] += [(180, -90), (-180, -90)]
            segments[right_end.index].reverse()
        elif (
            force_north_pole
            or not right_start
            or right_end.latitude > right_start.latitude
        ):
            is_over_north_pole = True
            segments[right_end.index] += [(180, 90), (-180, 90)]
    if fix_winding and is_over_north_pole and is_over_south_pole:
        # These assertions are here because we're assuming that we set
        # `fix_winding` to `False` up in `fix_polygon` if either of the
        # `force_*` variables are set.
        assert not force_north_pole
        assert not force_south_pole

        # If we're over both poles and we haven't explicitly disabled the
        # fix behavior, reverse all segments, effectively reversing the
        # winding order.
        FixWindingWarning.warn()
        for segment in original_segments:
            segment.reverse()
        return original_segments
    else:
        return segments


def build_polygons(
    segments: List[List[XY]],
) -> List[Polygon]:
    if not segments:
        return []
    segment = segments.pop()
    is_right = segment[-1][0] == 180
    candidates: List[Tuple[Optional[int], float]] = list()
    if is_self_closing(segment):
        # Self-closing segments might end up joining up with themselves. They
        # might not, e.g. donuts.
        candidates.append((None, segment[0][1]))
    for i, s in enumerate(segments):
        # Is the start of s on the same side as the end of segment?
        if s[0][0] == segment[-1][0]:
            # If so, check the following:
            # - Is the start of s closer to the pole than the end of segment, and
            # - is the end of s on the other side, or
            # - is the end of s further away from the pole than the start of
            #   segment (e.g. donuts)?
            if (
                is_right
                and s[0][1] > segment[-1][1]
                and (not is_self_closing(s) or s[-1][1] < segment[0][1])
            ) or (
                not is_right
                and s[0][1] < segment[-1][1]
                and (not is_self_closing(s) or s[-1][1] > segment[0][1])
            ):
                candidates.append((i, s[0][1]))

    # Sort the candidates so the closest point is first in the list.
    candidates.sort(key=lambda c: c[1], reverse=not is_right)
    if candidates:
        index = candidates[0][0]
    else:
        index = None

    if index is not None:
        # Join the segments, then re-add them to the list and recurse.
        segment = segment + segments.pop(index)
        segments.append(segment)
        return build_polygons(segments)
    else:
        # This segment should self-joining, so just build the rest of the
        # polygons without it.
        polygons = build_polygons(segments)
        if not all(p == segment[0] for p in segment):
            # If every point is the same, then we don't need it in the output
            # set of polygons. This happens if, e.g., one corner of an input
            # polygon is on the antimeridian.
            # https://github.com/gadomski/antimeridian/issues/45#issuecomment-1614586166
            polygons.append(Polygon(segment))
        return polygons


def is_self_closing(segment: List[XY]) -> bool:
    is_right = segment[-1][0] == 180
    return segment[0][0] == segment[-1][0] and (
        (is_right and segment[0][1] > segment[-1][1])
        or (not is_right and segment[0][1] < segment[-1][1])
    )


def bbox(
    shape: Dict[str, Any] | GeoInterface, force_over_antimeridian: bool = False
) -> List[float]:
    """Calculates a GeoJSON-spec conforming bounding box for a shape.

    Per the [GeoJSON
    spec](https://datatracker.ietf.org/doc/html/rfc7946#section-5.2), an
    antimeridian-spanning bounding box should have its larger longitude as its
    first bounding box coordinate.

    Args:
        shape: The polygon or multipolygon for which to calculate the bounding box.
        force_over_antimeridian: Force the bounding box to be over the antimeridian.

    Returns:
        List[float]: The bounding box.
    """
    geom = shapely.geometry.shape(shape)
    if geom.geom_type == "Polygon":
        return list(geom.bounds)
    elif geom.geom_type == "MultiPolygon":
        crosses_antimeridian = False
        xmins = list()
        ymin = 90
        xmaxs = list()
        ymax = -90
        for polygon in geom.geoms:
            bounds = polygon.bounds
            xmins.append(bounds[0])
            if bounds[1] < ymin:
                ymin = bounds[1]
            xmaxs.append(bounds[2])
            if bounds[3] > ymax:
                ymax = bounds[3]
            if is_coincident_to_antimeridian(polygon) and not (
                bounds[0] == -180 and bounds[2] == 180
            ):
                crosses_antimeridian = True

        if crosses_antimeridian or force_over_antimeridian:
            return [max(xmins), ymin, min(xmaxs), ymax]
        else:
            return [min(xmins), ymin, max(xmaxs), ymax]
    else:
        raise ValueError(
            f"unsupported geom_type for bbox calculation: {geom.geom_type}"
        )


def centroid(shape: Dict[str, Any] | GeoInterface) -> Point:
    """Calculates the centroid for a polygon or multipolygon.

    Polygons are easy, we just use [shapely.centroid][]. For
    multi-polygons, the antimeridian is taken into account by calculating the
    centroid from an identical multi-polygon with coordinates in [0, 360).

    Args:
        shape: The polygon or multipolygon for which to calculate the centroid.

    Returns:
        Point: The centroid.
    """
    # Inspired by
    # https://github.com/stactools-packages/sentinel2/blob/f90f5fa006459e9bb59bfd327d9199e5259ec4a7/src/stactools/sentinel2/stac.py#L192-L208
    geom = shapely.geometry.shape(shape)
    if geom.geom_type == "Polygon":
        return cast(Point, geom.centroid)
    elif geom.geom_type == "MultiPolygon":
        geoms = list()
        for component in geom.geoms:
            if any(c[0] < 0 for c in component.exterior.coords):
                geoms.append(shapely.affinity.translate(component, xoff=+360))
            else:
                geoms.append(component)
        centroid = cast(
            Point, shapely.validation.make_valid(MultiPolygon(geoms)).centroid
        )
        if centroid.x > 180:
            centroid = Point(centroid.x - 360, centroid.y)
        return centroid
    else:
        raise ValueError(
            f"unsupported geom_type for centroid calculation: {geom.geom_type}"
        )


def is_coincident_to_antimeridian(polygon: Polygon) -> bool:
    for start, end in zip(polygon.exterior.coords, polygon.exterior.coords[1:]):
        if abs(start[0]) == 180 and start[0] == end[0]:
            return True
    return False
