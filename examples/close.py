import json
import sys

import shapely.geometry

import antimeridian

with open(sys.argv[1]) as f:
    data = json.load(f)
if "geometry" in data:  # handle GeoJSON features
    data = data["geometry"]
polygons = antimeridian.close_polygon(shapely.geometry.shape(data))
print(json.dumps(shapely.geometry.mapping(polygons), indent=4))
