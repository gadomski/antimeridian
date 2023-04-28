Command line interface
======================

The **antimeridian** :abbr:`CLI (command line interface)` takes a GeoJSON file
path as its input, and outputs a fixed GeoJSON dictionary to standard output.

Installation
~~~~~~~~~~~~

Install with **pip**:

.. code-block:: shell

    pip install antimeridian[cli]

Usage
~~~~~

.. click:: antimeridian._cli:cli
   :prog: antimeridian
   :nested: full
