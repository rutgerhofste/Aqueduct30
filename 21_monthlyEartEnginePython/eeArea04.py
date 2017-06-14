import ee
import itertools
import time
import re
from retrying import retry

# This version uses regular expressions to filter dates based on fileNames


ee.Initialize()
start_time = time.time()

version = "V05"
hybasLevel = 6
#pattern = ".*Y2014M.*"


def getExportDescription(listItem):
    assetId = listItem["id"]
    exportDescription = ee.String(ee.Image(assetId).get("exportdescription"))
    return exportDescription

def volumeToFlux(image):
    image = ee.Image(image)
    image = image.divide(cellSize5min).multiply(1e6).copyProperties(image)
    image = image.set("units","m")
    image = image.set("convertedToFlux", "yes")
    return image

def addSuffix(fc,suffix):
    namesOld = ee.Feature(fc.first()).toDictionary().keys()
    namesNew = namesOld.map(lambda x:ee.String(x).cat(ee.String(suffix)))
    return fc.select(namesOld, namesNew)

def zonalStats(image,suffix,hybasLevel):
    image = ee.Image(image)
    valueImage = image
    weightsImage = onesRaster30s
    zonesImage = newHydroBASINimage
    scale = cellSize30s.projection().nominalScale();
    totalImage = valueImage.addBands(weightsImage).addBands(zonesImage)
    resultsList = ee.List(totalImage.reduceRegion(
        geometry= geometry,
        reducer= weightedReducers.group(groupField= 2, groupName= "PfafID"),
        scale= scale,
        maxPixels= 1e10
        ).get("groups"))
    fc = ee.FeatureCollection(resultsList.map(lambda listItem: ee.Feature(None,listItem)))
    fc2 = addSuffix(fc, suffix)
    fc2 = fc2.copyProperties(image)
    return fc2

@retry(wait_exponential_multiplier=10000, wait_exponential_max=100000)
def export(fc,description,version):
    fc = ee.FeatureCollection(fc)
    myExportFC = ee.batch.Export.table.toDrive(collection=fc,
                                                description=description+version,
                                                folder="EEOutput"+version,
                                                fileNamePrefix=description+version,
                                                fileFormat="CSV")
    myExportFC.start()


# Import aux data
geometry = ee.Geometry.Polygon(coords=[[-180.0, -90.0], [180,  -90.0], [180, 90], [-180,90]], proj= ee.Projection('EPSG:4326'),geodesic=False )
#geometry = ee.Geometry.Polygon(coords=[[0, 0], [15,  0], [15, 15], [0, 15]], proj= ee.Projection('EPSG:4326'),geodesic=False )

HydroBASINSimage = ee.Image("users/rutgerhofste/PCRGlobWB20V04/support/global_Standard_lev00_30sGDALv01")
newHydroBASINimage = ee.Image(HydroBASINSimage.divide(ee.Number(10).pow(ee.Number(12).subtract(hybasLevel))).floor())
newHydroBASINimage = newHydroBASINimage.toInt64().select(["b1"],["PfafID"])
cellSize5min = ee.Image('users/rutgerhofste/PCRGlobWB20V04/support/cellsize05min') #m^2 per pixel
cellSize30s = ee.Image('users/rutgerhofste/PCRGlobWB20V04/support/cellsize30s')
onesRaster30s = ee.Image('users/rutgerhofste/PCRGlobWB20V04/support/onesRaster30sV01')

reducers = ee.Reducer.mean().combine(reducer2= ee.Reducer.count(), sharedInputs= True)
weightedReducers = reducers.splitWeights()


# Start client side script
clientDict = {"area30sm2":{"id":"users/rutgerhofste/PCRGlobWB20V04/support/cellsize30s"}}


# iterate over client side dictionary, perform zonal stats and export
i = 0
for key, value in clientDict.iteritems():
    i += 1
    print("number of images processed:",i)
    print("%f seconds" % (time.time() - start_time))

    image = ee.Image(value["id"])

    fc = zonalStats(image,key,hybasLevel)
    export(fc, key, version)


print "Done"