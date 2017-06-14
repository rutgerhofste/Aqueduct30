import os
import pandas as pd
import multiprocessing as mp
import ast
import time
import numpy as np
import logging

# Rutger Hofste May 10 2017
# this script is written for Compute Engine. Copy folder to CE, install dependencies and run code
# this code has been altered to allow parallel processing


inputLocation = "input/pfaf_merged_standard_level6_V01_upstreamV14_resultsV01.csv"
inputParameterPath = "input/parameters"
outputLocation = "output01.csv"

df_full = pd.read_csv(inputLocation)
df_full = df_full[0:100]
df_full = df_full.set_index("PFAF_ID")

indices_full = df_full.index.values
indices_split = np.array_split(indices_full, mp.cpu_count())

files = os.listdir(inputParameterPath)
parameterList = []
for oneFile in files:
    if oneFile.endswith(".csv"):
        [fileName, extension] = oneFile.split(".")
        parameterList.append(fileName[:-3])



def addUpstream(listje):
    df_full_temp = df_full.copy()
    df_part_temp = df_full_temp[df_full_temp.index.isin(listje)]
    df_part_temp2 = df_part_temp.copy()
    df_out = df_part_temp2.copy()
    i = 0
    for index, row in df_part_temp2.iterrows():
        i += 1
        print "i: ",i  ," index: ", index
        try:
            upstreamCatchments = df_part_temp2.loc[index, "Upstream_PFAF_IDs"]
            upstreamCatchments = ast.literal_eval(upstreamCatchments)
            df_upstream = df_full_temp.loc[upstreamCatchments]
            area = df_upstream["countarea30sm2"] * df_upstream["meanarea30sm2"]

            df_new = pd.DataFrame()
            df_new["aream2"] = area

            for parameter in parameterList:
                df_new["count" + parameter] = df_upstream["count" + parameter]
                df_new["volumem3" + parameter] = area * df_upstream["mean" + parameter]

            sumSeries = df_new.sum()

            for key, value in sumSeries.iteritems():
                newKey = "upstream_sum_" + key
                df_out.loc[index, newKey] = value
            df_out.loc[index, "errorCode"] = 0
        except:
            print "error"
            df_out.loc[index, "errorCode"] = 1
            pass

    return df_out

if __name__ == '__main__':
    mp.log_to_stderr()
    logger = mp.get_logger()
    logger.setLevel(logging.INFO)
    pool = mp.Pool(mp.cpu_count())
    df_out = pd.concat(pool.map(addUpstream, indices_split))
    #df_out = pool.map(addUpstream, indices_split)
    pool.close()
    df_out.to_csv(outputLocation)
    pass
    pass


"""

def parallelize_dataframe(df, func):
    df_split = np.array_split(df, num_partitions)
    pool = mp.Pool(num_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


def addUpstreamData(data):
    i = 0
    for index, row in df.iterrows():
        i += 1
        time_elapsed = time.time() - start_time
        try:
            upstreamCatchments = df.loc[index, "Upstream_PFAF_IDs"]
            upstreamCatchments = ast.literal_eval(upstreamCatchments)
            df_upstream = df.loc[upstreamCatchments]
            area = df_upstream["countarea30sm2"] * df_upstream["meanarea30sm2"]

            df_new = pd.DataFrame()
            df_new["aream2"] = area

            for parameter in parameterList:
                df_new["count" + parameter] = df_upstream["count" + parameter]
                df_new["volumem3" + parameter] = area * df_upstream["mean" + parameter]

            sumSeries = df_new.sum()

            for key, value in sumSeries.iteritems():
                newKey = "upstream_sum_" + key
                df_out.loc[index, newKey] = value
            df_out.loc[index, "errorCode"] = 0
        except:
            print "ERROR"
            df_out.loc[index, "errorCode"] = 1
            errorlog.append(index)

    return df_out




if __name__ == '__main__':
    start_time = time.time()
    errorlog = []
    print "number of cores", mp.cpu_count()
    num_partitions = mp.cpu_count()  # number of partitions to split dataframe
    num_cores = mp.cpu_count()  # number of cores on your machine

    inputLocation = "input/pfaf_merged_standard_level6_V01_upstreamV14_resultsV01.csv"
    inputParameterPath = "input/parameters"
    outputLocation = "testParLoop01.csv"

    df_temp = pd.read_csv(inputLocation)
    df_temp = df_temp[0:100]

    df = df_temp.set_index("PFAF_ID")

    files = os.listdir(inputParameterPath)
    parameterList = []
    for oneFile in files:
        if oneFile.endswith(".csv"):
            [fileName, extension] = oneFile.split(".")
            parameterList.append(fileName[:-3])

    df_out = parallelize_dataframe(df, addUpstreamData)
    df_out.to_csv(outputLocation)

"""














