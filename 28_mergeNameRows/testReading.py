import pandas as pd
import numpy as np
import ast
inputLocation = "Hybas6_joinedWithFAONamesMergedV02.csv"

df = pd.read_csv(inputLocation,encoding="utf-8")
df = df.set_index("HYBAS_ID")

df[0:10]
print(df.index.values)

upstreamCatchments = df.loc[1060000100, "MAJ_NAME"]
upstreamCatchments2 = ast.literal_eval(upstreamCatchments)



print "Done"