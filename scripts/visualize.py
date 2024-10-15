"""Use this script to make a new image

E.g.:

    python scripts/visualize.py \
        tests/data/input/complex-split.json \
        docs/img/complex-split-uncorrected.png
"""

import json
import sys

import shapely.geometry
from cartopy.crs import PlateCarree
from matplotlib import pyplot

infile = sys.argv[1]
outfile = sys.argv[2]

with open(infile) as f:
    data = json.load(f)

shape = shapely.geometry.shape(data)

axes = pyplot.axes(projection=PlateCarree())
axes.stock_img()
axes.add_geometries(shape, crs=PlateCarree(), color="coral", alpha=0.7)

pyplot.savefig(outfile, bbox_inches="tight")
