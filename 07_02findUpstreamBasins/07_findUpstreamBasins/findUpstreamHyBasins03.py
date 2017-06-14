"""
CATCHMENT LEVEL FLOW ACCUMULATION
September 19, 2015 ; March 17 2017
Author: Tianyi Luo ; Rutger Hofste
"""

import pandas as pd
import numpy as np
import os, ftplib, urllib2
from datetime import datetime, timedelta

# Settings
# Before you run the script, make sure the columns are in the right dtype (int64)


inputLocation = "C:\Users\Rutger.Hofste\Desktop\werkmap\input\hybas_merged_custom_level6_V02.csv"
outputLocation = "C:\Users\Rutger.Hofste\Desktop\werkmap\output\hybas_custom_level6_upstreamV02.csv"
TARGET_BASIN = 2060022970

basin_ids =  [TARGET_BASIN]


df = pd.read_csv(inputLocation)

def find_upstream_catchments(basin_ids, df):
    all_up_catchments =[]
    for i in np.arange(1, 16397, 1):
        if not basin_ids:
            break
        else:
            up_catchments_adjacent = []
            for bid in basin_ids:
                up_ids_idx = df[df['NEXT_DOWNI'] == bid].index.tolist()
                for idx in up_ids_idx :
                    up_id = df.HYBAS_IDIn[idx]
                    up_catchments_adjacent.append(up_id)
            basin_ids = up_catchments_adjacent
            all_up_catchments = all_up_catchments + basin_ids
    return all_up_catchments

def generate_dictionary(df, outputLocation):
    #df_temp = df.drop(['dwnBasinID', 'Area_km2', 'Ua', 'Ui', 'Ud', 'Ca', 'Ci', 'Cd', 'Bt'], axis=1)
    df_temp = df
    up_catchments = []
    for bid in df.HYBAS_IDIn:
        up_catchments.append(find_upstream_catchments([bid], df))
    df_temp['Upstream_Catchments'] = up_catchments
    df_temp.to_csv(outputLocation)
    print "DONE!"

generate_dictionary(df, outputLocation)

#find_upstream_catchments([1060001510], df)


print "done"

