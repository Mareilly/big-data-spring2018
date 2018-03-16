from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import os
%matplotlib inline

DATA = "/Users/mareilly/Desktop/MIT_Spring_2018/Big_Data/Problem Sets/PSet4/landsat"

def process_string (st):
    """
    Parses Landsat metadata
    """
    return float(st.split(' = ')[1].strip('\n'))

def ndvi_calc(red, nir):
    """
    Calculate NDVI
    """
    return (nir - red) / (nir + red)

def emissivity_calc (pv, ndvi):
    """
    Calculates an estimate of emissivity
    """
    ndvi_dest = ndvi.copy()
    ndvi_dest[np.where(ndvi < 0)] = 0.991
    ndvi_dest[np.where((0 <= ndvi) & (ndvi < 0.2)) ] = 0.966
    ndvi_dest[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ] = (0.973 * pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + (0.966 * (1 - pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + 0.005)
    ndvi_dest[np.where(ndvi >= 0.5)] = 0.973
    return ndvi_dest

def array2tif(raster_file, new_raster_file, array):
    """
    Writes 'array' to a new tif, 'new_raster_file',
    whose properties are given by a reference tif,
    here called 'raster_file.'
    """
    # Invoke the GDAL Geotiff driver
    raster = gdal.Open(raster_file)

    driver = gdal.GetDriverByName('GTiff')
    out_raster = driver.Create(new_raster_file,
                        raster.RasterXSize,
                        raster.RasterYSize,
                        1,
                        gdal.GDT_Float32)
    out_raster.SetProjection(raster.GetProjection())
    # Set transformation - same logic as above.
    out_raster.SetGeoTransform(raster.GetGeoTransform())
    # Set up a new band.
    out_band = out_raster.GetRasterBand(1)
    # Set NoData Value
    out_band.SetNoDataValue(-1)
    # Write our Numpy array to the new band!
    out_band.WriteArray(array)

#MY FUNCTIONS

b4_raster = os.path.join(DATA, 'picture.tif')
b5_raster = os.path.join(DATA, 'picture2.tif')

def tif2array(location):
    red_data = gdal.Open(location)
    red_band = red_data.GetRasterBand(1)
    color = red_band.ReadAsArray()
    y = color.astype(np.float32)
    return y

def retrieve_meta(meta_text): #4 pieces of meta data
    meta_file = '/Users/mareilly/Desktop/MIT_Spring_2018/Big_Data/Problem Sets/PSet4/landsat/metadata.txt'
    with open(meta_file) as f:
        meta = f.readlines()
    matchers = ['RADIANCE_MULT_BAND_10', 'RADIANCE_ADD_BAND_10', 'K1_CONSTANT_BAND_10', 'K2_CONSTANT_BAND_10']
    matching = [process_string(s) for s in meta if any(xs in s for xs in matchers)]
    rad_mult_b10, rad_add_b10, k1_b10, k2_b10 = matching
    return matching


def rad_calc(tirs, var_list):
    rad = var_list[0] * tirs + var_list[1]
    return rad

def bt_calc(rad, var_list):
    bt = var_list[3]/ np.log((var_list[2]/rad) + 1) - 273.15
    return bt

def pv_calc(ndvi, ndvi_s, ndvi_v):
    pv = (ndvi - 0.2) / (0.5 - 0.2) ** 2
    return pv

def lst_calc(location):
#Calculate Estimate of Land Surface Temperature.
    tifname='LC08_L1TP_012030_20160713_20180130_01_T1_'

    red_path = os.path.join(DATA, (tifname+'b4.tif'))
    nir_path = os.path.join(DATA, (tifname+'b5.tif'))
    tirs_path = os.path.join(DATA, (tifname+'b10.TIF'))

    red=tif2array(red_path)
    nir=tif2array(nir_path)
    tirs=tif2array(tirs_path)

    ## Calculate Land Surface Temperature
    meta_file = '/Users/mareilly/Desktop/MIT_Spring_2018/Big_Data/Problem Sets/PSet4/landsat/metadata.txt'
    meta_list = retrieve_meta(meta_file)

    # Step 1: Calculate Top of Atmosphere Spectral Radiance
    rad = rad_calc(tirs, meta_list)

    #Step 2: Calculate Brightness Temperature
    bt = bt_calc(rad, meta_list)

    # Step 3: Calculate Normalized Difference Vegetation Index
    ndvi = ndvi_calc(red, nir)

    # Step 4: Calculate Proportional Vegetation
    pv = pv_calc(ndvi, 0.2, 0.5)

    # Step 5: Calculate Land Surface Emissivity
    emis = emissivity_calc(pv, ndvi)

    #Step 6:Calculate Land Surface Temperature
    wave = 10.8E-06
    # PLANCK'S CONSTANT
    h = 6.626e-34
    # SPEED OF LIGHT
    c = 2.998e8
    # BOLTZMANN's CONSTANT
    s = 1.38e-23
    p = h * c / s
    lst = bt / (1 + (wave * bt / p) * np.log(emis))
    return lst

#Cloud Filter

def cloud_filter(array, bqa): #Filters out clouds and cloud shadows using values of BQA.
    bqa_path = os.path.join(DATA, (tifname+'BQA.TIF'))
    bqa = tif2array(bqa_path)
    array_dest = array.copy()
    array_dest[np.where((bqa != 2720) & (bqa != 2724)& (bqa != 2728)& (bqa != 2732)) ] = 'nan'
    return array_dest
## Write Filtered Arrays as `.tifs`

cloudless_ndvi = cloud_filter(ndvi, bqa)
cloudless_lst = cloud_filter(lst, bqa)
plt.imshow(cloudless_lst)
plt.colorbar()

#TIFTIME

tirs_path = os.path.join(DATA, 'LC08_L1TP_012030_20160713_20180130_01_T1_B10.TIF')

out_path_ndvi = os.path.join(DATA, 'Reilly_ndvi_20180130.tif')
array2tif(tirs_path, out_path_ndvi, cloudless_ndvi)

out_path_lst = os.path.join(DATA, 'Reilly_lst_20180130.tif')
array2tif(tirs_path, out_path_lst, cloudless_lst)
