


import os
import pandas as pd
import ast

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

inputLocation = "/Users/rutgerhofste/Desktop/werkmap3/input/hybas6Results11.csv"
outputLocation = "/Users/rutgerhofste/Desktop/werkmap3/output/hybas6ResultsIncUpstream07.csv"

df = pd.read_csv(inputLocation, index_col="hybas6ID")

#df = df[0:100]

df["areaCatchm2"] = df["mean_area30sm2"]*df["count_area30sm2"]


df_out = df.copy()

for index, row in df.iterrows():
    print index

    upstreamCatchments = df.loc[index,"Upstream_Catchments"]
    upstreamCatchments = ast.literal_eval(upstreamCatchments)
    # include basin itself = YES!!!
    upstreamCatchments.append(index)

    df_upstream = df.loc[upstreamCatchments]
    #df_upstream = df.loc[df['hybas6ID'].isin(upstreamCatchments)]
    
    # calculate total values in million m^3
    areaCatch = df_upstream["areaCatchm2"]

    df_upstream["basinArea"] = areaCatch

    df_upstream["basinRunoff"] = (df_upstream["mean_mean1960tm2014totalRunoff_annuaTot"]*areaCatch)/1e6

    df_upstream["basinPTotWN"] = (df_upstream["mean_2014DemandWN"]*areaCatch)/1e6

    
    df_upstream["basinPTotWW"] = (df_upstream["mean_2014DemandWW"]*areaCatch)/1e6


    sumSeries = df_upstream.sum()
    
    upstreamDict= {}
    
    upstreamDict["BasinArea_m2"] =sumSeries["basinArea"]
    upstreamDict["BasinRunoff_Mm3"] =sumSeries["basinRunoff"]
    upstreamDict["BasinPTotWN_Mm3"] =sumSeries["basinPTotWN"]

    upstreamDict["BasinPTotWW_Mm3"] =sumSeries["basinPTotWW"]


    
    for key, value in upstreamDict.iteritems():
        key ="sum" + key
        df_out.loc[index,key] = value

area = df_out["areaCatchm2"]
withdrawal = (df_out["mean_2014DemandWW"]*area)/1e6 #withdrawal in catchment million m^3
consumption = (df_out["mean_2014DemandWN"]*area)/1e6 # consumption in catchment in million m^3

runoffBasin = df_out["sumBasinRunoff_Mm3"] #Upstream plus


df_out["withdrawalCatchMm3"] = withdrawal
df_out["consumptionCatchMm3"] = consumption
df_out["runoffBasinMm3"] = runoffBasin


df_out["WS"] = withdrawal / (runoffBasin + consumption)


df_out.to_csv(outputLocation)



print "done"