"""Fix antimeridian crossings in GeoJSON objects and shapely geometries."""

from ._implementation import (
    FixWindingWarning,
    GeoInterface,
    bbox,
    centroid,
    fix_geojson,
    fix_line_string,
    fix_multi_line_string,
    fix_multi_polygon,
    fix_polygon,
    fix_shape,
    segment_geojson,
    segment_shape,
)

__all__ = [
    "FixWindingWarning",
    "GeoInterface",
    "bbox",
    "centroid",
    "fix_geojson",
    "fix_line_string",
    "fix_multi_line_string",
    "fix_multi_polygon",
    "fix_polygon",
    "fix_shape",
    "segment_geojson",
    "segment_shape",
]
