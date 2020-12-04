# -*- coding: utf-8 -*-
import arcpy, os
from arcgis.gis import GIS

arcpy.env.workspace = os.path.join('C:\\', 'MadridPollution', 'ProjectSupportData')
arcpy.env.overwriteOutput = True

# location of the map document
wrkspc = 'C:\\MadridPollution\\ProjectSupportData\\'
serviceName = "madridPollutionSurface"
portal = "https://www.arcgis.com" # Can also reference a local portal
user = "user_name"
password = "pass_word"

# Set sharing options
shrOrg = True
shrEveryone = True
shrGroups = ""

# paths for the required files
SDdraft = os.path.join(wrkspc, serviceName + ".sddraft")
SD = os.path.join(wrkspc, serviceName + ".sd")
thumbn  = os.path.join(wrkspc, "MLAQI.jpg")

# provide summary and tags of the service
summary = 'Pollution surface for madrid city generated from MLAQI'
tags = 'Public health, Madrid city, air pollution, air quality'

# delete the SDDraft and SD files if they exist on the system.
if os.path.exists(SDdraft):
    arcpy.Delete_management(SDdraft)
if os.path.exists(SD):
    arcpy.Delete_management(SD)

# Location of the project and map
aprx = arcpy.mp.ArcGISProject(wrkspc + "ProjectSupportData.aprx")
aprxMap = aprx.listMaps("Map")[0]

arcpy.mp.CreateWebLayerSDDraft(aprxMap, SDdraft, serviceName, 'MY_HOSTED_SERVICES', 'FEATURE_ACCESS',
                               'Madrid', True, True, '', '', '', summary, tags, '', '', '')

# Create service definition
arcpy.StageService_server(SDdraft, SD)

# connect to the portal
print("Connecting to {}".format(portal))
gis = GIS(portal, user, password)

# Find the SD, update it, publish /w overwrite and set sharing
sdItem = gis.content.search("{} AND owner:{}".format(serviceName, user),
                            item_type="Service Definition")[0]

sdItem.update(data=SD, thumbnail=thumbn)
fs = sdItem.publish(overwrite=True)

if shrOrg or shrEveryone or shrGroups:
  print("Setting sharing options...")
  fs.share(org=shrOrg, everyone=shrEveryone, groups=shrGroups)

print("Finished updating and sharing: {} - ID: {}".format(fs.title, fs.id))
