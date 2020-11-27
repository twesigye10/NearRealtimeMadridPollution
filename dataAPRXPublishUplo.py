# -*- coding: utf-8 -*-
import arcpy, os

arcpy.env.workspace = os.path.join('C:\\', 'MadridPollution', 'ProjectSupportData')
arcpy.env.overwriteOutput = True

# location of the map document
wrkspc = 'C:\\MadridPollution\\ProjectSupportData\\'
serviceName = "madPSurface"

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
aprx = arcpy.mp.ArcGISProject(wrkspc + "ProjectSupportData.aprx")
aprxMap = aprx.listMaps("Map")[0]

arcpy.mp.CreateWebLayerSDDraft(aprxMap, SDdraft, serviceName, 'MY_HOSTED_SERVICES', 'FEATURE_ACCESS',
                               'Madrid', True, True, '', '', '', summary, tags, '', '', '')

# Create service definition
arcpy.StageService_server(SDdraft, SD)

# Upload service definition
arcpy.UploadServiceDefinition_server(SD, 'My Hosted Services', serviceName, '', '', 'FROM_SERVICE_DEFINITION', '', True, '', True, True)
print("Uploaded a new service")
