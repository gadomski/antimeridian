#!/usr/bin/env sh
#
# Compare ogr2ogr -wrapdateline with our package.

set -e

root="$(cd "$(dirname -- "$1")" >/dev/null; pwd -P)/$(basename -- "$1")"
destination="$root/tests/data/ogr2ogr"
mkdir -p $destination

for path in $root/tests/data/input/*.json; do
    file_name="${path##*/}"
    ogr2ogr -of GeoJSON -wrapdateline "$destination/$file_name" $path
done
