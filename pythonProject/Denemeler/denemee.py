import numpy as np
import math
import matplotlib.pyplot as plt
import os

def absolute_angle_between_points(p1, p2):
    d1 = p2[0] - p1[0]
    d2 = p2[1] - p1[1]
    if d1 == 0 or d2 == 0:
        deg = 0
    else:
        deg = abs(math.atan2(d2, d1) / math.pi * 180)

    return deg

y=absolute_angle_between_points((250,425),(255,430))

print(y)


