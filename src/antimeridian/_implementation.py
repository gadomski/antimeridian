from __future__ import annotations

from typing import List, Tuple, Union

from shapely.geometry import MultiPolygon, Polygon

Point = Tuple[float, float]


def fix_polygon(polygon: Polygon) -> Union[Polygon, MultiPolygon]:
    if bool(polygon.interiors):
        raise ValueError("cannot fix a polygon with interior rings")
    # TODO check for validity so we don't correct already-corrected
    # TODO test for 3D points
    coords = polygon.exterior.coords
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
        return Polygon(segment)
    elif coords[-1] == segments[0][0]:
        segments[0] = segment + segments[0]
        segment = []
    else:
        raise ValueError("geometry does not start and end with the same point")

    polygons = build_polygons(segments)
    assert polygons
    if len(polygons) > 1:
        return MultiPolygon(polygons)
    else:
        return polygons[0]


def crossing_latitude(start: Point, end: Point) -> float:
    # TODO test this
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


def build_polygons(
    segments: List[List[Point]],
) -> List[Polygon]:
    if not segments:
        return []
    segment = segments.pop()
    right = (
        segment[-1][0] == 180
    )  # all segments should start and end at abs(180) longitude
    candidates = list()  # list of (index, latitude, is_start)
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
        # Join the polygons then recurse.
        segment = segments.pop(index) + segment
        segments.append(segment)
        return build_polygons(segments)

    if segment[0][0] == segment[-1][0]:
        if (right and segment[0][1] > segment[-1][1]) or (
            not right and segment[0][1] < segment[-1][1]
        ):
            # This is a closed section that doesn't touch a pole, so we can let
            # shapely close the polygon itself.
            polygons = build_polygons(segments)
            polygons.append(Polygon(segment))
            return polygons

        # This is a "loop" on the antimeridian that needs to extend up to
        # the pole. Add the pole points, then recurse with the new segment
        # next up. We insert this segment at the front so we process it next
        # again -- the start might not be linked up right, so we need to ensure
        # we use its new end right away. AKA its hacky.
        elif segment[-1][0] == 180:
            # North pole
            segment.append((180, 90))
            segment.append((-180, 90))
            segments.insert(0, segment)
            return build_polygons(segments)
        else:
            # South pole
            segment.append((-180, -90))
            segment.append((180, -90))
            segments.insert(0, segment)
            return build_polygons(segments)

    # The segment goes all the way around the world (-180 to 180) and encloses a
    # pole.
    else:
        # Build the rest of the polygons
        polygons = build_polygons(segments)

        if segment[-1][0] == 180:
            # North pole
            segment.append((180, 90))
            segment.append((-180, 90))
            polygons.append(Polygon(segment))
        else:
            # South pole
            segment.append((-180, -90))
            segment.append((180, -90))
            polygons.append(Polygon(segment))

        return polygons
