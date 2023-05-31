"""Fix antimeridian crossings in GeoJSON objects and shapely geometries."""

from ._implementation import (
    GeoInterface,
    bbox,
    fix_geojson,
    fix_multi_polygon,
    fix_polygon,
    fix_shape,
    segment_geojson,
    segment_shape,
)

__all__ = [
    "bbox",
    "fix_polygon",
    "fix_geojson",
    "fix_multi_polygon",
    "fix_shape",
    "GeoInterface",
    "segment_geojson",
    "segment_shape",
]
