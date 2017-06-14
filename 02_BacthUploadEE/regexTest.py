import re
import os


LOCAL_FILE_BASEPATH = os.path.join('K:/',r'PCRGlob2WBBigV02')
PARAMETERS = ['demand']

test =[]
test.append("global_historical_PDomWN_month_millionm3_5min_1960_2014I000Y1960M01.tif")
test.append("global_historical_PLivWN_year_millionm3_5min_1960_2014I052Y2012M12.tif")

print re.match(".*year", test[0], flags=0)


print "Done"