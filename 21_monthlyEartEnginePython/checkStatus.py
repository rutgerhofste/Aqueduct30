import ee
import pandas as pd
from retrying import retry
ee.Initialize()

# specified by user:
outPutPath = "C:\Users\Rutger.Hofste\Desktop\werkmap\output\exportTaskListComplete03.csv"
maxTasks = 6000 #Set maximum number of tasks to include in csv file.

taskList = ee.batch.Task.list()
df = pd.DataFrame()

@retry(wait_exponential_multiplier=10000, wait_exponential_max=100000)
def checkStatus(task):
    return ee.batch.Task.status(task)

for i in range(0,min(len(taskList),maxTasks)):
    dictNew = checkStatus(taskList[i])
    dfNew = pd.DataFrame(dictNew, index=[i])
    try:
        dfNew["calctime(min)"] = (dfNew["update_timestamp_ms"]-dfNew["start_timestamp_ms"])/(1000*60)
        dfNew["queuetime(min)"] = (dfNew["start_timestamp_ms"]-dfNew["creation_timestamp_ms"])/(1000*60)
        dfNew["runtime(min)"]= dfNew["queuetime(min)"]+dfNew["calctime(min)"]
    except:
        pass
    df = df.append(dfNew)
    print i

df.to_csv(path_or_buf=outPutPath)

print "done"


