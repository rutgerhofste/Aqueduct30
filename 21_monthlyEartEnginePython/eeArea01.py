import ee
ee.Initialize()

cellSize30s = ee.Image('users/rutgerhofste/PCRGlobWB20V04/support/cellsize30s'); #m^2 per pixel
hybas6Image = ee.Image('users/rutgerhofste/PCRGlobWB20V04/support/hybas_merged_custom_level6_30s_hybasID_V01').toInt64().select(["b1"],["hybas6"]);
onesImage30s = ee.Image('users/rutgerhofste/PCRGlobWB20V04/support/onesRaster30sV01')

geometry = ee.Geometry.Polygon(coords=[[-180.0, -90.0], [180,  -90.0], [180, 89], [180,90]], proj= ee.Projection('EPSG:4326'),geodesic=False )
#geometry = ee.Geometry.Polygon(coords=[[0, 0], [15,  0], [15, 15], [0, 15]], proj= ee.Projection('EPSG:4326'),geodesic=False )

parameter = "area_m2"


def list2fc(listItem): #use lambda function?
    return ee.Feature(None,listItem)

def addSuffix(fc,suffix):
    namesOld = ee.Feature(fc.first()).toDictionary().keys()
    namesNew = namesOld.map(lambda x:ee.String(x).cat(suffix))
    return fc.select(namesOld, namesNew)

def zonalStats(key,image):
    valueImage = ee.Image(image)
    weightsImage = onesImage30s
    zonesImage = hybas6Image
    scale = zonesImage.select(["hybas6"]).projection().nominalScale();
    totalImage = valueImage.addBands(weightsImage).addBands(zonesImage)
    resultsList = ee.List(totalImage.reduceRegion(
        geometry= geometry,
        reducer= weightedReducers.group(groupField= 2, groupName= "hybas6ID"),
        scale= scale,
        maxPixels= 1e10
        ).get("groups"))
    fc = ee.FeatureCollection(resultsList.map(list2fc))
    suffix = ee.String("_").cat(ee.String(key))
    fc2 = addSuffix(fc, suffix)
    return fc2


def export(fc,description):
    fc = ee.FeatureCollection(fc)
    myExportFC = ee.batch.Export.table.toDrive(collection=fc,
                                                description=description,
                                                folder="EEOutput",
                                                fileNamePrefix=description,
                                                fileFormat="CSV")
    myExportFC.start()


reducers = ee.Reducer.sum().combine(reducer2= ee.Reducer.count(), sharedInputs= True)
weightedReducers = reducers.splitWeights()

fc = zonalStats(parameter,cellSize30s)
export(fc,parameter)
print "done"