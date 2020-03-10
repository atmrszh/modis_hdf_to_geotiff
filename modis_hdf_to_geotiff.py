#!/usr/bin/env python3

from osgeo import gdal
import numpy as np
import os
import argparse


def hdf_subdataset_extraction(hdf_file, dst_dir, subdataset):

    """ Writes MODIS remote sensing HDF file to GeoTiff """

    # open the dataset
    hdf_ds = gdal.Open(hdf_file, gdal.GA_ReadOnly)
    band_ds = gdal.Open(hdf_ds.GetSubDatasets()[subdataset][0], gdal.GA_ReadOnly)

    # read into numpy array
    band_array = band_ds.ReadAsArray().astype(np.int16)

    # convert no_data values
    band_array[band_array == -28672] = -32768

    # build output path
    band_path = os.path.join(dst_dir, os.path.basename(os.path.splitext(hdf_file)[0]) + "-sd" + str(subdataset+1) + ".tif")

    # write raster
    out_ds = gdal.GetDriverByName('GTiff').Create(band_path,
                                                  band_ds.RasterXSize,
                                                  band_ds.RasterYSize,
                                                  1,  #Number of bands
                                                  gdal.GDT_Int16,
                                                  ['COMPRESS=LZW', 'TILED=YES'])
    out_ds.SetGeoTransform(band_ds.GetGeoTransform())
    out_ds.SetProjection(band_ds.GetProjection())
    out_ds.GetRasterBand(1).WriteArray(band_array)
    out_ds.GetRasterBand(1).SetNoDataValue(-32768)
    print("Successfully wrote:" + band_path)

    out_ds = None  #close dataset to write to disc


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
            'Script to write MODIS remote sensing HDF file to GeoTiff')
    parser.add_argument('-f','--filename',type=str,metavar='',required=True,help='Path to .hdf file')
    parser.add_argument('-d','--destination',type=str,metavar='',help='Output file path. Default: current working directory')
    parser.add_argument('-b','--bands', nargs='+',type=int,metavar='',required=False,help='Bands to write in 0th indexing (e.g. -b 0 1 2). Default: all bands')
    args = parser.parse_args()

    if not args.destination:
        # use current working directory if destination not set
        args.destination = os.getcwd()
    if not args.bands:
        # write all bands if bands is not set
        src_ds = gdal.Open(args.filename, gdal.GA_ReadOnly)
        args.bands = list(range(len(src_ds.GetSubDatasets())))

    for band in args.bands:
        hdf_subdataset_extraction(args.filename,args.destination,band)

