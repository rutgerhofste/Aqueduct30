import subprocess
import datetime
import os
import time
import re

EEPATH = "users/rutgerhofste/PCRGlobWB20V04"
GROUPS = ["support"]

LOCAL_FILE_BASEPATH = os.path.join('K:/',r'PCRGlob2WBBigV02')
GS_FILE_BASEPATH = "gs://pcrglobwb20v02"

"""
# create folders
command = "earthengine create folder users/rutgerhofste/PCRGlobWB20V04/indicators"
subprocess.check_output(command)
command = "earthengine create folder users/rutgerhofste/PCRGlobWB20V04/support"
subprocess.check_output(command)
time.sleep(10) #wait for folders to be created
"""

print "folders created"

def upload2Collection(groupName, imageFile, GS_FILE_BASEPATH, EEPATH):
    source = GS_FILE_BASEPATH + "/" + groupName + "/" + imageFile
    target = EEPATH + "/" + groupName + "/" + imageFile[:len(imageFile) - 4]
    metadata = "--nodata_value=-9999"
    command = "earthengine upload image --asset_id %s %s %s" % (target, source, metadata)
    #subprocess.check_output(command)
    print command

for groupName in GROUPS:
    imageFiles = os.listdir(os.path.join(LOCAL_FILE_BASEPATH,groupName))
    for imageFile in imageFiles:
        upload2Collection(groupName, imageFile, GS_FILE_BASEPATH, EEPATH)