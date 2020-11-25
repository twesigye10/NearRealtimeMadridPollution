# -*- coding: utf-8 -*-
import urllib.request
import os
import arcpy
import dataAggregator  # calling the aggregation module
import madpolindexcalculation  # calling the index calculation module


arcpy.env.workspace = "C:\\MadridPollution\\ToneDev\\Madrid_Sensors.gdb"
arcpy.env.overwriteOutput = True

# local variables for feature class creation
out_path = arcpy.env.workspace
out_name = "testmadrid"
geometry_type = "POINT"
has_m = "DISABLED"
has_z = "DISABLED"
# projected coordinate system used for the area around madrid
sr = arcpy.SpatialReference(25830)
# Create empty point Featureclass
arcpy.CreateFeatureclass_management(out_path, out_name, geometry_type, "", has_m, has_z, sr)

empData = out_name


# adding required fields
def addRFields(featLyr):
    nFieldName = "stnID"
    if len(arcpy.ListFields(featLyr, nFieldName)) == 0:
        arcpy.AddField_management(featLyr, nFieldName, "TEXT")
    nFieldName = "stnName"
    if len(arcpy.ListFields(featLyr, nFieldName)) == 0:
        arcpy.AddField_management(featLyr, nFieldName, "TEXT")
    nFieldName = "stnType"
    if len(arcpy.ListFields(featLyr, nFieldName)) == 0:
        arcpy.AddField_management(featLyr, nFieldName, "TEXT")
    nFieldName = "stnElev"
    if len(arcpy.ListFields(featLyr, nFieldName)) == 0:
        arcpy.AddField_management(featLyr, nFieldName, "SHORT")
    nFieldName = "MLAQI"
    if len(arcpy.ListFields(featLyr, nFieldName)) == 0:
        arcpy.AddField_management(featLyr, nFieldName, "SHORT")


# check if fields are added
addRFields(empData)

stnLoc = [['004', 'Plaza de España', 439577.503, 4475070.366, 637, 'Urbana de tráfico'],
    ['008', 'Escuelas Aguirre', 442117.68, 4474786.082, 672, 'Urbana de tráfico'],
    ['011', 'Ramón y Cajal', 442567.611, 4478088.964, 708, 'Urbana de tráfico'],
    ['016', 'Arturo Soria', 445788.017, 4476804.759, 698, 'Urbana de fondo'],
    ['017', 'Villaverde', 439420.566, 4466527.998, 601, 'Urbana de fondo'],
    ['018', 'Farolillo', 437893.845, 4471845.515, 581, 'Urbana de fondo'],
    ['024', 'Casa de Campo', 436601.241, 4474586.797, 645, 'Suburbana'],
    ['027', 'Barajas Pueblo', 450835.949, 4480855.369, 631, 'Urbana de fondo'],
    ['035', 'Plaza del Carmen', 440344.765, 4474535.745, 657, 'Urbana de fondo'],
    ['036', 'Moratalaz', 445254.758, 4473251.64, 671, 'Urbana de tráfico'],
    ['038', 'Cuatro Caminos', 440036.799, 4477465.145, 699, 'Urbana de tráfico'],
    ['039', 'Barrio del Pilar', 439693.285, 4481085.951, 673, 'Urbana de tráfico'],
    ['040', 'Vallecas', 444705.01, 4471040.179, 677, 'Urbana de fondo'],
    ['047', 'Méndez Álvaro', 441734.865, 4472167.017, 609, 'Urbana de fondo'],
    ['048', 'Castellana', 441455.003, 4476789.943, 676, 'Urbana de tráfico'],
    ['049', 'Parque del Retiro', 442095.972, 4473986.767, 662, 'Urbana de fondo'],
    ['050', 'Plaza Castilla', 441622.45, 4479674.926, 728, 'Urbana de tráfico'],
    ['054', 'Ensanche de Vallecas', 448055.403, 4469329.231, 630, 'Urbana de fondo'],
    ['055', 'Urbanización Embajada', 450784.046, 4479256.762, 619, 'Urbana de fondo'],
    ['056', 'Plaza Fernández Ladreda', 439003.502, 4470704.937, 605, 'Urbana de tráfico'],
    ['057', 'Sanchinarro', 444026.471, 4482834.185, 700, 'Urbana de fondo'],
    ['058', 'El Pardo', 434382.749, 4485555.056, 616, 'Suburbana'],
    ['059', 'Juan Carlos I', 448379.789, 4479557.516, 669, 'Suburbana'],
    ['060', 'Tres Olivos', 441559.491, 4483537.375, 715, 'Urbana de fondo']]


# Adding points and updating the fields
fields = ["SHAPE@XY", "stnID", "stnName", "stnType", "stnElev", "MLAQI"]

#      Fetching Data from the madrid city council URL

source = "http://www.mambiente.munimadrid.es/opendata/horario.txt"
# store the decoded data in a 2D list
raw_data = dataAggregator.prepare_raw_data(source)

pldata = dataAggregator.aggregator_stn_data(raw_data)
dWI = madpolindexcalculation.dataIndices(pldata)


def usedStnData(a, b):
    # retrieve only stations with MLAQI measurements
    stnLocUsed = []
    kt = len(a)
    i = 0
    for i in range(kt):
        if a[i][0] in b:
            listVal = a[i]
            stnLocUsed.append(listVal)
            i += 1
    # update the used stations with the index
    ktused = len(stnLocUsed)
    j = 0
    for j in range(ktused):
        indIndex = b.index(stnLocUsed[j][0])+1
        stnLocUsed[j].append(b[indIndex])
        j += 1
    # print stnLocUsed
    return stnLocUsed
    pass


# print usedStnData(stnLoc, dWI)


# organise the data according to feature class structure using draftData
draftData = []
shpData = usedStnData(stnLoc, dWI)
for rowStn in shpData:
    ptLoc = (rowStn[2], rowStn[3])
    ptID = rowStn[0]
    ptNam = rowStn[1]
    ptTy = rowStn[5]
    ptEl = rowStn[4]
    ptInd = rowStn[6]
    ptdec = (ptLoc, ptID, ptNam, ptTy, ptEl, ptInd)
    draftData.append(ptdec)
# insert the data into the feature class
with arcpy.da.InsertCursor(empData, fields) as updLyr:
        for row in draftData:
            updLyr.insertRow(row)

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
arcpy.Project_management("clippedFeat", "clipFeatProj", "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "ETRS_1989_To_WGS_1984", "PROJCS['ETRS_1989_UTM_Zone_30N',GEOGCS['GCS_ETRS_1989',DATUM['D_ETRS_1989',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-3.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")


# seperate the shape into seperate index categories
sepFeat = clipProjected
arcpy.Select_analysis(sepFeat, "Good", "Classes = 0")
arcpy.Select_analysis(sepFeat, "Acceptable", "Classes = 1")
arcpy.Select_analysis(sepFeat, "Poor", "Classes = 2")
arcpy.Select_analysis(sepFeat, "VeryPoor", "Classes = 3")
print ("This is the last index category")
