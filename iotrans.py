import os
import tempfile

import xmltodict

import pandas as pd
import geopandas as gpd

GEOSPATIAL_FORMATS = ['csv', 'geojson', 'gpkg', 'shp']
TABULAR_FORMATS = ['csv', 'json', 'xml']

FILE_PREFIX = 'iotrans_'

def prune():
    main = tempfile.gettempdir()
    for folder in os.listdir(main):
        if folder.startswith(FILE_PREFIX):
            shutil.rmtree(os.path.join(main, folder))

def to_file(data, fmt_out, filename='data', zip_content=True, remap_shp_fields=True):
    assert fmt_out in GEOSPATIAL_FORMATS or fmt_out in TABULAR_FORMATS, 'Invalid output formats'
    assert (fmt_out in TABULAR_FORMATS and isinstance(data, (pd.DataFrame, gpd.GeoDataFrame))) or \
            (fmt_out in GEOSPATIAL_FORMATS and isinstance(data, gpd.GeoDataFrame)), \
            'Invalid data structure'

    source = tempfile.mkdtemp(prefix=FILE_PREFIX)
    path = os.path.join(source, '{0}.{1}'.format(filename, fmt_out))

    if fmt_out == 'csv':
        data.to_csv(path, index=False, encoding='utf-8')
    elif fmt_out == 'json':
        data.to_json(path, orient='records')
    elif fmt_out == 'xml':
        content = xmltodict.unparse(data.to_dict('records'), pretty=True)
        with open(path, 'w') as f:
            f.write(content)
    elif fmt_out == 'geojson':
        data.to_file(path, driver='GeoJSON', encoding='utf-8')
    elif fmt_out == 'gpkg':
        data.to_file(path, driver='GPKG')
    elif fmt_out == 'shp':
        if remap_shp_fields and any([len(x) > 10 for x in df.columns]):
            fields = pd.DataFrame([['FIELD_{0}'.format(i+1) if x != 'geometry' else x, x] for i, x in enumerate(df.columns)], columns=['field', 'name'])
            fields.to_csv(os.path.join(source, 'fields.csv'), index=False, encoding='utf-8')

            df.columns = fields['field']

        df.to_file(path, driver='ESRI Shapefile')

    if zip_content:
        zipped = tempfile.mkdtemp()
        path = shutil.make_archive(os.path.join(zipped, filename), 'zip', root_dir=source, base_dir='.')

    return path
