import os
import pandas as pd


inputPath = "C:\Users\Rutger.Hofste\Desktop\werkmap\input\lightTable"
inputLocation = "C:\Users\Rutger.Hofste\Desktop\werkmap\input\leftTable\hybas_merged_standard_level6_V01_upstreamV14.csv"
outputLocation = "C:\Users\Rutger.Hofste\Desktop\werkmap\output\pfaf_merged_standard_level6_V01_upstreamV14_resultsV01.csv"

dfl = pd.read_csv(inputLocation)
#dfl.set_index("hybas6ID")

files = os.listdir(inputPath)


for oneFile in files:
    if oneFile.endswith(".csv"):
        [fileName,extension] =oneFile.split(".")
        print fileName
        inputLocation = os.path.join(inputPath,oneFile)
        dfr = pd.read_csv(inputLocation)
        dfr = dfr.drop("system:index",1)
        dfr = dfr.drop(".geo",1)
        #dfr.set_index("hybas6ID")
        rightColName = "PfafID" + fileName[:-3]
        dfl = dfl.merge(dfr, how="outer",left_on="PFAF_ID",right_on=rightColName,suffixes=["",""])


dfl.to_csv(outputLocation)

print "done"