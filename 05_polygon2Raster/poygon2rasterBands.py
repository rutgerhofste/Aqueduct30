# Run During a night!

import arcpy
import os
import re
import time
import subprocess
from arcpy.sa import *

start_time = time.time()
# gdal_rasterize -a PFAF_12_IN -ot Integer64 -of GTiff -te -180 -90 180 90 -ts 43200 21600 -co COMPRESS=LZW -co PREDICTOR=1 -co ZLEVEL=6 -l global_Standard_lev00_v1c -a_nodata -9999 C:\Users\Rutger.Hofste\Desktop\werkmap\input\global_Standard_lev00_v1c.shp C:\Users\Rutger.Hofste\Desktop\werkmap\output\global_Standard_lev00_30sGDALv01.tif
arcpy.CheckOutExtension("spatial")

onesRaster30sV01Location = "C:\Users\Rutger.Hofste\Desktop\werkmap\sampleInput\onesRaster30sV01.tif"
shapeLocation = "C:\Users\Rutger.Hofste\Desktop\werkmap\input\global_Standard_lev00_v1c.shp"
outputPath = "C:\Users\Rutger.Hofste\Desktop\werkmap\output"

def getFieldNames(shp):
    fieldnames = [f.name for f in arcpy.ListFields(shp)]
    return fieldnames

fields = getFieldNames(shapeLocation)

fields = [u'HYBAS_ID', u'NEXT_DOWN', u'NEXT_SINK', u'MAIN_BAS', u'DIST_SINK', u'DIST_MAIN', u'SUB_AREA', u'UP_AREA', u'ENDO', u'COAST', u'ORDER_', u'SORT', u'PFAF_1', u'PFAF_2', u'PFAF_3', u'PFAF_4', u'PFAF_5', u'PFAF_6', u'PFAF_7', u'PFAF_8', u'PFAF_9', u'PFAF_10', u'PFAF_11', u'PFAF_12', u'PFAF_12_IN']
rasterType = {'HYBAS_ID':"Integer64", 'NEXT_DOWN': "Integer64", 'NEXT_SINK':"Integer64", 'MAIN_BAS':"Integer64", 'DIST_SINK':"Float64", 'DIST_MAIN':"Float64", 'SUB_AREA':"Float64", 'UP_AREA':"Float64", 'ENDO':"Integer64", 'COAST':"Integer64", 'ORDER_':"Integer64", 'SORT':"Integer64", 'PFAF_1':"Integer64", 'PFAF_2':"Integer64", 'PFAF_3':"Integer64", 'PFAF_4':"Integer64", 'PFAF_5':"Integer64", 'PFAF_6':"Integer64", 'PFAF_7':"Integer64", 'PFAF_8':"Integer64", 'PFAF_9':"Integer64", 'PFAF_10':"Integer64", 'PFAF_11':"Integer64", 'PFAF_12':"Integer64", 'PFAF_12_IN':"Integer64"}
resolutions = ["30s","15s"]

for resolution in resolutions:
    if resolution == "30s":
        print "30s"
        xsize = 43200
        ysize = 21600
    elif resolution == "15s":
        print "15s"
        xsize = 43200*2
        ysize = 21600*2

    for field in fields:
        print field
        outputFileName = "%sres%sGDALv01.tif" %(field,resolution)
        # Set local variables
        inFeature = shapeLocation
        outRaster = os.path.join(outputPath,outputFileName)

        command = "gdal_rasterize"
        command += " -a %s" %(field)
        command += " -ot %s -of GTiff -te -180 -90 180 90 -ts %0.2d %0.2d" %(rasterType[field],xsize,ysize) #global 30s 43200 21600
        command += " -co COMPRESS=LZW -co PREDICTOR=1 -co ZLEVEL=6"
        command += " -l global_Standard_lev00_v1c" # layer name global_Standard_lev00_v1c
        command += " -a_nodata -9999"
        command += " %s" %(inFeature)
        command += " %s" %(outRaster)
        print(command)
        try:
            subprocess.check_output(command)
        except:
            print("FAILED!!:" , command)
        elapsed_time = time.time() - start_time
        print("time elapsed: ", elapsed_time)




print "Done"