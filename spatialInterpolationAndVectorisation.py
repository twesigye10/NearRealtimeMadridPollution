# -*- coding: utf-8 -*-
import os
import arcpy

# local variables
gdbLocation = "C:\\MadridPollution\\ProjectSupportData\\Madrid_Sensors.gdb"
arcpy.env.workspace = gdbLocation
arcpy.env.overwriteOutput = True

#           IDW Interpolation
arcpy.AddMessage("""
***** Started Spatial Interpolation  *****
""" )

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
processing_sr = arcpy.SpatialReference(25830)
mapping_sr = arcpy.SpatialReference(3857)
arcpy.Project_management(clip_outfeat, clipProjected, mapping_sr, "ETRS_1989_To_WGS_1984", processing_sr)

# seperate the shape into seperate index categories
arcpy.Select_analysis(clipProjected, "Good", "Classes = 0")
arcpy.Select_analysis(clipProjected, "Acceptable", "Classes = 1")
arcpy.Select_analysis(clipProjected, "Poor", "Classes = 2")
arcpy.Select_analysis(clipProjected, "VeryPoor", "Classes = 3")
print ("This is the last index category")

arcpy.AddMessage("""
***** Finished Spatial Interpolation  *****
""" )
