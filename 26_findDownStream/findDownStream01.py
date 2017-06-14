"""
CATCHMENT LEVEL FLOW ACCUMULATION
September 19, 2015 ; March 17 2017
Author: Tianyi Luo ; Rutger Hofste
"""

import pandas as pd
import numpy as np
import os, ftplib, urllib2, ast
from datetime import datetime, timedelta

# Settings
# Before you run the script, make sure the columns are in the right dtype (int64)

errorlog = []
inputLocation = "C:\Users\Rutger.Hofste\Desktop\werkmap\input\hybas_merged_standard_level6_V01_upstreamV17.csv"
outputLocation = "C:\Users\Rutger.Hofste\Desktop\werkmap\output\hybas_merged_standard_level6_V01_upstreamDownstreamV13.csv"
#TARGET_BASIN = 2060022970

#basin_ids =  [TARGET_BASIN]

df = pd.read_csv(inputLocation)
header = df.dtypes

df["HYBAS_ID2"] = df["HYBAS_ID"]
df = df.set_index(["HYBAS_ID2"])


# testing purposes
#df = df[ 0:200]
df_out = df.copy()


df_out['Downstream_HYBAS_IDs'] = "Nodata"
df_out['Downstream_PFAF_IDs'] = "Nodata"
df_out['Basin_HYBAS_IDs'] = "Nodata"
df_out['Basin_PFAF_IDs'] = "Nodata"

print df_out.dtypes

i = 1
for id in df.index:
    print "item: ", i, " id: ",id
    i += 1
    writeID = id
    allDownID = []
    allDownPFAF = []

    sinkHybasID = np.int64(df.loc[id]["NEXT_SINK"])
    sinkPfafID = np.int64(df.loc[sinkHybasID]["PFAF_ID"])


    while id != 0:
        series = df.loc[id]
        downId = np.int64(series["NEXT_DOWN"]) # Next down ID
        if downId != 0 :
            downSeries = df.loc[downId]
            pfafID = np.int64(downSeries["PFAF_ID"])
            allDownID.append(downId)
            allDownPFAF.append(pfafID)
            id = downId
        else:
            # most downstream basin
            if (len(series["Upstream_HYBAS_IDs"]) == 2 ):
                allBasinIDs =  "[" + str(sinkHybasID)+ "]" #super ugly but it works
                allBasinPFAFs ="[" + str(sinkPfafID) + "]"
            else:
                allBasinIDs = series["Upstream_HYBAS_IDs"][:-1] + ", " + str(sinkHybasID) + "]"  # super ugly but it works
                allBasinPFAFs = series["Upstream_PFAF_IDs"][:-1] + ", " + str(sinkPfafID) + "]"
            id = 0
            pass



    df_out.set_value(writeID, 'Downstream_HYBAS_IDs', allDownID)
    df_out.set_value(writeID, 'Downstream_PFAF_IDs',allDownPFAF)
    df_out.set_value(writeID, 'Basin_HYBAS_IDs', allBasinIDs)
    df_out.set_value(writeID, 'Basin_PFAF_IDs',allBasinPFAFs)

    df_out.set_value(writeID, 'NEXT_SINK_PFAF', sinkPfafID )


df_out.to_csv(outputLocation)

print "done"
