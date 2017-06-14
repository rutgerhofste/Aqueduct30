


import os
import pandas as pd
import ast

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

inputLocation = "/Users/rutgerhofste/Desktop/werkmap/input/hybas6Results08.csv"
outputLocation = "/Users/rutgerhofste/Desktop/werkmap/output/test10.csv"

df = pd.read_csv(inputLocation, index_col="hybas6ID")


#df = df[0:10]

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
    area = df_upstream["sumareaWeighted"]
    df_upstream["basinRunoff"] = (df_upstream["meanrunoffWeighted"]*area)/1e6

    df_upstream["basinPDomWN"] = (df_upstream["meanPDomWNWeighted"]*area)/1e6
    df_upstream["basinPIndWN"] = (df_upstream["meanPIndWNWeighted"]*area)/1e6
    df_upstream["basinPIrrWN"] = (df_upstream["meanPIrrWNWeighted"]*area)/1e6
    df_upstream["basinPLivWN"] = (df_upstream["meanPLivWNWeighted"]*area)/1e6
    df_upstream["basinPTotWN"] = (df_upstream["meanPTotWNWeighted"]*area)/1e6
    
    df_upstream["basinPDomWW"] = (df_upstream["meanPDomWWWeighted"]*area)/1e6
    df_upstream["basinPIndWW"] = (df_upstream["meanPIndWWWeighted"]*area)/1e6
    df_upstream["basinPIrrWW"] = (df_upstream["meanPIrrWWWeighted"]*area)/1e6
    df_upstream["basinPLivWW"] = (df_upstream["meanPLivWWWeighted"]*area)/1e6
    df_upstream["basinPTotWW"] = (df_upstream["meanPTotWWWeighted"]*area)/1e6
    
    sumSeries = df_upstream.sum()
    
    upstreamDict= {}
    
    upstreamDict["BasinArea_m2"] =sumSeries["sumareaWeighted"]
    upstreamDict["BasinRunoff_Mm3"] =sumSeries["basinRunoff"]
    upstreamDict["BasinPDomWN_Mm3"] =sumSeries["basinPDomWN"]
    upstreamDict["BasinPIndWN_Mm3"] =sumSeries["basinPIndWN"]
    upstreamDict["BasinPIrrWN_Mm3"] =sumSeries["basinPIrrWN"]
    upstreamDict["BasinPLivWN_Mm3"] =sumSeries["basinPLivWN"]
    upstreamDict["BasinPTotWN_Mm3"] =sumSeries["basinPTotWN"]
    
    upstreamDict["BasinPDomWW_Mm3"] =sumSeries["basinPDomWW"]
    upstreamDict["BasinPIndWW_Mm3"] =sumSeries["basinPIndWW"]
    upstreamDict["BasinPIrrWW_Mm3"] =sumSeries["basinPIrrWW"]
    upstreamDict["BasinPLivWW_Mm3"] =sumSeries["basinPLivWW"]
    upstreamDict["BasinPTotWW_Mm3"] =sumSeries["basinPTotWW"]


    
    for key, value in upstreamDict.iteritems():
        key ="sum" + key
        df_out.loc[index,key] = value

area = df_out["sumareaWeighted"]
withdrawal = (df_out["meanPTotWWWeighted"]*area)/1e6 #withdrawal in catchment million m^3
consumption = (df_out["meanPTotWNWeighted"]*area)/1e6 # consumption in catchment in million m^3

runoffBasin = df_out["sumBasinRunoff_Mm3"] #Upstream plus

df_out["withdrawal"] = withdrawal
df_out["consumption"] = consumption
df_out["runoffBasin"] = runoffBasin


df_out["WS"] = withdrawal / (runoffBasin + consumption)


df_out.to_csv(outputLocation)



print "done"