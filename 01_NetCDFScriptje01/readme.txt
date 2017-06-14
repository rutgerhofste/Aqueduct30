This script will store every individual layer from NetCDF4 to geotiff. I will use Yoshi's name for the layers and parameters. 

The goal is to upload them to google cloud storage from where it can be uploaded to Earth Engine. 

Changed NoData value from -9999.900390625 (artefact of PCR) to -9999 using GDAL

