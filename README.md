# antimeridian

[![CI Status](https://img.shields.io/github/actions/workflow/status/gadomski/antimeridian/ci.yaml?style=for-the-badge&label=CI)](https://github.com/gadomski/antimeridian/actions/workflows/ci.yaml)
[![Read the Docs](https://img.shields.io/readthedocs/antimeridian?style=for-the-badge)](https://antimeridian.readthedocs.io/en/latest/)
[![PyPI](https://img.shields.io/pypi/v/antimeridian?style=for-the-badge)](https://pypi.org/project/antimeridian/)

[![GitHub](https://img.shields.io/github/license/gadomski/antimeridian?style=for-the-badge)](https://github.com/gadomski/antimeridian/blob/main/LICENSE)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg?style=for-the-badge)](https://github.com/gadomski/antimeridian/blob/main/CODE_OF_CONDUCT)

Fix polygons that cross the antimeridian.
See [the documentation](https://antimeridian.readthedocs.io) for information about the underlying algorithm.
Depends on [shapely](https://shapely.readthedocs.io).

Can fix:

- Shapely [`Polygon`](https://shapely.readthedocs.io/en/stable/reference/shapely.Polygon.html#shapely.Polygon) and [`MultiPolygon`](https://shapely.readthedocs.io/en/stable/reference/shapely.MultiPolygon.html#shapely.MultiPolygon) objects
- GeoJSON [Polygons](https://datatracker.ietf.org/doc/html/rfc7946#section-3.1.6), [MultiPolygons](https://datatracker.ietf.org/doc/html/rfc7946#section-3.1.7), [Features](https://datatracker.ietf.org/doc/html/rfc7946#section-3.2) and [FeatureCollections](https://datatracker.ietf.org/doc/html/rfc7946#section-3.3), as dictionaries
- Anything that has a [`__geo_interface__`](https://gist.github.com/sgillies/2217756)

## Usage

```shell
pip install antimeridian
```

Then:

```python
import antimeridian
fixed = antimeridian.fix_geojson(geojson)
```

### Command line interface

Use the `cli` optional dependency to install the `antimeridian` CLI:

```shell
pip install 'antimeridian[cli]'
antimeridian fix input.json > output.json
```

## Developing

Clone and install in editable mode with the development optional dependencies:

```shell
git clone https://github.com/gadomski/antimeridian
cd antimeridian
pip install -e '.[dev,docs]'
```

We use [pytest](https://docs.pytest.org) for tests:

```shell
pytest
```

We use [Sphinx](https://www.sphinx-doc.org) for docs:

```shell
make -C docs html
```

## Contributing

Github [issues](https://github.com/gadomski/antimeridian/issues) and [pull requests](https://github.com/gadomski/antimeridian/pulls), please and thank you!

## License

[Apache-2.0](https://github.com/gadomski/antimeridian/blob/main/LICENSE)
