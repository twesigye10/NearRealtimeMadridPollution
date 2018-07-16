# import madpoldataaggreg  # calling the aggregation module
# pld = madpoldataaggreg.stnNos

# Ilo - Index lower limit, Iup - Index upper limit
# Plo - pollutant lower limit, Pup - pollutant upper limit
# Px -  pollutant value whose index we want, Pco - pollutant code

# indexLimits = [0, 50, 51, 100, 101, 150, >150]


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
    sx = ((Px - Plo)/(Pup - Plo))*(Iup - Ilo) + Ilo
    return sx


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
    sx = ((Px - Plo)/(Pup - Plo))*(Iup - Ilo) + Ilo
    return sx


# function for determining pm10 params for index
def ptnLim(Px):
    # pmtenLimitValues = [0, 50, 51, 90, 91, 150]
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
    sx = ((Px - Plo)/(Pup - Plo))*(Iup - Ilo) + Ilo
    return sx


# function for determining pm2.5 params for index
def ptfLim(Px):
    # ptwodotfiveLimitValues = [0, 30, 31, 55, 56, 90]
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
    sx = ((Px - Plo)/(Pup - Plo))*(Iup - Ilo) + Ilo
    return sx


def dataIndices(a):
    finalDataList = []
    # a is the whole data list
    # navigate through the entire data
    wdl = len(a)  # the length of the whole data
    i = 0
    for i in range(wdl):
        stnWithIndex = []
        b = a[i].split()  # b is a station data list
        # navigate through a station data
        sdl = len(b)  # the length of the station data
        if "08" in b and sdl > 3:  # condition for core pollutant
            if "14" in b or "10" in b:  # condition for auxilliary pollutants
                stnWithIndex.append(b[0])
                subIndicesList = []
                j = 1
                for j in range(sdl):
                    # nitrogen a core pollutant, is already in the condition
                    indexN = b.index("08")
                    indexNV = indexN+1
                    nitSubIndex = nitLim(float(b[indexNV]))
                    subIndicesList.append(nitSubIndex)
                    # test existance of ozone in the station list
                    if "14" in b:
                        indexO = b.index("14")
                        indexOV = indexO+1
                        ozoSubIndex = ozoLim(float(b[indexOV]))
                        subIndicesList.append(ozoSubIndex)
                    # test existance of pm10 in the station list
                    if "10" in b:
                        indexT = b.index("10")
                        indexTV = indexT+1
                        ptnSubIndex = ptnLim(float(b[indexTV]))
                        subIndicesList.append(ptnSubIndex)
                    # test existance of pm25 in the station list
                    if "09" in b:
                        indexF = b.index("09")
                        indexFV = indexF+1
                        ptfSubIndex = ptfLim(float(b[indexFV]))
                        subIndicesList.append(ptfSubIndex)
                    pass
                stnIndex = int(round(max(subIndicesList)))
                stnWithIndex.append(stnIndex)
                finalDataList += stnWithIndex
        pass
    return finalDataList
    pass


#  excecuting the function
# plExcect = dataIndices(pld)
# print(plExcect)
