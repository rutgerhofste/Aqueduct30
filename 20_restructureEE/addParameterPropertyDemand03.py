# Rutger Hofste May 3rd 2017
# This script will add the parameter and an export description property to the images in the PCRGlob-WB imageCollecitons.
# In the future, this script will be unnecessary because the properties would ideally be added during the ingestion phase.


import subprocess
import os
import time

# the first time I ran the script on a local machine. It is more convenient though to run as a bash scrip in Gloud shell
# launch a google cloud shell
# set up earthengine
# Authenticate
# Use nano to create a bash script (small)
# or upload to Google cloud storage and use gsutil to copy to cloud shell
# run the bash script


# users/rutgerhofste/PCRGlobWB20V04/demand/global_historical_PDomWN_month/global_historical_PDomWN_month_millionm3_5min_1960_2014I000Y1960M01

target = open("bashfile.sh", 'w')


assetNameFolder = "K:\PCRGlob2WBBigV02\demand"
assetFolder = "users/rutgerhofste/PCRGlobWB20V04/demand/"

imageCollectionNames = os.listdir(assetNameFolder)



for imageCollectionName in imageCollectionNames:
    imageFileNames = os.listdir(os.path.join(assetNameFolder,imageCollectionName))
    parameter = imageCollectionName[19:]
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

        target.write(command)
        target.write("\n")
        target.write(command2)
        target.write("\n")
        target.write(command3)
        target.write("\n")
        target.write(command4)
        target.write("\n")


        #subprocess.Popen(command)
        #subprocess.Popen(command2)
        #subprocess.Popen(command3)
        #subprocess.Popen(command4)
        print command
        print command2
        print command3
        print command4


target.close()

print "done"