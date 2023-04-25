# Tests

All of the test files were hand-crafted, with these exceptions:

- [overlap](./data/input/overlap.json): this is a real-world example, created from a producer-provided geometry in a [Sentinel 3](https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-3) [STAC](https://stacspec.org) item (`S3A_SL_2_WST_20171106T152925_20171106T171024_6059_024_139_4545`).

## Adding new polygon tests

1. Add a JSON file to `data/input`.
   This file should be a GeoJSON Polygon.
2. Add its expected output to `data/output` with the same file name.
3. Add its file name, with no suffix, to the parameterization of the `test_fix_polygon` function in `test_polygon.py`.
