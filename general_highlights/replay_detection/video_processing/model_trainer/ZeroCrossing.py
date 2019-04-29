import numpy as np

BETA = 1
THETAS = np.arange(.000001, .0001, .000001) # should be tunned :D

def getZeroCrossingTheta_pzc(d):
    if(len(d) == 0):
        return -1

    for i in range(len(THETAS)-1, -1, -1):
        if(getZeroCrossing_zc(d, THETAS[i]) > BETA):
            return i

    return -1


def getZeroCrossing_zc(d, theta):
    zc = 0

    mean = 0
    for i in range(len(d)):
        mean += d[i]

    mean /= len(d)

    for i in range(1, len(d)):
        zc += thrd(d[i-1]-mean, d[i]-mean, theta)

    return zc


def thrd(x, y, theta):
    return (x >= theta and y <= -theta) or (x <= -theta and y >= theta)
