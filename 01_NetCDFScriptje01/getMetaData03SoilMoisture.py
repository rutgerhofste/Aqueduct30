# Since the Time units for Soil Moisture are different, a separate script . days since 1901 vs days since 1900 for the rest of the datasets.

'''
PURPOSE
    Read University of Utrecht files and store as geotiff
    this project use a virtual environment with the following pip installs:
    netcdf4, https://pythongisandstuff.wordpress.com/2016/04/13/installing-gdal-ogr-for-python-on-windows/

PROGRAMMER(S)
    Rutger Hofste
    Chris Slocum
REVISION HISTORY
    20170203 -- GDAL part added
    20161202 -- Rutger changes to work with UU data
    20140320 -- Initial version created and posted online
    20140722 -- Added basic error handling to ncdump
                Thanks to K.-Michael Aye for highlighting the issue
REFERENCES
    netcdf4-python -- http://code.google.com/p/netcdf4-python/
    colormap -- http://matplotlib.org/examples/pylab_examples/custom_cmap.html
    GDAL -- https://pythongisandstuff.wordpress.com/2016/04/13/installing-gdal-ogr-for-python-on-windows/

CAVEATS
    I did not use a robust way to find the filename without extension. Filepath cannot contain periods. No error module built in.



'''

#<editor-fold desc="IMPORTS">
try:
    from osgeo import ogr, osr, gdal
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')
# Enable GDAL/OGR exceptions
gdal.UseExceptions()
import datetime as dt
import numpy as np
from netCDF4 import Dataset
import os
import datetime
#from mpl_toolkits.basemap import Basemap
#from matplotlib.colors import LinearSegmentedColormap
#from matplotlib import colors
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
#</editor-fold>




#<editor-fold desc="Settings">
NETCDFINPUTPATH = os.path.join('C:/',r'Users\Rutger.Hofste\Desktop\werkmap\dataInput')

GEOTIFFINPUTPATH = os.path.join('C:/',r'Users\Rutger.Hofste\Desktop\werkmap\sampleInput')
GEOTIFFINPUTFILENAME = "sampleGeotiff.tiff"
PRINT_METADATA = True
OUTPUTPATH = os.path.join('K:/',r'PCRGlob2WBBigV02\runoff')
#</editor-fold>


def ncdump(nc_fid, verb=True):
    '''
    ncdump outputs dimensions, variables and their attribute information.
    The information is similar to that of NCAR's ncdump utility.
    ncdump requires a valid instance of Dataset.

    Parameters
    ----------
    nc_fid : netCDF4.Dataset
        A netCDF4 dateset object
    verb : Boolean
        whether or not nc_attrs, nc_dims, and nc_vars are printed

    Returns
    -------
    nc_attrs : list
        A Python list of the NetCDF file global attributes
    nc_dims : list
        A Python list of the NetCDF file dimensions
    nc_vars : list
        A Python list of the NetCDF file variables
    '''
    def print_ncattr(key):
        """
        Prints the NetCDF file attributes for a given key

        Parameters
        ----------
        key : unicode
            a valid netCDF4.Dataset.variables key
        """
        try:
            print "\t\ttype:", repr(nc_fid.variables[key].dtype)
            for ncattr in nc_fid.variables[key].ncattrs():
                print '\t\t%s:' % ncattr,\
                      repr(nc_fid.variables[key].getncattr(ncattr))
        except KeyError:
            print "\t\tWARNING: %s does not contain variable attributes" % key

    # NetCDF global attributes
    nc_attrs = nc_fid.ncattrs()
    if verb:
        print "NetCDF Global Attributes:"
        for nc_attr in nc_attrs:
            print '\t%s:' % nc_attr, repr(nc_fid.getncattr(nc_attr))
    nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions
    # Dimension shape information.
    if verb:
        print "NetCDF dimension information:"
        for dim in nc_dims:
            print "\tName:", dim
            print "\t\tsize:", len(nc_fid.dimensions[dim])
            print_ncattr(dim)
    # Variable information.
    nc_vars = [var for var in nc_fid.variables]  # list of nc variables
    if verb:
        print "NetCDF variable information:"
        for var in nc_vars:
            if var not in nc_dims:
                print '\tName:', var
                print "\t\tdimensions:", nc_fid.variables[var].dimensions
                print "\t\tsize:", nc_fid.variables[var].size
                print_ncattr(var)
    return nc_attrs, nc_dims, nc_vars

def saveMap(title,data,OUTPUTPATH,outputFileName):
    # Setup the map. See http://matplotlib.org/basemap/users/mapsetup.html
    # for other projections.
    fig = plt.figure(figsize=(30, 15)) # Dimension in cm?
    fig.suptitle(title)
    m = Basemap(llcrnrlat=-90, urcrnrlat=90,llcrnrlon=-180, urcrnrlon=180, resolution='l', lon_0=0)
    m.drawcoastlines()
    m.drawmapboundary()
    NormalArray = np.ma.getdata(data)
    NormalArray = np.flipud(NormalArray)
    X , Y = np.meshgrid(lons, lats)
    levels = np.linspace(-1, 15, 11)
    #m.contourf(X, Y,NormalArray, levels=levels ,cmap=plt.cm.Spectral, corner_mask= False)

    cmap = mpl.colors.ListedColormap([[1, 1, 1],  # NoData
                                      [255./255, 255./255, 153./255], # Low
                                      [255./255, 230./255, 0./255], # Low - med
                                      [255./255, 153./255, 0./255], # Medium - High
                                      [255./255, 25./255, 0./255], # High
                                      [204./255, 0./255, 20./255],# Very High
                                      [78./255, 78./255, 78./255]]) # NoData
    bounds=[-100000.,0.,0.1,0.2,0.4,0.8,1.1,100]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    m.imshow(NormalArray,cmap=cmap, norm=norm)
    #m.drawmapboundary()

    #plt.show(fig)
    fig.savefig(os.path.join(OUTPUTPATH,outputFileName))
    plt.close()

def readFile(filename):
    filehandle = gdal.Open(filename)
    band1 = filehandle.GetRasterBand(1)
    geotransform = filehandle.GetGeoTransform()
    geoproj = filehandle.GetProjection()
    Z = band1.ReadAsArray()
    xsize = filehandle.RasterXSize
    ysize = filehandle.RasterYSize
    filehandle = None
    return xsize,ysize,geotransform,geoproj,Z

def writeFile(filename,geotransform,geoprojection,data):
    (x,y) = data.shape
    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    # you can change the dataformat but be sure to be able to store negative values including -9999
    dst_datatype = gdal.GDT_Float32
    dst_ds = driver.Create(filename,y,x,1,dst_datatype, [ 'COMPRESS=LZW' ])
    dst_ds.GetRasterBand(1).SetNoDataValue(-9999)
    dst_ds.GetRasterBand(1).WriteArray(data)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(geoprojection)
    dst_ds = None
    return 1

def normalizeTime(time):
    timeNormal =[]
    for i in range(0, len(time)):
        fullDate = days_since_jan_1_1900_to_datetime(time[i])
        timeNormal.append(fullDate)
    return timeNormal

def days_since_jan_1_1900_to_datetime(d):
    return datetime.datetime(1901,1,1) + \
        datetime.timedelta(days=d)


#<editor-fold desc="Metadata">
# get projection and extent from sample Geotiff file
[xsize,ysize,geotransform,geoproj,ZSample] = readFile(os.path.join(GEOTIFFINPUTPATH,GEOTIFFINPUTFILENAME))
files = os.listdir(NETCDFINPUTPATH)


for oneFile in files:
    netCDFInputFileName = oneFile
    print oneFile
    netCDFInputBaseName = netCDFInputFileName.split('.')[0]

    nc_f = os.path.join(NETCDFINPUTPATH,netCDFInputFileName)
    nc_fid = Dataset(nc_f, 'r')  # Dataset is the class behavior to open the file
         # and create an instance of the ncCDF4 class
    nc_attrs, nc_dims, nc_vars = ncdump(nc_fid, PRINT_METADATA)
    parameter = nc_vars[3]

    lats = nc_fid.variables['latitude'][:]  # extract/copy the data
    lons = nc_fid.variables['longitude'][:]
    time = nc_fid.variables['time'][:]
    timeNormal = normalizeTime(time)

    print "Time Minimum: ", min(timeNormal), " Days since 1901-01-01:", min(time)
    print "Time Maximum: ", max(timeNormal), " Days since 1901-01-01:", max(time)
    print "Number of layers", len(timeNormal)

    minLats =  min(lats)
    minLons = min(lons)
    maxLats = max(lats)
    maxLons = max(lons)

    print "%2.30f" %minLats
    print "%2.30f" % minLons
    print "%2.30f" % maxLats
    print "%2.30f" % maxLons



    for i in range(0,len(timeNormal)):
        print timeNormal[i].year

        Z = nc_fid.variables[parameter][i, :, :]
        Z[Z<-9990]= -9999
        Z[Z>1e19] = -9999
        outputFilename = netCDFInputBaseName + "I%0.3dY%0.2dM%0.2d.tif" %(i,timeNormal[i].year,timeNormal[i].month)
        writefilename = os.path.join(OUTPUTPATH,outputFilename)
        writeFile(writefilename,geotransform,geoproj,Z)
        #errorLog =[]


#</editor-fold


"""
# display using python basemap
for i in range(0,2):
    data = nc_fid.variables['bwsi'][i, :, :]
    fullDate = days_since_jan_1_1900_to_datetime(time[i])
    title = 'BWSI Y%0.2d M%0.2d' %(fullDate.year, fullDate.month)
    outputFileName = 'BWSIY%0.2dM%0.2drutger.png' %(fullDate.year, fullDate.month)
    try:
        saveMap(title,data,OUTPUTPATH,outputFileName)
    except:
        errorLog.append(title)
"""







print "Done"
