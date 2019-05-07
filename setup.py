try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='iotrans',
    version='0.0.1',
    author='Open Data Toronto',
    author_email='opendata@toronto.ca',
    packages=[],
    url='https://github.com/open-data-toronto/iotrans',
    license='MIT',
    description='Centralize various format writing tools for structured data',
    install_requires=[
        'geopandas>=0.4.0',
        'xmltodict>=0.12.0'
    ],
    include_package_data=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
    keywords='',
)
