# Rutger Hofste 2017 03 16

# This script will merge HydroBasins on any given level



import arcpy
import os

metadata = "custom_level6"
inputPath = os.path.join('C:/',r'Users\Rutger.Hofste\Desktop\werkmap\input')
outputPath = os.path.join('C:/',r'Users\Rutger.Hofste\Desktop\werkmap\output')
outputFileName = "hybas_merged_%s_V01.shp" %(metadata)
outputLocation = os.path.join(outputPath, outputFileName)

files = os.listdir(inputPath)
fileList = []
for oneFile in files:
    if oneFile.endswith(".shp"):
        print oneFile
        fileList.append(os.path.join(inputPath,oneFile))



arcpy.Merge_management(fileList, outputLocation)

print("done")