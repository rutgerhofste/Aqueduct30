First I tried ARCGIS, weird horizontal artefacts

Second try using GDAL (system GDAL form cmd)

gdal_rasterize -a PFAF_12_IN -ot Integer64 -of GTiff -te -180 -90 180 90 -ts 360 180 -co COMPRESS=DEFLATE -co PREDICTOR=1 -co ZLEVEL=6 -l global_Standard_lev00_v1c -a_nodata -9999 C:\Users\Rutger.Hofste\Desktop\werkmap6\global_Standard_lev00_v1c.shp C:\Users\Rutger.Hofste\Desktop\werkmap6\selection\output\test3.tif
