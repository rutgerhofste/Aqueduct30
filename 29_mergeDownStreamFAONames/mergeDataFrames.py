# super simple script to merge two dataframes
# Rutger Hofste June 6 2017

import pandas as pd
import numpy as np

inputLocationLeft = "input/hybas_merged_standard_level6_V01_upstreamDownstreamV13.csv"
inputLocationRight = "input/PFAF_joinedWithFAONamesMergedV05.csv"

outputLocation = "output/Hybas6_FAONamesUpstreamDownstreamV05.csv"

df_left = pd.read_csv(inputLocationLeft,encoding="utf-8")
df_right = pd.read_csv(inputLocationRight,encoding="utf-8")

header_left = df_left.dtypes
header_right = df_right.dtypes

df_out = df_left.merge(df_right,how="outer",left_on="PFAF_ID",right_on="PFAF_ID")

df_out.to_csv(outputLocation,encoding="UTF-8")


print "Done"