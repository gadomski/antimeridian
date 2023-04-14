from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol, Tuple, Union, cast

import shapely.geometry
from shapely.geometry import MultiPolygon, Polygon

Point = Tuple[float, float]


class GeoInterface(Protocol):
    def __geo_interface__(self) -> Dict[str, Any]:
        ...


def fix_shape(shape: Dict[str, Any] | GeoInterface) -> Dict[str, Any]:
    geom = shapely.geometry.shape(shape)
    if geom.geom_type == "Polygon":
        return cast(Dict[str, Any], shapely.geometry.mapping(fix_polygon(geom)))
    elif geom.geom_type == "MultiPolygon":
        return cast(Dict[str, Any], shapely.geometry.mapping(fix_multi_polygon(geom)))
    else:
        raise ValueError(f"unsupported geom_type: {geom.geom_type}")


def fix_multi_polygon(multi_polygon: MultiPolygon) -> MultiPolygon:
    polygons = list()
    for polygon in multi_polygon.geoms:
        polygons += fix_polygon_to_list(polygon)
    return MultiPolygon(polygons)


def fix_polygon(polygon: Polygon) -> Union[Polygon, MultiPolygon]:
    polygons = fix_polygon_to_list(polygon)
    if len(polygons) == 1:
        return polygons[0]
    else:
        return MultiPolygon(polygons)


def fix_polygon_to_list(polygon: Polygon) -> List[Polygon]:
    segments = segment(polygon.exterior.coords)
    if not segments:
        return [polygon]
    else:
        interiors = []
        for interior in polygon.interiors:
            interior_segments = segment(interior.coords)
            if interior_segments:
                segments.extend(interior_segments)
            else:
                interiors.append(interior)
    segments = extend_over_poles(segments)
    polygons = build_polygons(segments)
    assert polygons
    for interior in interiors:
        for i, polygon in enumerate(polygons):
            if polygon.contains(interior):
                interiors = list(polygon.interiors)
                interiors.append(interior)
                polygons[i] = Polygon(polygon.exterior, interiors)
    return polygons


def segment(coords: List[Point]) -> List[List[Point]]:
    segment = []
    segments = []
    for start, end in zip(coords, coords[1:]):
        segment.append(start)
        if end[0] - start[0] > 180:  # left
            latitude = crossing_latitude(start, end)
            segment.append((-180, latitude))
            segments.append(segment)
            segment = [(180, latitude)]
        elif start[0] - end[0] > 180:  # right
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


def extend_over_poles(segments: List[List[Point]]) -> List[List[Point]]:
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
    if left_ends and (not left_starts or left_ends[0][1] < left_starts[0][1]):
        segments[left_ends[0][0]] += [(-180, -90), (180, -90)]
    if right_ends and (not right_starts or right_ends[0][1] > right_starts[0][1]):
        segments[right_ends[0][0]] += [(180, 90), (-180, 90)]
    return segments


def build_polygons(
    segments: List[List[Point]],
) -> List[Polygon]:
    if not segments:
        return []
    segment = segments.pop()
    right = (
        segment[-1][0] == 180
    )  # all segments should start and end at abs(180) longitude
    candidates: List[
        Tuple[Optional[int], float, bool]
    ] = list()  # list of (index, latitude, is_start)
    if segment[0][0] == segment[-1][0] and (
        (right and segment[0][1] > segment[-1][1])
        or (not right and segment[0][1] < segment[-1][1])
    ):
        candidates.append((None, segment[0][1], True))
    for i, s in enumerate(segments):
        if s[0][0] == segment[-1][0]:
            if (right and s[0][1] > segment[-1][1]) or (
                not right and s[0][1] < segment[-1][1]
            ):
                candidates.append((i, s[0][1], True))
        if s[-1][0] == segment[-1][0]:
            if (right and s[-1][1] > segment[-1][1]) or (
                not right and s[-1][1] < segment[-1][1]
            ):
                candidates.append((i, s[-1][1], False))
    candidates.sort(key=lambda c: c[1], reverse=not right)
    if candidates and candidates[0][2]:
        index = candidates[0][0]
    else:
        index = None

    if index is not None:
        segment = segments.pop(index) + segment
        segments.append(segment)
        return build_polygons(segments)
    else:
        polygons = build_polygons(segments)
        polygons.append(Polygon(segment))
        return polygons
