import numpy as np
import math

def absolute_angle_between_points(p1, p2): #update

    d1 = p2[0] - p1[0]
    d2 = p2[1] - p1[1]
    if d1 == 0 or d2 == 0:
        deg = 0
    else:
        deg = abs(math.atan2(d2 , d1) / math.pi * 180)

    return deg

def mean_turning_angle(filename):
    datafile = filename
    data_array = np.load(datafile)
    duration= data_array[:,0]
    xy_pos = data_array[:, [1,2]]

    angle_sum=0
    for i in range(len(duration)):
        if i< len(duration)-1:
            angle_sum+= absolute_angle_between_points(xy_pos[i], xy_pos[i+1])


    angle_mean = angle_sum/ len(duration)

    print( filename+ "mean turning angle is", angle_mean )

    return angle_mean


