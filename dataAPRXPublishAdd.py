# -*- coding: utf-8 -*-
import arcpy, os
from arcgis.gis import GIS

arcpy.env.workspace = os.path.join('C:\\', 'MadridPollution', 'ToneDev')
arcpy.env.overwriteOutput = True

# location of the map document
wrkspc = 'C:\\MadridPollution\\ToneDev\\'
serviceName = "madPSurface1"
portal = "http://www.arcgis.com" # Can also reference a local portal
user = "twesigye_uji"
password = "y20tplt18jabs"

# paths for the required files
SDdraft = os.path.join(wrkspc, serviceName + ".sddraft")
SD = os.path.join(wrkspc, serviceName + ".sd")

# provide summary and tags of the service
summary = 'Pollution surface for madrid city generated from MLAQI'
tags = 'Public health, Madrid city, air pollution, air quality'

# delete the SDDraft and SD files if they exist on the system.
if os.path.exists(SDdraft):
    arcpy.Delete_management(SDdraft)
if os.path.exists(SD):
    arcpy.Delete_management(SD)

# Location of the project and map
aprx = arcpy.mp.ArcGISProject(wrkspc + "ToneDev.aprx")
aprxMap = aprx.listMaps("Map")[0]

arcpy.mp.CreateWebLayerSDDraft(aprxMap, SDdraft, serviceName, 'MY_HOSTED_SERVICES', 'FEATURE_ACCESS',
                               'Madrid', True, True, '', '', '', summary, tags, '', '', '')

# Create service definition
arcpy.StageService_server(SDdraft, SD)

# connect to the portal
print("Connecting to {}".format(portal))
gis = GIS(portal, user, password)

sdItem = gis.content.add({}, data=SD)
sdItem.publish(overwrite=True)
print("Published a new service")
