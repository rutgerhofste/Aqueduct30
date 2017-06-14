import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import pandas as pd
import numpy as np

inputLocation = "hybas6JoinedFAOV03UTF8V02.csv"
outputLocation = "output/PFAF_joinedWithFAONamesMergedV05.csv"

df = pd.read_csv(inputLocation,encoding="utf-8")

#df = df[0:1000]

header = df.dtypes

df['PFAF_ID'] = df['PFAF_ID'].astype(np.int64)
df = df.set_index("PFAF_ID")

header2 = df.dtypes

#df = df.loc[7060820630] test Unicode characters

series = df.groupby('PFAF_ID')['SUB_NAME'].apply(list)
series2 = df.groupby('PFAF_ID')['MAJ_NAME'].apply(list)


df_new1 = series.to_frame()
df_new2 = series2.to_frame()


df_out = df_new1.merge(right = df_new2, how = "outer", left_index = True, right_index = True )

df_out.to_csv(outputLocation,encoding="UTF-8")

print "Done"