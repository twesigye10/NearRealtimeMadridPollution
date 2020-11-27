# -*- coding: utf-8 -*-
# The time Handler Module

from datetime import datetime
import pytz

# checking to provide index positions of values at the current time(tm)

def current_hour_data_indices(tm):
    # conditions for 24 hours time variation
    # d_v_i == data value index, v_t_i == index of the data validity test(V or N)
    if tm >= 0 and tm <= 24:
        if tm >= 0.34 and tm < 1.34:
            d_v_i, v_t_i = 55, 56
        elif tm >= 1.34 and tm < 2.34:
            d_v_i, v_t_i = 9, 10
        elif tm >= 2.34 and tm < 3.34:
            d_v_i, v_t_i = 11, 12
        elif tm >= 3.34 and tm < 4.34:
            d_v_i, v_t_i = 13, 14
        elif tm >= 4.34 and tm < 5.34:
            d_v_i, v_t_i = 15, 16
        elif tm >= 5.34 and tm < 6.34:
            d_v_i, v_t_i = 17, 18
        elif tm >= 6.34 and tm < 7.34:
            d_v_i, v_t_i = 19, 20
        elif tm >= 7.34 and tm < 8.34:
            d_v_i, v_t_i = 21, 22
        elif tm >= 8.34 and tm < 9.34:
            d_v_i, v_t_i = 23, 24
        elif tm >= 9.34 and tm < 10.34:
            d_v_i, v_t_i = 25, 26
        elif tm >= 10.34 and tm < 11.34:
            d_v_i, v_t_i = 27, 28
        elif tm >= 11.34 and tm < 12.34:
            d_v_i, v_t_i = 29, 30
        elif tm >= 12.34 and tm < 13.34:
            d_v_i, v_t_i = 31, 32
        elif tm >= 13.34 and tm < 14.34:
            d_v_i, v_t_i = 33, 34
        elif tm >= 14.34 and tm < 15.34:
            d_v_i, v_t_i = 35, 36
        elif tm >= 15.34 and tm < 16.34:
            d_v_i, v_t_i = 37, 38
        elif tm >= 16.34 and tm < 17.34:
            d_v_i, v_t_i = 39, 40
        elif tm >= 17.34 and tm < 18.34:
            d_v_i, v_t_i = 41, 42
        elif tm >= 18.34 and tm < 19.34:
            d_v_i, v_t_i = 43, 44
        elif tm >= 19.34 and tm < 20.34:
            d_v_i, v_t_i = 45, 46
        elif tm >= 20.34 and tm < 21.34:
            d_v_i, v_t_i = 47, 48
        elif tm >= 21.34 and tm < 22.34:
            d_v_i, v_t_i = 49, 50
        elif tm >= 22.34 and tm < 23.34:
            d_v_i, v_t_i = 51, 52
        else:
            d_v_i, v_t_i = 53, 54

    return [d_v_i, v_t_i]


def current_time():
    # using the Madrid local time
    time_zone = pytz.timezone('Europe/Madrid')
    madrid_time_now = datetime.now(time_zone)
    # print("Madrid local time : {0}".format(madrid_time_now))
    # print("Hour : {0}, Minutes : {1}, Seconds : {2}".format(madrid_time_now.strftime('%H') ,madrid_time_now.strftime('%M') ,madrid_time_now.strftime('%S')))
    dec_time = (int(madrid_time_now.strftime('%H')) + (int(madrid_time_now.strftime('%M'))/60))

    return dec_time


if __name__ == '__main__':
    data_and_validity_indices = current_hour_data_indices(current_time())
    print ("Data index : {0}, Validity index : {1}".format(data_and_validity_indices[0], data_and_validity_indices[1]))
