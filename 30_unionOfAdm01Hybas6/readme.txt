This step was done using adm01 V2.8 and Hybas6 using arcgis

1) Add unique provinceID to GADM level 1 in QGIS (same as OBJECT ID) 

2) Created Union

3) Removed all fields except AqID, PFAF_ID, ProvinceID and ISO

4) Added unique AQ30ID 


After that I removed the Hybas6 field except HybasID and PFAFID using QGIS

Added column based on rownumber called rutgerID30 to be able to later join to shape


Messages
Executing: Union "hybas_merged_custom_level6_V02 #;adm1 #" C:\Users\Rutger.Hofste\Desktop\werkmap2\unionArcGADM01Hybas6V01.shp ALL # GAPS
Start Time: Thu Jun 08 09:58:55 2017
Reading Features...
Processing Tiles...
Assembling Tile Features...
Succeeded at Thu Jun 08 10:08:20 2017 (Elapsed Time: 9 minutes 25 seconds)
