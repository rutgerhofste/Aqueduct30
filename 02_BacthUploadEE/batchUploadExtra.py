import subprocess
import datetime
import os
import time
import re

EEPATH = "users/rutgerhofste/PCRGlobWB20V04"
GROUPS = ["support","indicators"]

LOCAL_FILE_BASEPATH = os.path.join('K:/',r'PCRGlob2WBBigV02')
GS_FILE_BASEPATH = "gs://pcrglobwb20v02"

for groupName in GROUPS:
    print groupName
    indicators = os.listdir(os.path.join(LOCAL_FILE_BASEPATH,groupName))
    print indicators