import ee
ee.Initialize()

year = 2014

demandParameters = ["Dom","Ind","Irr","Liv"]
demandTypes = ["WW","WN"]
monthlyParameterListDemand = []

#geometry = ee.Geometry.Polygon(coords=[[-180.0, -90.0], [180,  -90.0], [180, 89], [180,90]], proj= ee.Projection('EPSG:4326'),geodesic=False )
geometry = ee.Geometry.Polygon(coords=[[0, 0], [15,  0], [15, 15], [0, 15]], proj= ee.Projection('EPSG:4326'),geodesic=False )

for demandType in demandTypes:
    for demandParameter in demandParameters:
        monthlyParameterListDemand.append(demandParameter + demandType)

monthlyParameterListSupply = ["totalRunoff_monthly"]
monthlyParameterList = monthlyParameterListDemand + monthlyParameterListSupply

hybas6Image = ee.Image('users/rutgerhofste/PCRGlobWB20V04/support/hybas_merged_custom_level6_30s_hybasID_V01').toInt64().select(["b1"],["hybas6"]);
cellSize5min = ee.Image('users/rutgerhofste/PCRGlobWB20V04/support/cellsize05min') #m^2 per pixel
cellSize30s = ee.Image('users/rutgerhofste/PCRGlobWB20V04/support/cellsize30s');

def importDemandData(listItem):
    if listItem == "LivWW": # Livestock withdrawal (WW) = consumption (WN)
        listItem = "LivWN"
    imageCollection = ee.ImageCollection('users/rutgerhofste/PCRGlobWB20V04/demand/global_historical_P'+listItem+"_month")
    imageCollection = imageCollection.filter(ee.Filter.eq("year",year))
    return imageCollection

def volumeToFlux(imageCollection):
    imageCollection = ee.ImageCollection(imageCollection).map(lambda image:ee.Image(image).divide(cellSize5min).multiply(1e6).copyProperties(image))
    return imageCollection

def list2fc(listItem): #use lambda function?
    return ee.Feature(None,listItem)

def addSuffix(fc,suffix):
    namesOld = ee.Feature(fc.first()).toDictionary().keys()
    namesNew = namesOld.map(lambda x:ee.String(x).cat(suffix))
    return fc.select(namesOld, namesNew)










icListDemand = ee.List(map(importDemandData,monthlyParameterListDemand)) # Units are million m^3/year
icFluxListDemand = icListDemand.map(volumeToFlux)
icDictDemand = ee.Dictionary.fromLists(monthlyParameterListDemand,icFluxListDemand)

icFluxListSupply = ee.List([ee.ImageCollection('users/rutgerhofste/meanNonAccumulatedPCRRunoff/mean1960tm2014totalRunoff_monthlyTot_output')])
icDictSupply = ee.Dictionary.fromLists(monthlyParameterListSupply,icFluxListSupply)

icFluxList = icFluxListDemand.cat(icFluxListSupply)
icDict = ee.Dictionary(icDictDemand.combine(icDictSupply))

reducers = ee.Reducer.mean().combine(reducer2= ee.Reducer.count(), sharedInputs= True)
weightedReducers = reducers.splitWeights()












print "done"