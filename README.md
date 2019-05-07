# iotrans

A package to easily convert structured data into various file formats

## Requirements
* Python 3.6
* geopandas>=0.4.0
* xmltodict>=0.12.0

## Installation
    git clone https://github.com/open-data-toronto/iotrans
    cd iotrans
    python setup.py install

## Usage
.. code:: python

    >>> import geopandas as gpd
    >>> import iotrans

### Geospatial data to XML

    >>> df = gpd.read_file([data_path])
    >>> iotrans.to_file(df, './data.xml')
        './data.xml'

### Output as a zip file

    >>> df = gpd.read_file([data_path])
    >>> iotrans.to_file(df, './data.shp')
        './data.zip'

## Supported Formats
### Tabular Formats
* CSV
* JSON
* XML

### Geospatial Formats
* CSV
* GeoJSON
* GeoPackage
* Shapefile
