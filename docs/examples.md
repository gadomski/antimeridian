---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
---

# Examples

Here's some examples of using the **antimeridian** package on some artificial and real-world data.

## Test cases

Our test suite exercises the antimeridian algorithm in a variety of ways.
Here, we visualize some our test cases in two projections.

```python
import warnings
import json

import shapely.geometry
from cartopy.crs import Mollweide, PlateCarree
from cartopy.io import DownloadWarning
from matplotlib import pyplot

import antimeridian

warnings.filterwarnings("ignore", category=DownloadWarning)


def plot(name: str) -> None:
    with open(f"../tests/data/input/{name}.json") as f:
        data = json.load(f)
    input = shapely.geometry.shape(data)
    output = shapely.geometry.shape(antimeridian.fix_geojson(data))

    figure = pyplot.figure()
    figure.suptitle(name)

    axes = figure.add_subplot(2, 2, 1, projection=PlateCarree())
    axes.set_title("Original in PlateCarree")
    axes.stock_img()
    axes.coastlines()
    axes.add_geometries(input, crs=PlateCarree(), color="coral", alpha=0.7)

    axes = figure.add_subplot(2, 2, 2, projection=PlateCarree())
    axes.set_title("Fixed in PlateCarree")
    axes.stock_img()
    axes.coastlines()
    axes.add_geometries(output, crs=PlateCarree(), color="coral", alpha=0.7)

    axes = figure.add_subplot(2, 2, 3, projection=Mollweide(central_longitude=180))
    axes.set_title("Original in Mollweide")
    axes.stock_img()
    axes.coastlines()
    axes.add_geometries(input, crs=PlateCarree(), color="coral", alpha=0.7)

    axes = figure.add_subplot(2, 2, 4, projection=Mollweide(central_longitude=180))
    axes.set_title("Fixed in Mollweide")
    axes.stock_img()
    axes.coastlines()
    axes.add_geometries(output, crs=PlateCarree(), color="coral", alpha=0.7)

    pyplot.show()

for name in ["split", "north-pole", "both-poles", "complex-split", "multi-split", "overlap"]:
    plot(name)
```
