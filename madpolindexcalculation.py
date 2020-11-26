# Sub indices and final MLAQI calculation Module

# Ilo - Index lower limit
# Iup - Index upper limit
# Plo - pollutant lower limit
# Pup - pollutant upper limit
# Px -  pollutant value whose index we want
# Pco - pollutant code

# indexLimits = [0, 50, 51, 100, 101, 150, >150]


def mlaqi_sub_index(Ilo, Iup,Px,Plo,Pup):
    sub_index = ((Px - Plo)/(Pup - Plo))*(Iup - Ilo) + Ilo
    return sub_index


# function for determining nitrogen params for index
def nitLim(Px):
    # nitrogenLimitValues = [0, 100, 101, 200, 201, 300]
    # conditions for Pco 08(Nitrogen dioxide)
    if Px >= 0 and Px <= 100:
        Ilo, Iup, Plo, Pup = 0, 50, 0, 100
    elif Px > 100 and Px <= 200:
        Ilo, Iup, Plo, Pup = 51, 100, 101, 200
    elif Px > 200 and Px <= 300:
        Ilo, Iup, Plo, Pup = 101, 150, 201, 300
    else:
        # arbitrary addition of 100 to the pollutant reading to allow index calc
        # arbitrary Iup of 200 for index calc
        Ilo, Iup, Plo, Pup = 151, 200, 301, Px+100
    return [Ilo, Iup, Px, Plo, Pup]


# function for determining ozone params for index
def ozoLim(Px):
    # ozoneLimitValues = [0, 90, 91, 180, 181, 240]
    # conditions for Pco 14(Ozone)
    if Px >= 0 and Px <= 90:
        Ilo, Iup, Plo, Pup = 0, 50, 0, 90
    elif Px > 90 and Px <= 180:
        Ilo, Iup, Plo, Pup = 51, 100, 91, 180
    elif Px > 180 and Px <= 240:
        Ilo, Iup, Plo, Pup = 101, 150, 181, 240
    else:
        # arbitrary addition of 100 to the pollutant reading to allow index calc
        # arbitrary Iup of 200 for index calc
        Ilo, Iup, Plo, Pup = 151, 200, 241, Px+100
    return [Ilo, Iup, Px, Plo, Pup]


# function for determining pm10 params for index
def ptnLim(Px):
    # pm10 = [0, 50, 51, 90, 91, 150]
    # conditions for Pco 10(PM10)
    if Px >= 0 and Px <= 50:
        Ilo, Iup, Plo, Pup = 0, 50, 0, 50
    elif Px > 50 and Px <= 90:
        Ilo, Iup, Plo, Pup = 51, 100, 51, 90
    elif Px > 90 and Px <= 150:
        Ilo, Iup, Plo, Pup = 101, 150, 91, 150
    else:
        # arbitrary addition of 100 to the pollutant reading to allow index calc
        # arbitrary Iup of 200 for index calc
        Ilo, Iup, Plo, Pup = 151, 200, 151, Px+100
    return [Ilo, Iup, Px, Plo, Pup]


# function for determining pm2.5 params for index
def ptfLim(Px):
    # pm2.5LimitValues = [0, 30, 31, 55, 56, 90]
    # conditions for Pco 09(PM2.5)
    if Px >= 0 and Px <= 30:
        Ilo, Iup, Plo, Pup = 0, 50, 0, 30
    elif Px > 30 and Px <= 55:
        Ilo, Iup, Plo, Pup = 51, 100, 31, 55
    elif Px > 55 and Px <= 90:
        Ilo, Iup, Plo, Pup = 101, 150, 56, 90
    else:
        # arbitrary addition of 100 to the pollutant reading to allow index calc
        # arbitrary Iup of 200 for index calc
        Ilo, Iup, Plo, Pup = 151, 200, 91, Px+100
    return [Ilo, Iup, Px, Plo, Pup]


def dataIndices(a):
    finalDataList = []
    # a is the whole data list
    # navigate through the entire data
    wdl = len(a)  # the length of the whole data
    i = 0
    for i in range(wdl):
        stn_with_index = []
        b = a[i].split()  # b is a station data list
        # navigate through a station data
        sdl = len(b)  # the length of the station data
        if "08" in b and sdl > 3:  # condition for core pollutant
            if "14" in b or "10" in b:  # condition for auxilliary pollutants
                stn_with_index.append(b[0])
                mlaqi_sub_indices_list = []
                j = 1
                for j in range(sdl):
                    # nitrogen a core pollutant, is already in the condition
                    index__nitrogen__value = b.index("08") + 1
                    nitrogen_limits = nitLim(float(b[index__nitrogen__value]))
                    nitrogen_sub_index = mlaqi_sub_index(nitrogen_limits[0],nitrogen_limits[1],nitrogen_limits[2],nitrogen_limits[3],nitrogen_limits[4])
                    mlaqi_sub_indices_list.append(nitrogen_sub_index)
                    # test existance of ozone in the station list
                    if "14" in b:
                        index_ozone_value = b.index("14") + 1
                        ozone_limits = ozoLim(float(b[index_ozone_value]))
                        ozone_sub_index = mlaqi_sub_index(ozone_limits[0],ozone_limits[1],ozone_limits[2],ozone_limits[3],ozone_limits[4])
                        mlaqi_sub_indices_list.append(ozone_sub_index)
                    # test existance of pm10 in the station list
                    if "10" in b:
                        index_pm10_value = b.index("10") + 1
                        pm10_limits = ptnLim(float(b[index_pm10_value]))
                        pm10_sub_index = mlaqi_sub_index(pm10_limits[0],pm10_limits[1],pm10_limits[2],pm10_limits[3],pm10_limits[4])
                        mlaqi_sub_indices_list.append(pm10_sub_index)
                    # test existance of pm25 in the station list
                    if "09" in b:
                        index_pm25_value = b.index("09") + 1
                        pm25_limits = ptfLim(float(b[index_pm25_value]))
                        pm25_sub_index = mlaqi_sub_index(pm25_limits[0],pm25_limits[1],pm25_limits[2],pm25_limits[3],pm25_limits[4])
                        mlaqi_sub_indices_list.append(pm25_sub_index)
                    pass
                station_max_mlaqi_value = int(round(max(mlaqi_sub_indices_list)))
                stn_with_index.append(station_max_mlaqi_value)
                finalDataList += stn_with_index
        pass
    return finalDataList
    pass


if __name__ == '__main__':
    import dataAggregator  # calling the aggregation module
    source = "http://www.mambiente.munimadrid.es/opendata/horario.txt"
    raw_data = dataAggregator.prepare_raw_data(source)
    # print("Raw data : {0}".format(raw_data))
    aggregated_data = dataAggregator.aggregator_stn_data(raw_data)
    print("Agrregated station data : {0}".format(aggregated_data))

    mlaqi_index_data = dataIndices(aggregated_data)
    print("MLAQI index data : {0}".format(mlaqi_index_data))

