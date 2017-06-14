


import os
import pandas as pd


inputPath = "/Users/rutgerhofste/Desktop/werkmap/input/rightTable"
inputLocation = "/Users/rutgerhofste/Desktop/werkmap/input/leftTable/leftTable.csv"
outputLocation = "/Users/rutgerhofste/Desktop/werkmap/output/hybas6Results08.csv"

dfl = pd.read_csv(inputLocation)
#dfl.set_index("hybas6ID")

files = os.listdir(inputPath)


for oneFile in files:
    if oneFile.endswith(".csv"):
        [fileName,extension] =oneFile.split(".")
        inputLocation = os.path.join(inputPath,oneFile)
        dfr = pd.read_csv(inputLocation)
        #dfr.set_index("hybas6ID")

        dfl = dfl.merge(dfr, how="outer",left_on="hybas6ID",right_on="hybas6ID",suffixes=["",fileName])

dfl.to_csv(outputLocation)

print "done"

