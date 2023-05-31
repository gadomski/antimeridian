"""Implementation module for the antimeridian package.

This is a "private" module that is not part of our public API. Downstream users
should not use these functions and objects directly; instead, use the functions
explicitly imported into the top-level of the package. The interfaces in this
module can change at any time without warning.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol, Tuple, Union, cast

import shapely
import shapely.geometry
from shapely.geometry import MultiLineString, MultiPolygon, Polygon

Point = Tuple[float, float]


class GeoInterface(Protocol):
    """A simple protocol for things that have a ``__geo_interface__`` method.

    The ``__geo_interface__`` protocol is described `here
    <https://gist.github.com/sgillies/2217756>`_, and is used within `shapely
    <https://shapely.readthedocs.io/en/stable/manual.html>`_ to
    extract geometries from objects.
    """

    def __geo_interface__(self) -> Dict[str, Any]:
        ...


def fix_geojson(
    geojson: Dict[str, Any],
    *,
    force_north_pole: bool = False,
    force_south_pole: bool = False,
) -> Dict[str, Any]:
    """Fixes a GeoJSON object that crosses the antimeridian.

    If the object does not cross the antimeridian, it is returned unchanged.

    See :py:func:`fix_polygon` for a description of the ``force_north_pole`` and
    ``force_south_pole`` arguments.

    Args:
        geojson: A GeoJSON object as a dictionary
        force_north_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the north pole.
        force_south_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the south pole.

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
            )
        geojson["features"] = features
        return geojson
    else:
        return fix_shape(
            geojson,
            force_north_pole=force_north_pole,
            force_south_pole=force_south_pole,
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
) -> Dict[str, Any]:
    """Fixes a shape that crosses the antimeridian.

    See :py:func:`fix_polygon` for a description of the ``force_north_pole`` and
    ``force_south_pole`` arguments.

    Args:
        shape: A polygon or multi-polygon, either as a dictionary or as a
            :py:class:`GeoInterface`. Uses :py:func:`shapely.geometry.shape`
            under the hood.
        force_north_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the north pole.
        force_south_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the south pole.

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
                )
            ),
        )
    else:
        raise ValueError(f"unsupported geom_type: {geom.geom_type}")


def segment_shape(shape: Dict[str, Any] | GeoInterface) -> List[List[Point]]:
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
) -> MultiPolygon:
    """Fixes a :py:class:`shapely.geometry.MultiPolygon`.

    See :py:func:`fix_polygon` for a description of the ``force_north_pole`` and
    ``force_south_pole`` arguments.

    Args:
        multi_polygon: The multi-polygon
        force_north_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the north pole.
        force_south_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the south pole.

    Returns:
        The fixed multi-polygon
    """
    polygons = list()
    for polygon in multi_polygon.geoms:
        polygons += fix_polygon_to_list(
            polygon,
            force_north_pole=force_north_pole,
            force_south_pole=force_south_pole,
        )
    return MultiPolygon(polygons)


def fix_polygon(
    polygon: Polygon, *, force_north_pole: bool = False, force_south_pole: bool = False
) -> Union[Polygon, MultiPolygon]:
    """Fixes a :py:class:`shapely.geometry.Polygon`.

    If the input polygon is a single polygon that is wound clockwise and doesn't
    cross the antimeridian, it will be corrected by adding a counter-clockwise
    polygon from (-180, -90) to (180, 90) as its exterior.

    In rare cases, the underlying algorithm might need a little help to fix the polygon.
    For example, a polygon that just barely crosses over a pole might have very
    few points at high latitudes, leading to ambiguous antimeridian crossing
    points and invalid geometries. We provide two flags, ``force_north_pole``
    and ``force_south_pole``, for those cases. Most users can ignore these
    flags.

    Args:
        polygon: The input polygon
        force_north_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the north pole.
        force_south_pole: If the polygon crosses the antimeridian, force the
            joined segments to enclose the south pole.

    Returns:
        The fixed polygon, either as a single polygon or a multi-polygon (if it
        was split)
    """
    polygons = fix_polygon_to_list(
        polygon, force_north_pole=force_north_pole, force_south_pole=force_south_pole
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


def segment_polygon(polygon: Polygon) -> List[List[Point]]:
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
    polygon: Polygon, *, force_north_pole: bool, force_south_pole: bool
) -> List[Polygon]:
    segments = segment(list(polygon.exterior.coords))
    if not segments:
        return [polygon]
    else:
        interiors = []
        for interior in polygon.interiors:
            interior_segments = segment(list(interior.coords))
            if interior_segments:
                segments.extend(interior_segments)
            else:
                interiors.append(interior)
    segments = extend_over_poles(
        segments, force_north_pole=force_north_pole, force_south_pole=force_south_pole
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


def segment(coords: List[Point]) -> List[List[Point]]:
    segment = []
    segments = []
    for i, point in enumerate(coords):
        # Ensure all longitudes are between -180 and 180
        if point[0] != 180:
            coords[i] = (((point[0] + 180) % 360) - 180, point[1])
    for start, end in zip(coords, coords[1:]):
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
    return segments


def crossing_latitude(start: Point, end: Point) -> float:
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


def extend_over_poles(
    segments: List[List[Point]],
    *,
    force_north_pole: bool,
    force_south_pole: bool,
) -> List[List[Point]]:
    left_starts = list()
    right_starts = list()
    left_ends = list()
    right_ends = list()
    for i, segment in enumerate(segments):
        if segment[0][0] == -180:
            left_starts.append((i, segment[0][1]))
        else:
            right_starts.append((i, segment[0][1]))
        if segment[-1][0] == -180:
            left_ends.append((i, segment[-1][1]))
        else:
            right_ends.append((i, segment[-1][1]))
    left_ends.sort(key=lambda v: v[1])
    left_starts.sort(key=lambda v: v[1])
    right_ends.sort(key=lambda v: v[1], reverse=True)
    right_starts.sort(key=lambda v: v[1], reverse=True)
    # If there's no segment ends between a start and the pole, extend the
    # segment over the pole.
    if left_ends and (
        force_south_pole or not left_starts or left_ends[0][1] < left_starts[0][1]
    ):
        segments[left_ends[0][0]] += [(-180, -90), (180, -90)]
    if right_ends and (
        force_north_pole or not right_starts or right_ends[0][1] > right_starts[0][1]
    ):
        segments[right_ends[0][0]] += [(180, 90), (-180, 90)]
    return segments


def build_polygons(
    segments: List[List[Point]],
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
        polygons.append(Polygon(segment))
        return polygons


def is_self_closing(segment: List[Point]) -> bool:
    is_right = segment[-1][0] == 180
    return segment[0][0] == segment[-1][0] and (
        (is_right and segment[0][1] > segment[-1][1])
        or (not is_right and segment[0][1] < segment[-1][1])
    )


def bbox(shape: Dict[str, Any] | GeoInterface) -> List[float]:
    """Calculates a GeoJSON-spec conforming bounding box for a shape.

    Per `the GeoJSON spec
    <https://datatracker.ietf.org/doc/html/rfc7946#section-5.2>`_, an
    antimeridian-spanning bounding box should have its larger longitude as its
    first bounding box coordinate.

    Args:
        shape: The polygon or multipolygon for which to calculate the bounding box.

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
            if is_coincident_to_antimeridian(polygon):
                crosses_antimeridian = True

        if crosses_antimeridian:
            return [max(xmins), ymin, min(xmaxs), ymax]
        else:
            return [min(xmins), ymin, max(xmaxs), ymax]
    else:
        raise ValueError(
            f"unsupported geom_type for bbox calculation: {geom.geom_type}"
        )


def is_coincident_to_antimeridian(polygon: Polygon) -> bool:
    for start, end in zip(polygon.exterior.coords, polygon.exterior.coords[1:]):
        if abs(start[0]) == 180 and start[0] == end[0]:
            return True
    return False
