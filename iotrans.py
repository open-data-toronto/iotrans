from zipfile import ZipFile

import os

import pandas as pd
import geopandas as gpd
import xmltodict


_GEO_FMT = ['csv', 'geojson', 'gpkg', 'shp']
_TAB_FMT = ['csv', 'json', 'xml']

_MULTI_FILE = ['shp']


supported_formats = set(_GEO_FMT + _TAB_FMT)

def to_file(data, path, zip_content=True, remap_shp_fields=True):
    '''
    Converts pandas DataFrame or geopandas GeoDataFrame to another format

    Parameters:
    data             (DataFrame or GeoDataFrame): Data content to be converted
    path              (str)                     : Path to the output file
    zip_content      (bool)                     : If output file should be zipped
    remap_shp_fields (bool)                     : If Shapefile field names should be remapped to "FILED_#" structure

    Returns:
    (str): Path to the converted file
    '''

    filename, fmt = os.path.basename(path).split('.')
    path = os.path.dirname(path)

    assert fmt in supported_formats, 'Invalid output formats'
    assert (fmt in _TAB_FMT and isinstance(data, (pd.DataFrame, gpd.GeoDataFrame))) or \
            (fmt in _GEO_FMT and isinstance(data, gpd.GeoDataFrame)), \
            'Invalid data structure'

    # Create directory if the output format will generate multiple files (eg. Shapefile)
    if fmt in _MULTI_FILE:
        path = os.path.join(path, filename) # eg. '/path/output/'

        if os.path.isdir(path):
            _prune(path)

        os.mkdir(path)

    output = os.path.join(path, '{0}.{1}'.format(filename, fmt))

    if fmt == 'csv':
        data.to_csv(output, index=False, encoding='utf-8')
    elif fmt == 'json':
        data.to_json(output, orient='records')
    elif fmt == 'xml':
        content = xmltodict.unparse({
            'DATA': {
                'ROW_{0}'.format(idx): row for idx, row in enumerate(df.to_dict('records'))
            }
        }, pretty=True)

        with open(output, 'w') as f:
            f.write(content)
    elif fmt == 'geojson':
        data.to_file(output, driver='GeoJSON', encoding='utf-8')
    elif fmt == 'gpkg':
        data.to_file(output, driver='GPKG')
    elif fmt == 'shp':
        # Map the field names to 'FIELD_#' structure to avoid field names being truncated
        if remap_shp_fields and any([len(x) > 10 for x in df.columns]):
            fields = pd.DataFrame([['FIELD_{0}'.format(i+1) if x != 'geometry' else x, x] for i, x in enumerate(df.columns)], columns=['field', 'name'])

            # Save the converted field names as a CSV in the same directory
            fields.to_csv(os.path.join(path, '{0}_fields.csv'.format(filename)), index=False, encoding='utf-8')

            df.columns = fields['field']

        df.to_file(output, driver='ESRI Shapefile')

    if zip_content:
        # Go up a directory level to zip the entire contents of the directory
        if fmt in _MULTI_FILE:
            path = os.path.dirname(path)
            output = os.path.dirname(output)

        _zip_file(output, os.path.join(path, '{0}.zip'.format(filename)), clean=True)

    return output

def _prune(path):
    '''
    Deletes a file or a directory

    Parameters:
    path    (str): Path to be removed
    '''

    if os.path.isdir(path):
        # Empty the contents of the folder before removing the directory
        for f in os.listdir(path):
            os.remove(path)

        os.rmdir(path)
    else:
        os.remove(path)

def _zip_file(content, path, clean=False):
    '''
    Archives a file or the contents of a directory as a zip

    Parameters:
    content (str): Input path to the file or directory
    path    (str): Output path for the zip file
    '''

    with ZipFile(path, 'w') as f:
        if os.path.isdir(content):
            for item in os.listdir(content):
                f.write(os.path.join(content, item), arcname=item)
        else:
            f.write(content)

    if clean:
        _prune(content)
