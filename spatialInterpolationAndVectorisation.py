# -*- coding: utf-8 -*-
import os
import arcpy

# local variables
gdbLocation = "C:\\MadridPollution\\ProjectSupportData\\Madrid_Sensors.gdb"
arcpy.env.workspace = gdbLocation
arcpy.env.overwriteOutput = True

#           IDW Interpolation
# local variables for IDW interpolation
in_feat = "testmadrid"
zField = "MLAQI"
out_feat = "surfacemadrid"
IDW_Layer = "IDW_Layer"
Output_raster = ""
cellSize = 65
power = 2
# search neighborhood
majSemiaxis = 6000
minSemiaxis = 6000
angle = 0
maxNeighbors = 10
minNeighbors = 3
sectorType = "EIGHT_SECTORS"
searchNeighbourhood = arcpy.SearchNeighborhoodStandard(majSemiaxis, minSemiaxis,
                                                       angle, maxNeighbors,
                                                       minNeighbors, sectorType)
# Enable Geostatistical Analyst license
arcpy.CheckOutExtension("GeoStats")
# IDW interpolation
arcpy.IDW_ga(in_feat, zField, IDW_Layer, Output_raster, cellSize, power, searchNeighbourhood)
# Creating pollution shapes from interpolation
tempEnvironment0 = arcpy.env.extent
arcpy.env.extent = "424753.6621 4462565.9412 456039.9542 4499364.5676"
arcpy.GALayerToContour_ga(IDW_Layer, "FILLED_CONTOUR", out_feat, "DRAFT", "MANUAL", "", "50;100;150;200")
arcpy.env.extent = tempEnvironment0
# Delete the IDW_Layer
arcpy.Delete_management(IDW_Layer)

# Clipping local variables
clip_infeat = out_feat
clip_feat = "DISTRITOS"
clip_outfeat = "clippedFeat"
xy_tolerance = ""
# Clipping out the required extents
arcpy.Clip_analysis(clip_infeat, clip_feat, clip_outfeat, xy_tolerance)
# reproject Features
clipProjected = "clipFeatProj"
arcpy.Project_management(clip_outfeat, clipProjected, "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "ETRS_1989_To_WGS_1984", "PROJCS['ETRS_1989_UTM_Zone_30N',GEOGCS['GCS_ETRS_1989',DATUM['D_ETRS_1989',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-3.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")


# seperate the shape into seperate index categories
sepFeat = clipProjected
arcpy.Select_analysis(sepFeat, "Good", "Classes = 0")
arcpy.Select_analysis(sepFeat, "Acceptable", "Classes = 1")
arcpy.Select_analysis(sepFeat, "Poor", "Classes = 2")
arcpy.Select_analysis(sepFeat, "VeryPoor", "Classes = 3")
print ("This is the last index category")

arcpy.AddMessage("""
**************************************************
***** Finished processing the data in : {0}  *****
**************************************************
""".format(gdbLocation) )
