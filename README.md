# antimeridian

A Python package to correct [shapely](https://shapely.readthedocs.io/en/stable/manual.html) polygons that cross the antimeridian.

## Usage

```shell
pip install git+https://github.com/gadomski/antimeridian
```

Then, in your code:

```python
import antimeridian
fixed = antimeridian.fix_polygon(polygon)
```

## Background

#### What's the antimeridian?

Also known as the [180th meridian](https://en.wikipedia.org/wiki/180th_meridian), the antimeridian is the line of longitude on the opposite side of the world from the prime meridian.
It can be either 180° east or west.

![The antimeridian, from Wikipedia](https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Earth_map_with_180th_meridian.jpg/320px-Earth_map_with_180th_meridian.jpg)

### What's the problem?

The GeoJSON specification [recommends cutting geometries at the antimeridian](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.9).
Many real-world geometries, however, don't follow this recommendation.
It's very common to, for example, create a geometry in a projected coordinate system, then reproject that geometry to WGS84 for its GeoJSON representation.
The reprojection process usually does not split the output geometry across the antimeridian, leading to invalid geometries.
Here's a simple example, taken from landsat:

```json
{
    "type": "Polygon",
    "coordinates": [
        [
            [
                -179.70358951407547,
                52.750507455036264
            ],
            [
                179.96672360880183,
                52.00163609753924
            ],
            [
                -177.89334479610974,
                50.62805205289558
            ],
            [
                -179.9847165338706,
                51.002602948712465
            ],
            [
                -179.70358951407547,
                52.750507455036264
            ]
        ]
    ]
}
```

As you can see, a tiny corner of the polygon crosses the antimeridian, leading to an invalid item:

![Landsat problem](./img/landsat-problem.png)

The issue also arises when geometries cross over the pole.

### How do we fix it?

We use a relatively simple algorithm that splits the input polygon into segments.
Each segment is defined by jumps of greater than 180° longitude -- it's not a perfect heuristic, but tends to work for most real-world geometries we've encountered.
Segments are then joined along the antimeridian.
Segments that enclose the poles are constructed by adding points at the top of the antimeridian at both the east and the west longitudes.

Here's before and after pictures of some Sentinel 5p data.
These are swath data that enclose both poles.
In the before picture, you can see the strange artifacts created by the invalid geometry:

![Sentinel 5p before](./img/sentinel-5p-before.png)

After correction, it's more clear that the data covers both poles:

![Sentinel 5p after](./img/sentinel-5p-after.png)
