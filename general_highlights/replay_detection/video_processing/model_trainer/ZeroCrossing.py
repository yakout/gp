import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt

BETA = 3
THETAS = np.arange(0, 1, .05) # should be tunned :D

def getZeroCrossingTheta_pzc(d):
    if(len(d) == 0):
        return -1

    # print(len(THETAS))
    normalized_d = (d-np.mean(d))/np.std(d)
    # print(d, "\n")
    # print(normalized_d, "\n\n")
    # print("mean normalized d zerocrossing ", np.mean(normalized_d))

    c1 = plt.plot(normalized_d, color='g')

    c2 = 0
    # for theta in THETAS:
    #     c2 = plt.plot(np.mean(normalized_d)-theta, color='r', linestyle='dashed')
    #     plt.plot(np.mean(normalized_d)+theta, color='r', linestyle='dashed')
    #
    # # plt.legend([c1, c2], ['Diff', 'theta'])
    # plt.show()
    # plt.show()
    # print('zero crossing mean',np.mean(d))

    for i in range(len(THETAS)-1, -1, -1):
        if(getZeroCrossing_zc(normalized_d, THETAS[i]) > BETA):
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
