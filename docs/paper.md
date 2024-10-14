---
title: "antimeridian: A Python package for fixing geometries that cross the 180th meridian"
tags:
  - Python
  - geospatial
  - antimeridian
authors:
  - name: Peter Gadomski
    orcid: 0000-0003-4877-7217
    corresponding: true
    affiliation: 1
  - name: Preston Hartzell
    orcid: 0000-0002-8293-3706
    affiliation: 2
affiliations:
  - name: Development Seed, USA
    index: 1
  - name: Element 84, Inc., USA
    index: 2
date: 10 October 2024
bibliography: paper.bib
---

## Summary

Locations on and around planet Earth are commonly represented in a geodetic coordinate system with a longitude, a latitude, and a height. 
Longitude, the "horizontal" dimension, covers the domain from -180° to 180° or 0° and 360°.
Where the two domain bounds meet is known as the _180th meridian_ or the _antimeridian_.

![Earth map centered on the Pacific ocean, with the 180th meridian highlighted.](./img/antimeridian.jpg)

The GeoJSON specification [@10.17487/RFC7946] describes how antimeridian-crossing shapes should be represented.
For a variety of reasons, real-world geometries often do not comply with the specification, leading to confusing and unrepresentable geometries.
Our **antimeridan** package provides Python functions for correcting improper geometries, as well as other related utilities.

## Statement of need

Due to a variety of factors, including the relative lack of populated settlements on the other side of the world, the Prime Meridian (0°) runs through Greenwich, England [@alma992356353405961].
Before the advent of satellite imagery, relatively few geospatial products crossed the 180th meridian, and so the problem of antimeridian-crossing geometries was usually avoidable.
The proliferation of satellite remote sensing products, including Earth Observation (EO) imagery, coupled with the ubiquity of interactive online maps, the antimeridian has become a feature that can appear on almost anyone's tablet, web portal, or desktop Geographic Information System (GIS) software.
There is a a need to create and fix antimeridian-crossing geometries at scale, e.g. for large SpatioTemporal Asset Catalog (STAC) [@STAC_Contributors_SpatioTemporal_Asset_Catalog_2024] catalogs that are used to search and discover petabytes of geospatial data.
When creating these catalogs, improper antimeridian-crossing geometries need to be corrected before ingesting to a data store to ensure that queries do not break and visualizations do not go haywire.
This is the problem for which **antimeridian** was designed.

To the best of our knowledge, the [algorithm](https://antimeridian.readthedocs.io/en/stable/the-algorithm.html) underlying **antimeridian** is a novel one.
Briefly, it breaks each polygon into segments and finds where a segment might cross the antimeridian.
It then breaks that segment at that crossing point and closes that segment along the antimeridian to create a new polygon.
This results in a multi polygon split on the antimeridian, as the GeoJSON specification requires.

![A complex shape split at the antimeridian](./img/complex-split.png)

The library also includes utilities for calculating centriods from antimeridian-crossing geometries and generating valid GeoJSON antimeridian-crossing bounding boxes.
It has been ported to Go by another developer at [go-geospatial/antimeridian](https://pkg.go.dev/github.com/go-geospatial/antimeridian).

## Key references

- The **antimeridian** package relies on Shapely [@Gillies_Shapely_2024] for geometry validation, conversions, and other operations.
- We use Cartopy [@Cartopy] to generate visualizations for our documentation.

# Acknowledgements

We acknowledge Rob Emanuele, Tom Augspurger, and Matt McFarland for the technical and financial support they provided us through the Planetary Computer program at Microsoft.
We would also like to acknowledge our employers, Development Seed and Element 84, who support open source software through direct funding and developer contribution time.
