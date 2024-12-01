# antimeridian

[![CI Status](https://img.shields.io/github/actions/workflow/status/gadomski/antimeridian/ci.yaml?style=for-the-badge&label=CI)](https://github.com/gadomski/antimeridian/actions/workflows/ci.yaml)
[![Read the Docs](https://img.shields.io/readthedocs/antimeridian?style=for-the-badge)](https://antimeridian.readthedocs.io/en/stable/)
[![PyPI](https://img.shields.io/pypi/v/antimeridian?style=for-the-badge)](https://pypi.org/project/antimeridian/)

[![GitHub](https://img.shields.io/github/license/gadomski/antimeridian?style=for-the-badge)](https://github.com/gadomski/antimeridian/blob/main/LICENSE)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg?style=for-the-badge)](https://github.com/gadomski/antimeridian/blob/main/CODE_OF_CONDUCT)

![Demonstration image](./docs/img/complex-split.png)

Fix shapes that cross the antimeridian.
See [the documentation](https://antimeridian.readthedocs.io) for information about the underlying algorithm.
Depends on [shapely](https://shapely.readthedocs.io) and [numpy](https://numpy.org/).

Can fix:

- Shapely [`Polygon`](https://shapely.readthedocs.io/en/stable/reference/shapely.Polygon.html#shapely.Polygon), [`MultiPolygon`](https://shapely.readthedocs.io/en/stable/reference/shapely.MultiPolygon.html#shapely.MultiPolygon), [`LineString`](https://shapely.readthedocs.io/en/stable/reference/shapely.LineString.html#shapely.LineString), and [`MultiLineString`](https://shapely.readthedocs.io/en/stable/reference/shapely.MultiLineString.html#shapely.MultiLineString) objects
- GeoJSON [Polygons](https://datatracker.ietf.org/doc/html/rfc7946#section-3.1.6), [MultiPolygons](https://datatracker.ietf.org/doc/html/rfc7946#section-3.1.7), [Features](https://datatracker.ietf.org/doc/html/rfc7946#section-3.2) and [FeatureCollections](https://datatracker.ietf.org/doc/html/rfc7946#section-3.3), as dictionaries
- Anything that has a [`__geo_interface__`](https://gist.github.com/sgillies/2217756)

## Usage

```shell
python -m pip install antimeridian
```

Then:

```python
import antimeridian

fixed = antimeridian.fix_geojson(geojson)
```

We also have some utilities to create [bounding boxes](https://antimeridian.readthedocs.io/en/latest/api.html#antimeridian.bbox) and [centroids](https://antimeridian.readthedocs.io/en/latest/api.html#antimeridian.centroid) from antimeridian-crossing polygons and multipolygons.
See [the documentation](https://antimeridian.readthedocs.io/) for a complete API reference.

### Command line interface

Use the `cli` optional dependency to install the `antimeridian` CLI:

```shell
python -m pip install 'antimeridian[cli]'
antimeridian fix input.json > output.json
```

## Developing

Get [uv](https://docs.astral.sh/uv/getting-started/installation/).
Then:

```shell
git clone https://github.com/gadomski/antimeridian
cd antimeridian
uv sync
```

We use [pytest](https://docs.pytest.org) for tests:

```shell
uv run pytest
```

To build and serve the docs locally:

```shell
uv run mkdocs serve
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[Apache-2.0](https://github.com/gadomski/antimeridian/blob/main/LICENSE)
