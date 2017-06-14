# Author: Rutger.Hofste , Creation Date (MM/DD/YYYY): 5/12/2017

import os
import pandas as pd
import numpy as np

import multiprocessing as mp

inputLocation = "input/output02.csv"
outputLocation = "calculatedWS01.csv"

df_full = pd.read_csv(inputLocation)
#df_full = df_full[0:100]
df_full = df_full.set_index("PFAF_ID")

df_out = df_full.copy()

# Area
df_out["local_sum_aream2"] = df_full["meanarea30sm2"] * df_full["countarea30sm2"]

# Total local WW volume



df_out["local_sum_volumem3_TotWW_yearY2014"] = \
                            df_out["local_sum_aream2"]*df_full["meanDomWW_yearY2014M12"] +\
                            df_out["local_sum_aream2"]*df_full["meanIndWW_yearY2014M12"] +\
                            df_out["local_sum_aream2"]*df_full["meanIrrWW_yearY2014M12"] +\
                            df_out["local_sum_aream2"]*df_full["meanLivWN_yearY2014M12"]  # there is no LivWW

df_out["local_sum_volumem3_TotWN_yearY2014"] = \
                            df_out["local_sum_aream2"]*df_full["meanDomWN_yearY2014M12"] +\
                            df_out["local_sum_aream2"]*df_full["meanIndWN_yearY2014M12"] +\
                            df_out["local_sum_aream2"]*df_full["meanIrrWN_yearY2014M12"] +\
                            df_out["local_sum_aream2"]*df_full["meanLivWN_yearY2014M12"]


df_out["upstream_sum_volumem3_TotWW_yearY2014"] = \
                            df_out["upstream_sum_volumem3DomWW_yearY2014M12"] +\
                            df_out["upstream_sum_volumem3IndWW_yearY2014M12"] +\
                            df_out["upstream_sum_volumem3IrrWW_yearY2014M12"] +\
                            df_out["upstream_sum_volumem3LivWN_yearY2014M12"]

df_out["upstream_sum_volumem3_TotWN_yearY2014"] = \
                            df_out["upstream_sum_volumem3DomWN_yearY2014M12"] +\
                            df_out["upstream_sum_volumem3IndWN_yearY2014M12"] +\
                            df_out["upstream_sum_volumem3IrrWN_yearY2014M12"] +\
                            df_out["upstream_sum_volumem3LivWN_yearY2014M12"]


df_out["local_sum_volumem3_Runoff_yearY2014"] = \
                            df_out["local_sum_aream2"]*df_full["meanrunoff_annua"]

# WS = Local WW / (avail runoff)  = Local WW / (Runoff_up + Runoff_local - WN_up)
df_out["ws_yearY2014"] = df_out["local_sum_volumem3_TotWW_yearY2014"] / (df_out["local_sum_volumem3_Runoff_yearY2014"] + df_out["upstream_sum_volumem3runoff_annua"] - df_out["upstream_sum_volumem3_TotWN_yearY2014"])



# Monthly

def addMonthly(month):

    df_out[(("local_sum_volumem3_TotWW_monthY2014M%02.d")%month)] = \
                                df_out["local_sum_aream2"]*df_full[(("meanDomWW_monthY2014M%0.2d")%month)] +\
                                df_out["local_sum_aream2"]*df_full[(("meanIndWW_monthY2014M%0.2d")%month)] +\
                                df_out["local_sum_aream2"]*df_full[(("meanIrrWW_monthY2014M%0.2d")%month)] +\
                                df_out["local_sum_aream2"]*df_full[(("meanLivWN_monthY2014M%0.2d")%month)] # there is no LivWW


    df_out[(("local_sum_volumem3_TotWN_monthY2014M%02.d")%month)] = \
                                df_out["local_sum_aream2"]*df_full[(("meanDomWN_monthY2014M%0.2d")%month)] +\
                                df_out["local_sum_aream2"]*df_full[(("meanIndWN_monthY2014M%0.2d")%month)] +\
                                df_out["local_sum_aream2"]*df_full[(("meanIrrWN_monthY2014M%0.2d")%month)] +\
                                df_out["local_sum_aream2"]*df_full[(("meanLivWN_monthY2014M%0.2d")%month)]

    df_out[(("upstream_sum_volumem3_TotWW_monthY2014M%0.2d")%month)] = \
                                df_out[(("upstream_sum_volumem3DomWW_monthY2014M%0.2d")%month)] +\
                                df_out[(("upstream_sum_volumem3IndWW_monthY2014M%0.2d")%month)] +\
                                df_out[(("upstream_sum_volumem3IrrWW_monthY2014M%0.2d")%month)] +\
                                df_out[(("upstream_sum_volumem3LivWN_monthY2014M%0.2d")%month)]

    df_out[(("upstream_sum_volumem3_TotWN_monthY2014M%0.2d")%month)] = \
                                df_out[(("upstream_sum_volumem3DomWN_monthY2014M%0.2d")%month)] +\
                                df_out[(("upstream_sum_volumem3IndWN_monthY2014M%0.2d")%month)] +\
                                df_out[(("upstream_sum_volumem3IrrWN_monthY2014M%0.2d")%month)] +\
                                df_out[(("upstream_sum_volumem3LivWN_monthY2014M%0.2d")%month)]

    df_out[(("local_sum_volumem3_Runoff_monthY2014M%0.2d")%month)] = \
                                df_out["local_sum_aream2"] * df_full[(("meanrunoff_month_M%0.2d")%month)]


    # WS = Local WW / (avail runoff)  = Local WW / (Runoff_up + Runoff_local - WN_up)
    df_out[(("ws_monthY2014M%0.2d")%month)] = df_out[(("local_sum_volumem3_TotWW_monthY2014M%02.d")%month)] / (
    df_out[(("local_sum_volumem3_Runoff_monthY2014M%0.2d")%month)] + df_out[(("upstream_sum_volumem3runoff_month_M%02.d")%month)] - df_out[(("upstream_sum_volumem3_TotWN_monthY2014M%0.2d")%month)])

    return 1


for month in range(1,13):
    print month
    addMonthly(month)


df_out.replace([np.inf, -np.inf], np.nan)
df_out.to_csv(outputLocation)


print "Done"