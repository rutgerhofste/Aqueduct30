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

inputLocation = "C:\Users\Rutger.Hofste\Desktop\werkmap\input\GDBD_MASTER.csv"
outputLocation = "C:\Users\Rutger.Hofste\Desktop\werkmap\output\output01.csv"
TARGET_BASIN = 5746




def csv_to_pd_dataframe(csv_path):
    df = pd.DataFrame.from_csv(csv_path, index_col=0)
    return df


def find_upstream_catchments(basin_ids, df):
    all_up_catchments = []
    for i in np.arange(1, 15007, 1):
        if not basin_ids:
            break
        else:
            up_catchments_adjacent = []
            for bid in basin_ids:
                up_ids_idx = df[df['dwnBasinID'] == bid].index.tolist()
                for idx in up_ids_idx:
                    up_id = df.BasinID[idx]
                    up_catchments_adjacent.append(up_id)
            basin_ids = up_catchments_adjacent
            all_up_catchments = all_up_catchments + basin_ids
    print all_up_catchments
    return all_up_catchments


def generate_dictionary(df, out_csv_path):
    df_temp = df.drop(['dwnBasinID', 'Area_km2', 'Ua', 'Ui', 'Ud', 'Ca', 'Ci', 'Cd', 'Bt'], axis=1)
    up_catchments = []
    for bid in df.BasinID:
        up_catchments.append(find_upstream_catchments([bid], df))
    df_temp['Upstream_Catchments'] = up_catchments
    df_temp.to_csv(out_csv_path)
    print "DONE!"


if __name__ == '__main__':

    gdbd_df = csv_to_pd_dataframe(inputLocation)
    #generate_dictionary(gdbd_df, outputLocation)

    find_upstream_catchments([TARGET_BASIN], gdbd_df)


