# modis_hdf_to_geotiff
Converts MODIS HDF dataset to GeoTiff using Python 3.

## Requirements
 - gdal with HDF4 support

## Usage
 ```
 modis_hdf_to_geotiff.py -h
 ```

 ```
usage: modis_hdf_to_geotiff.py [-h] -f  [-d] [-b  [...]]

Script to write MODIS remote sensing HDF file to GeoTiff

optional arguments:
  -h, --help            show this help message and exit
  -f , --filename       Path to .hdf file
  -d , --destination    Output file path. Default: current working directory
  -b  [ ...], --bands  [ ...]
                        Bands to write in 0th indexing (e.g. -b 0 1 2).
                        Default: all bands
 ```

## Example
### Extracting all bands
 ```
./modis_hdf_to_geotiff.py -f MOD16A2.A2018233.h10v04.006.2018249000053.hdf
 ```
### Extracting specific bands
 ```
./modis_hdf_to_geotiff.py -f MOD16A2.A2018233.h10v04.006.2018249000053.hdf -b 0 3

 ```
