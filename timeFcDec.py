# -*- coding: utf-8 -*-

# The time Handler Module 

# checking to provide index positions of values at the current time(tm)


def currHour(tm):
    # conditions for 24 hours time variation
    if tm >= 0 and tm <= 24:
        if tm >= 0.34 and tm < 1.34:
            # dVI data value index, vTI index of the data validity test
            dVI, vTI = 55, 56
        elif tm >= 1.34 and tm < 2.34:
            dVI, vTI = 9, 10
        elif tm >= 2.34 and tm < 3.34:
            dVI, vTI = 11, 12
        elif tm >= 3.34 and tm < 4.34:
            dVI, vTI = 13, 14
        elif tm >= 4.34 and tm < 5.34:
            dVI, vTI = 15, 16
        elif tm >= 5.34 and tm < 6.34:
            dVI, vTI = 17, 18
        elif tm >= 6.34 and tm < 7.34:
            dVI, vTI = 19, 20
        elif tm >= 7.34 and tm < 8.34:
            dVI, vTI = 21, 22
        elif tm >= 8.34 and tm < 9.34:
            dVI, vTI = 23, 24
        elif tm >= 9.34 and tm < 10.34:
            dVI, vTI = 25, 26
        elif tm >= 10.34 and tm < 11.34:
            dVI, vTI = 27, 28
        elif tm >= 11.34 and tm < 12.34:
            dVI, vTI = 29, 30
        elif tm >= 12.34 and tm < 13.34:
            dVI, vTI = 31, 32
        elif tm >= 13.34 and tm < 14.34:
            dVI, vTI = 33, 34
        elif tm >= 14.34 and tm < 15.34:
            dVI, vTI = 35, 36
        elif tm >= 15.34 and tm < 16.34:
            dVI, vTI = 37, 38
        elif tm >= 16.34 and tm < 17.34:
            dVI, vTI = 39, 40
        elif tm >= 17.34 and tm < 18.34:
            dVI, vTI = 41, 42
        elif tm >= 18.34 and tm < 19.34:
            dVI, vTI = 43, 44
        elif tm >= 19.34 and tm < 20.34:
            dVI, vTI = 45, 46
        elif tm >= 20.34 and tm < 21.34:
            dVI, vTI = 47, 48
        elif tm >= 21.34 and tm < 22.34:
            dVI, vTI = 49, 50
        elif tm >= 22.34 and tm < 23.34:
            dVI, vTI = 51, 52
        else:
            dVI, vTI = 53, 54
        tIndixValues = [dVI, vTI]
    return tIndixValues
