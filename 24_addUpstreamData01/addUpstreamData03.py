import os
import pandas as pd
import ast
import time

# Rutger Hofste May 10 2017
# this script is written for Compute Engine. Copy folder to CE, install dependencies and run code



start_time = time.time()
errorlog =[]

inputLocation = "input/pfaf_merged_standard_level6_V01_upstreamV14_resultsV01.csv"
inputParameterPath = "input/parameters"
outputLocation = "output/pfaf_merged_standard_level6_V01_upstreamV14_resultsV01_summedV01.csv"

df_temp = pd.read_csv(inputLocation)
df = df_temp.set_index("PFAF_ID")
df_out = df.copy()

types = df.dtypes

files = os.listdir(inputParameterPath)
parameterList =[]
for oneFile in files:
    if oneFile.endswith(".csv"):
        [fileName,extension] =oneFile.split(".")
        parameterList.append(fileName[:-3])

i = 0
for index, row in df.iterrows():
    i += 1
    time_elapsed = time.time() - start_time
    print "i:", i, " PFAF_ID: ", index , "time elapsed: ", time_elapsed

    try:
        upstreamCatchments = df.loc[index, "Upstream_PFAF_IDs"]
        upstreamCatchments = ast.literal_eval(upstreamCatchments)
        df_upstream = df.loc[upstreamCatchments]
        area = df_upstream["countarea30sm2"]*df_upstream["meanarea30sm2"]

        df_new = pd.DataFrame()
        df_new["aream2"] = area

        for parameter in parameterList:
            df_new["count"+parameter] = df_upstream["count"+parameter]
            df_new["volumem3"+parameter] = area* df_upstream["mean" + parameter]

        sumSeries = df_new.sum()

        for key, value in sumSeries.iteritems():
            newKey = "upstream_sum_" + key
            df_out.loc[index, newKey] = value
    except:
        print "ERROR"
        errorlog.append(index)

df_out.to_csv(outputLocation)

print "errorlog" , errorlog
print "Done"