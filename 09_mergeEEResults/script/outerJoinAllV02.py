


import os
import pandas as pd


inputPath = "/Users/rutgerhofste/Desktop/werkmap2/input/right_Table"
inputLocation = "/Users/rutgerhofste/Desktop/werkmap2/input/left_Table/hybas6c.csv"
outputLocation = "/Users/rutgerhofste/Desktop/werkmap2/output/hybas6Results11.csv"

dfl = pd.read_csv(inputLocation)
#dfl.set_index("hybas6ID")

files = os.listdir(inputPath)


for oneFile in files:
    if oneFile.endswith(".csv"):
        [fileName,extension] =oneFile.split(".")
        columnName = fileName[:-2]

        inputLocation = os.path.join(inputPath,oneFile)
        dfr = pd.read_csv(inputLocation)
        dfr = dfr.drop("system:index",1)
        dfr = dfr.drop(".geo",1)
        #dfr.set_index("hybas6ID")

        dfl = dfl.merge(dfr, how="outer",left_on="hybas6ID",right_on="hybas6ID"+"_"+columnName,suffixes=["",""])

dfl.to_csv(outputLocation)

print "done"

