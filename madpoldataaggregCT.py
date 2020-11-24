# -*- coding: utf-8 -*-
import time
import timeHandler


def aggrData(a):
    # storing all data into a single list to be returned
    storePollData = []
    # # using the local time
    # currTimeLocal = time.localtime()
    # decTime = (currTimeLocal[3] + (float(currTimeLocal[4])/60))
    dataIndexHolder = timeHandler.currHour(timeHandler.current_time())
    # extracting lines from the text file
    for lineData in a:
        if lineData[dataIndexHolder[1]] == 'V':
            processPart = (lineData[0]+lineData[1]+lineData[2]+" "+lineData[3]+" " +
                                    lineData[4]+" "+lineData[5]+" " + lineData[6]+" " +
                                    lineData[7]+" "+lineData[8]+" "+lineData[dataIndexHolder[0]])
            storePollData.append(processPart)

    # testing the station and component pollutants
    stnNosRef = ['004', '008', '011', '016', '017', '018', '024', '027', '035',
                        '036', '038', '039', '040', '047', '048', '049', '050',
                        '054', '055', '056', '057', '058', '059', '060']
    pollNos = ['08', '09', '10', '14']
    # storing all component pollutant data into respective stations
    stnNos = ['004', '008', '011', '016', '017', '018', '024', '027', '035', '036',
                            '038', '039', '040', '047', '048', '049', '050', '054',
                            '055', '056', '057', '058', '059', '060']
    # the length of the entire list
    dataLength = len(storePollData)
    i = 0
    for i in range(dataLength):
        m = storePollData[i].split()
        if m[0][-3:] in stnNosRef and m[1] in pollNos:
            r = stnNosRef.index(m[0][-3:])
            if r >= 0:
                stnNos[r] += (" "+m[1]+" "+m[7])
    return stnNos
    pass
