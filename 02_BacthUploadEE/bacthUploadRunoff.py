# Created by Rutger Hofste on Feb 9 2017
# Goal is to batch upload geotiffs to Earth engine

import subprocess
import datetime
import os
import time
import re

# Deletes existing folders!!
INITIATLIZE = True


EEPATH = "users/rutgerhofste/PCRGlobWB20V04"
GROUPS = ["runoff"]

LOCAL_FILE_BASEPATH = os.path.join('K:/',r'PCRGlob2WBBigV02')
GS_FILE_BASEPATH = "gs://pcrglobwb20v02"

def createEEgroup(EEPATH,groupName):
    folderLocation = EEPATH + '/' + groupName
    # BE CAREFUL HERE!!!!! -----------------
    #command = ("earthengine rm -r %s") %folderLocation
    #subprocess.check_output(command)
    # --------------------------------------

    command = ("earthengine create folder %s") %folderLocation
    subprocess.check_output(command)
    return "success"

def createEECollection(EEPATH,groupName,collectionName):
    collectionLocation = EEPATH + '/' + groupName + '/' + collectionName
    # BE CAREFUL HERE!!!!! THIS WILL DELETE COLLECTION BEFORE CREATING -----------------
    command = ("earthengine rm -r %s") %collectionLocation
    subprocess.check_output(command)
    # --------------------------------------

    command = ("earthengine create collection %s") %collectionLocation
    subprocess.check_output(command)
    return  "success"

def upload2Collection(groupName,indicator,imageFile,GS_FILE_BASEPATH,EEPATH):
    source = GS_FILE_BASEPATH+"/"+groupName+"/"+imageFile
    target = EEPATH+"/"+groupName+"/"+indicator+"/"+imageFile[:len(imageFile)-4]
    year = imageFile[len(imageFile) - 11:len(imageFile) - 7]
    month = imageFile[len(imageFile) - 6:len(imageFile)-4]
    metadata = "--nodata_value=-9999 --time_start %s-%s-01 -p (number)year=%s -p (number)month=%s" %(year,month,year,month)
    command = "earthengine upload image --asset_id %s %s %s" %(target,source,metadata)
    subprocess.check_output(command)
    print command
    print "done"

# Create folder structure
if INITIATLIZE:
    for groupName in GROUPS:
        #Create group in EE
        createEEgroup(EEPATH,groupName)
        indicators = os.listdir(os.path.join(LOCAL_FILE_BASEPATH,groupName))
        for indicator in indicators:
            collectionName = indicator
            print groupName, indicator
            createEECollection(EEPATH, groupName, collectionName)
print "Collections created"

# Upload files to collections
errorlog = []
start_time = time.time()
i = 0
for groupName in GROUPS:
    indicators = os.listdir(os.path.join(LOCAL_FILE_BASEPATH,groupName))
    for indicator in indicators:
        collectionName = indicator
        imageFiles = os.listdir(os.path.join(LOCAL_FILE_BASEPATH, groupName,indicator))
        for imageFile in imageFiles:
            i += 1
            time.sleep(1)
            elapsed_time = (time.time() - start_time) / 60
            try:
                upload2Collection(groupName, indicator, imageFile, GS_FILE_BASEPATH, EEPATH)
            except:
                errorlog.append(imageFile)
            print "Item: " + str(i) + "  Time (min):" + str(elapsed_time)
"""

def createEEfolder(EEPATH,folderName):
    folderLocation = EEPATH + '/' + folderName
    # BE CAREFUL HERE!!!!! -----------------
    #command = ("earthengine rm -r %s") %folderLocation
    #subprocess.check_output(command)
    # --------------------------------------

    command = ("earthengine create folder %s") %folderLocation
    subprocess.check_output(command)
    return "success"

def createEECollection(EEPATH,folderName,collectionName):
    collectionLocation = EEPATH + '/' + folderName + '/' + collectionName
    # BE CAREFUL HERE!!!!! THIS WILL DELETE COLLECTION BEFORE CREATING -----------------
    command = ("earthengine rm -r %s") %collectionLocation
    subprocess.check_output(command)
    # --------------------------------------

    command = ("earthengine create collection %s") %collectionLocation
    subprocess.check_output(command)
    return  "success"

def uploadEEimage2collection(gsid,EEPath,folderName,collectionName,imageName):
    year = imageName[len(imageName)-7:len(imageName)-3]
    month = imageName[len(imageName)-2:len(imageName)]
    print year + " " + month
    imageLocation = EEPATH + '/' + folderName + '/' + collectionName + "/" + imageName
    command = "earthengine upload image --asset_id %s --nodata_value=-9999 %s --time_start %s-%s-01 " %(imageLocation,gsid,year,month)
    print command
    response = subprocess.check_output(command)
    return response


start_time = time.time()
# Set up folders
for EEFolderName in EEFOLDERS: #year month
    response = createEEfolder(EEPATH,EEFolderName)
    print "Folder %s Created" %EEFolderName

    for group in GROUP:
        collectionName = parameter
        response2 = createEECollection(EEPATH, EEFolderName, collectionName)
        print parameter
        files = os.listdir(os.path.join(LOCAL_FILE_BASEPATH,parameter))

        for i in range(0,len(files)):
            fileName = files[i]
            pattern = ".*" + str(EEFolderName)
            if re.match(pattern, fileName, flags=0):
                elapsed_time = (time.time() - start_time) / 60
                print "Item: " + str(i) + "  Time (min):" + str(elapsed_time)
                fileBaseName = fileName.split('.')[0]
                cloudLocation = GS_FILE_BASEPATH+ "/" + parameter +"/" + fileName
                EEImageName = fileBaseName
                response3 = uploadEEimage2collection(cloudLocation, EEPATH, EEFolderName, collectionName, EEImageName)

"""

print "Done"
print "Done"