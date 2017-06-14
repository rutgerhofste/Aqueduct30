# Rutger Hofste May 3rd 2017
# This script will add the parameter and an export description property to the images in the PCRGlob-WB imageCollecitons.
# In the future, this script will be unnecessary because the properties would ideally be added during the ingestion phase.


import subprocess
import os
import time




# users/rutgerhofste/PCRGlobWB20V04/demand/global_historical_PDomWN_month/global_historical_PDomWN_month_millionm3_5min_1960_2014I000Y1960M01



assetNameFolder = os.path.join("K:\PCRGlob2WBBigV02","runoff")
assetFolder = "users/rutgerhofste/PCRGlobWB20V04/runoff/"


imageCollectionNames = os.listdir(assetNameFolder)



for imageCollectionName in imageCollectionNames:
    imageFileNames = os.listdir(os.path.join(assetNameFolder,imageCollectionName))
    parameter = imageCollectionName[:-10]
    for imageFileName in imageFileNames:
        assetFileName = imageFileName[:-4]
        assetLocation = assetFolder + imageCollectionName + "/" + assetFileName
        year = imageFileName[-11:-7]
        month = imageFileName[-6:-4]
        exportDescription = parameter + "Y" + year +"M" +month
        units = "millionm3"
        identifier = imageFileName[-15:-12]


        command =  'earthengine asset set -p parameter=%s %s' % (parameter,assetLocation)
        command2 = 'earthengine asset set -p exportdescription=%s %s' % (exportDescription,assetLocation)
        command3 = 'earthengine asset set -p units=%s %s' % (units, assetLocation)
        command4 = 'earthengine asset set -p identifier=%s %s' % (identifier, assetLocation)




        subprocess.Popen(command)
        subprocess.Popen(command2)
        subprocess.Popen(command3)
        subprocess.Popen(command4)
        print command



print "done"