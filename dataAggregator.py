# -*- coding: utf-8 -*-
# The Data Aggregator module

import urllib.request
import timeHandler

def aggregator_stn_data(a):
    # storing all data into a single list to be returned
    store_poll_data = []
    # get data and validity indices
    dataIndexHolder = timeHandler.current_hour_data_indices(timeHandler.current_time())
    # print("The current indices : {0}".format(dataIndexHolder))
    # extracting lines(current hour data) from the text file
    for lineData in a:
        if lineData[dataIndexHolder[1]] == 'V':
            processPart = (lineData[0]+lineData[1]+lineData[2]+" "+lineData[3]+" " +
                                    lineData[4]+" "+lineData[5]+" " + lineData[6]+" " +
                                    lineData[7]+" "+lineData[8]+" "+lineData[dataIndexHolder[0]])
            store_poll_data.append(processPart)

    # testing the station and component pollutants
    stn_nos_ref = ['004', '008', '011', '016', '017', '018', '024', '027', '035',
                        '036', '038', '039', '040', '047', '048', '049', '050',
                        '054', '055', '056', '057', '058', '059', '060']
    considered_pollutants_codes = ['08', '09', '10', '14']
    # storing all component pollutant data into respective stations
    aggregate_stns_pollutant_data = ['004', '008', '011', '016', '017', '018', '024', '027', '035', '036',
                            '038', '039', '040', '047', '048', '049', '050', '054',
                            '055', '056', '057', '058', '059', '060']
    # the length of the entire list
    # print("The stored pollutant data : {0}".format(store_poll_data))
    dataLength = len(store_poll_data)
    i = 0
    for i in range(dataLength):
        m = store_poll_data[i].split()
        if m[0][-3:] in stn_nos_ref and m[1] in considered_pollutants_codes:
            r = stn_nos_ref.index(m[0][-3:])
            if r >= 0:
                aggregate_stns_pollutant_data[r] += (" "+m[1]+" "+m[7])
    return aggregate_stns_pollutant_data
    pass

def prepare_raw_data(data_source):
    #      Fetching Data from the madrid city council URL
    # source = "http://www.mambiente.munimadrid.es/opendata/horario.txt"
    with urllib.request.urlopen(data_source) as response:
        byte_data = response.read().decode('utf-8') # decode from byte format
    # store the decoded data in a 2D list
    raw_data =[]
    kmt = byte_data.split()
    for k in kmt:
        raw_data.append(k.split(","))

    return raw_data


if __name__ == '__main__':
    source = "http://www.mambiente.munimadrid.es/opendata/horario.txt"
    raw_data = prepare_raw_data(source)
    # print("Raw data : {0}".format(raw_data))
    print("Agrregated station data : {0}".format(aggregator_stn_data(raw_data)))
