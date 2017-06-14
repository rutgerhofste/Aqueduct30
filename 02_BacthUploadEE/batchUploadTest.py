import os

LOCAL_FILE_BASEPATH = os.path.join('K:/',r'PCRGlob2WBBigV02')

PARAMETERS = ["test","demand","soilMoisture","waterAvailability","waterStress"]

parameter = 'demand'
files = os.listdir(os.path.join(LOCAL_FILE_BASEPATH,parameter))
print "test"