# -*- coding: utf-8 -*-
import os
import arcpy
import dataAggregator  # calling the aggregation module
import madpolindexcalculation  # calling the index calculation module


# Functions
def create_fc_from_list(a_gdb_name, a_feature, a_geomtype, a_has_m, a_has_z, a_sr ):
    if arcpy.Exists(a_feature):
        arcpy.AddMessage('The feature : {0}, already exists in the database : {1}'.format(a_feature.split("\\")[-1], (a_gdb_name.split("\\")[-1])[:-4]))
    else:
        # Create empty FeatureClasses
        arcpy.CreateFeatureclass_management(a_gdb_name + "\\", a_feature, a_geomtype, "", a_has_m, a_has_z, a_sr)
        arcpy.AddMessage('Created new feature : {0}, in the database : {1}'.format(a_feature.split("\\")[-1], (a_gdb_name.split("\\")[-1])[:-4]))


def create_field_from_list(a_feature, a_list):
    if len(arcpy.ListFields(a_feature, a_list[0])) == 0:
        arcpy.AddField_management(a_feature, a_list[0], a_list[1], a_list[2], a_list[3], a_list[4], a_list[5],
                                  a_list[6], a_list[7], a_list[8])
        arcpy.AddMessage('Fc : {0} , added new field : {1} '.format(a_feature.split("\\")[-1], a_list[0]))
    else:
        arcpy.AddMessage('Fc : {0} , already has field : {1} '.format(a_feature.split("\\")[-1], a_list[0]))


def formatted_stn_data_with_mlaqi(a, b):
    # retrieve only stations with MLAQI measurements
    stn_loc_used = []
    kt = len(a)
    i = 0
    for i in range(kt):
        if a[i][0] in b:
            list_data = a[i]
            mlaqi_stn_index = b.index(list_data[0])+1
            # update the station data with the index
            list_data.append(b[mlaqi_stn_index])
            stn_loc_used.append(list_data)
            i += 1

    # organise the data according to feature class structure
    formatted_stn_data = []
    for row_stn in stn_loc_used:
        pt_loc, pt_id, pt_nam, pt_ty, pt_el, pt_ind = (row_stn[2], row_stn[3]), row_stn[0], row_stn[1], row_stn[5], row_stn[4], row_stn[6]
        ptdec = (pt_loc, pt_id, pt_nam, pt_ty, pt_el, pt_ind)
        formatted_stn_data.append(ptdec)

    return formatted_stn_data


# local variables
gdbLocation = "C:\\MadridPollution\\ProjectSupportData\\Madrid_Sensors.gdb"
arcpy.env.workspace = gdbLocation
arcpy.env.overwriteOutput = True

out_name = "testmadrid"
geometry_type = "POINT"
has_m = "DISABLED"
has_z = "DISABLED"
# projected coordinate system used for the area around madrid
sr = arcpy.SpatialReference(25830)
# required fields
feilds_to_add_flist = [
        ["stnID", "TEXT", "", "", "", "", "", "", ""],
        ["stnName", "TEXT", "", "", "", "", "", "", ""],
        ["stnType", "TEXT", "", "", "", "", "", "", ""],
        ["stnElev", "SHORT", "", "", "", "", "", "", ""],
        ["MLAQI", "SHORT", "", "", "", "", "", "", ""]
    ]

# Sensor Location data
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

# # ------------------Processing------------------
arcpy.AddMessage("""
**************************************************
*****   Started Integrating Location data    *****
**************************************************
""")

# Create empty point Featureclass
create_fc_from_list(gdbLocation, out_name, geometry_type, has_m, has_z, sr)
empData = out_name

# adding required fields
for f_data in feilds_to_add_flist:
    create_field_from_list(empData, f_data)

# Fetching Data from the madrid city council URL
source = "http://www.mambiente.munimadrid.es/opendata/horario.txt"
# store the decoded data in a 2D list
raw_data = dataAggregator.prepare_raw_data(source)

pldata = dataAggregator.aggregator_stn_data(raw_data)
dWI = madpolindexcalculation.dataIndices(pldata)

# insert the data into the feature class
#  Adding points and updating the fields
fields = ["SHAPE@XY", "stnID", "stnName", "stnType", "stnElev", "MLAQI"]
data_to_insert = formatted_stn_data_with_mlaqi(stnLoc, dWI)
with arcpy.da.InsertCursor(empData, fields) as updLyr:
        for row in data_to_insert:
            updLyr.insertRow(row)

arcpy.AddMessage("""
**************************************************
*****   Finished Integrating Location data   *****
**************************************************
""" )
