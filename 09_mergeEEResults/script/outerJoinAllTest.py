import os
import pandas as pd
import ast



inputLocation = "/Users/rutgerhofste/Desktop/werkmap/input/hybas6Results04.csv"
outputLocation = "/Users/rutgerhofste/Desktop/werkmap/output/test.csv"

df = pd.read_csv(inputLocation, index_col="hybas6ID")


df = df.head()

#print df.iloc[1]

series = pd.Series([-9999,-9998], index=[1060000100,1060000010])

df['New'] = series



print "done"