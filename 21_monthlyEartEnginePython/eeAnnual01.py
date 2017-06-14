import ee
ee.Initialize()

demandParameters = ["Dom","Ind","Irr","Liv"]
demandTypes = ["WW","WN"]
annualParameterListDemand = []

year = 2014
version = 04

for demandType in demandTypes:
    for demandParameter in demandParameters:
        annualParameterListDemand.append(demandParameter + demandType)

annualParameterListSupply = ["totalRunoff_annual"]

annualParameterList = annualParameterListDemand + annualParameterListSupply


#geometry = ee.Geometry.Polygon(coords=[[-180.0, -90.0], [180,  -90.0], [180, 89], [180,90]], proj= ee.Projection('EPSG:4326'),geodesic=False )
geometry = ee.Geometry.Polygon(coords=[[0, 0], [15,  0], [15, 15], [0, 15]], proj= ee.Projection('EPSG:4326'),geodesic=False )


hybas6Image = ee.Image('users/rutgerhofste/PCRGlobWB20V04/support/hybas_merged_custom_level6_30s_hybasID_V01').toInt64().select(["b1"],["hybas6"]);
cellSize5min = ee.Image('users/rutgerhofste/PCRGlobWB20V04/support/cellsize05min') #m^2 per pixel
cellSize30s = ee.Image('users/rutgerhofste/PCRGlobWB20V04/support/cellsize30s'); #m^2 per pixel

def importData(listItem):
    if listItem == "LivWW": # Livestock withdrawal (WW) = consumption (WN)
        listItem = "LivWN"
    imageCollection = ee.ImageCollection('users/rutgerhofste/PCRGlobWB20V04/demand/global_historical_P'+listItem+"_year")
    image = ee.Image(imageCollection.filter(ee.Filter.eq("year",year)).first())
    return image

def volumeToFlux(image):
  return ee.Image(image).divide(cellSize5min).multiply(1e6).copyProperties(image) #m/year or m/month

def list2fc(listItem): #use lambda function?
    return ee.Feature(None,listItem)

def addSuffix(fc,suffix):
    namesOld = ee.Feature(fc.first()).toDictionary().keys()
    namesNew = namesOld.map(lambda x:ee.String(x).cat(ee.String(suffix)))
    return fc.select(namesOld, namesNew)


def zonalStats(key,image):
    valueImage = ee.Image(image)
    weightsImage = cellSize30s
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
    suffix = ee.String(ee.Image(image).get("exportdescription"))
    fc2 = addSuffix(fc, suffix)
    return fc2

imageListDemand = ee.List(map(importData,annualParameterListDemand)) # client side
imageFluxListDemand = imageListDemand.map(volumeToFlux)  # server side m/year
imageDictDemand = ee.Dictionary.fromLists(annualParameterListDemand,imageFluxListDemand)

imageFluxListSupply = ee.List([ee.Image('users/rutgerhofste/meanNonAccumulatedPCRRunoff/mean1960tm2014totalRunoff_annuaTot_outputV21')])
imageDictSupply = ee.Dictionary.fromLists(annualParameterListSupply,imageFluxListSupply)

#imageList = imageListDemand
imageFluxList = imageFluxListDemand.cat(imageFluxListSupply)
imageDict = imageDictDemand.combine(imageDictSupply)

reducers = ee.Reducer.mean().combine(reducer2= ee.Reducer.count(), sharedInputs= True)
weightedReducers = reducers.splitWeights()

resultDict = ee.Dictionary(imageDict.map(zonalStats))

# export function runs client side

resultFCs = resultDict

print(resultFCs.getInfo())


def export(fc,description):
    fc = ee.FeatureCollection(fc)
    myExportFC = ee.batch.Export.table.toDrive(collection=fc,
                                                description=description,
                                                folder="EEOutput",
                                                fileNamePrefix=description,
                                                fileFormat="CSV")
    myExportFC.start()

for parameter in annualParameterList:
    print parameter
    resultFC = resultDict.get(parameter)
    description = parameter+"_annual_Y%0.2d_v%0.2d" %(year,version)
    export(resultFC,description)

print "Done"