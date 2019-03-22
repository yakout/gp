import numpy as np
from general_highlights.replay_detection import constant

ZC_WINDOW_SIZE = constant.WINDOW_SIZE
BETA = 1
THETAS = np.arange(.000001, .0001, .000001)

def getZeroCrossingTheta_pzc(t, d):
    if(t <= ZC_WINDOW_SIZE):
        return -1

    for i in range(len(THETAS)-1, -1, -1):
        if(getZeroCrossing_zc(t, d, THETAS[i]) > BETA):
            return i

    return -1


def getZeroCrossing_zc(t, d, theta):
    zc = 0

    mean = 0
    for i in range(t-ZC_WINDOW_SIZE+2, t):
        mean += d[i]

    mean /= ZC_WINDOW_SIZE

    for i in range(t-ZC_WINDOW_SIZE+2, t):
        zc += thrd(d[i-1]-mean, d[i]-mean, theta)

    return zc


def thrd(x, y, theta):
    return (x >= theta and y <= -theta) or (x <= -theta and y >= theta)
