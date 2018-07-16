# -*- coding: utf-8 -*-
import arcpy
import os

arcpy.env.overwriteOutput = True

# Referencing the project and its contents
projLoc = 'C:\\MadridPollution\\ToneDev\\'
aprx = arcpy.mp.ArcGISProject(projLoc+"ToneDev.aprx")
aprxMap = aprx.listMaps("Map")[0]

# remove existing layers from the map inside the project
lyrs = aprxMap.listLayers()
for lyr in lyrs:
    aprxMap.removeLayer(lyr)

# add the updated layers to the map inside the project
aprxMap.addDataFromPath(projLoc + "Madrid_Sensors.gdb\\VeryPoor")
aprxMap.addDataFromPath(projLoc + "Madrid_Sensors.gdb\\Poor")
aprxMap.addDataFromPath(projLoc + "Madrid_Sensors.gdb\\Acceptable")
aprxMap.addDataFromPath(projLoc + "Madrid_Sensors.gdb\\Good")


# Reference symbology sources
symb1 = projLoc + "Good.lyrx"
symb2 = projLoc + "Acceptable.lyrx"
symb3 = projLoc + "Poor.lyrx"
symb4 = projLoc + "VeryPoor.lyrx"

# apply symbology to the current layers in the document
doclyrs = aprxMap.listLayers()
arcpy.ApplySymbologyFromLayer_management(doclyrs[0], symb1)
arcpy.ApplySymbologyFromLayer_management(doclyrs[1], symb2)
arcpy.ApplySymbologyFromLayer_management(doclyrs[2], symb3)
arcpy.ApplySymbologyFromLayer_management(doclyrs[3], symb4)

aprx.save()
del aprx
