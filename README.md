# iotrans

Centralize various format writing tools for structured data

## Requirements
* Python 3.6
* geopandas>=0.4.0
* xmltodict>=0.12.0

## Installation
    git clone https://github.com/open-data-toronto/iotrans
    cd iotrans
    python setup.py install
    
## Usage

```python
import geopandas as gpd
import iotrans
```

### Geospatial data to XML

```python
df = gpd.read_file([data_path])
iotrans.to_file(df, './data.xml')
```
```
   './data.xml'
```
        
### Output as a zip file

```python
df = gpd.read_file([data_path])
iotrans.to_file(df, './data.shp')
```
```
'./data.zip'
```

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
