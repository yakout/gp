import numpy as np
import constant
import cv2
from PIL import Image
from matplotlib import pyplot as plt
import collections


class LogoDetector(object):
    """docstring for LogoDetector."""
    captured_frames = []
    numOfZeroForCell = [] # should be initalized with zeroes and same dims for image
    zeroApperanceThreshold = 0
    shaded = []
    n = 0
    m = 0
    def __init__(self, captured_frames):
        super(LogoDetector, self).__init__()
        self.captured_frames = captured_frames
        if(len(captured_frames) > 0):
            self.n, self.m, _ = captured_frames[0].shape
            self.numOfZeroForCell = np.zeros((self.n, self.m))

        # print("hash")
        # newCaptured_frames = []
        # for img in self.captured_frames:
        #     newImg = np.zeros((self.n, self.m))
        #     for i in range(self.n):
        #         for j in range(self.m):
        #             newImg[i][j] = img[i][j][0] * constant.MAX_COLOR_VAL * constant.MAX_COLOR_VAL + img[i][j][1]*constant.MAX_COLOR_VAL + img[i][j][2]
        #     newCaptured_frames.append(newImg)
        # self.captured_frames = newCaptured_frames;
        # print("hash finished")

    def getZeroAreaXOR(self, i, selectedImages):
        if(i == len(self.captured_frames)):
            if(len(selectedImages)%2 == 1 or len(selectedImages) == 0):
                return

            print("xor")
            xorSum = np.zeros((self.n, self.m))  # initalize with same dimensions and zeros
            for img in selectedImages:
                xorSum = np.bitwise_xor(xorSum.astype(int), img.astype(int))

            print("find zeroes")
            self.zeroApperanceThreshold += constant.ZERO_APPERANCE_THRESHOLD
            # print(self.numOfZeroForCell.shape)
            # for i in range(self.n):
            #     for j in range(self.m):
            #         self.numOfZeroForCell[i][j] += np.array_equal(xorSum[i][j], np.zeros(3))

            self.numOfZeroForCell += xorSum == 0
            # ind = np.where(xorSum == 0)
            # print(ind[0].shape)
            print("return")
            return

        print(i)
        self.getZeroAreaXOR(i + 1, selectedImages)  # leave it

        selectedImages.append(self.captured_frames[i])
        self.getZeroAreaXOR(i + 1, selectedImages) # take it
        return


    def getZeroAreaSub(self):
        print("zero area sub")
        sum = np.zeros((self.n, self.m, 3))

        for i in range(1, len(self.captured_frames)):
            sum += 1.0*np.abs(self.captured_frames[i].astype(int)-self.captured_frames[i-1].astype(int))

        # print(sum)
        print("set shaded pixles")

        img = self.captured_frames[0]
        self.shaded = np.zeros((self.n, self.m))
        for i in range(self.n):
            for j in range(self.m):
                self.shaded[i][j] = np.all(sum[i][j] <= (constant.FRAME_SUBTRACTION_THRESHOLD))
                if self.shaded[i][j] == 0:
                    img[i][j] = [0, 0, 0]

        # cv2.imshow("a7a", img)
        #
        # plt.imshow(img, interpolation='nearest')
        # plt.show()
        #
        # img = Image.fromarray(img, 'RGB')
        # img.show()

        # print(self.shaded)
        print("return sub")
        return

    def getShadedArea(self, i, j):
        # xor
        # if(i < 0 or j < 0 or i >= self.n or j >= self.m or self.vis[i][j] or self.numOfZeroForCell[i][j] < self.zeroApperanceThreshold):
        #     return;

        # subtract
        queue = collections.deque()
        queue.append([i,j])
        while queue:
            i, j = queue.popleft()
            if(i < 0 or j < 0 or i >= self.n or j >= self.m or self.vis[i][j] == 1 or self.shaded[i][j] == 0):
                continue

            self.minI = np.minimum(self.minI, i)
            self.maxI = np.maximum(self.maxI, i)
            self.minJ = np.minimum(self.minJ, j)
            self.maxJ = np.maximum(self.maxJ, j)
            self.vis[i][j] = 1;
            queue.append([i+1, j])
            queue.append([i-1, j])
            queue.append([i, j+1])
            queue.append([i, j-1])



    def detectLogo(self):
        # self.getZeroAreaXOR(0, [])
        if(len(self.captured_frames) == 0):
            return -1, -1, -1, -1, []

        self.getZeroAreaSub()

        maxArea = -np.Inf
        x1 = y1 = x2 = y2 = -1
        self.vis = np.zeros((self.n, self.m))
        for i in range(self.n):
            for j in range(self.m):
                if(self.vis[i][j] == 0):
                    self.minI = constant.INF
                    self.maxI = -constant.INF
                    self.minJ = constant.INF
                    self.maxJ = -constant.INF
                    self.getShadedArea(i, j)
                    area = (self.maxI-self.minI+1)*(self.maxJ-self.minJ+1)
                    if(self.maxI >= 0 and self.maxJ >= 0 and area > maxArea):
                        x1 = self.minI
                        y1 = self.minJ
                        x2 = self.maxI
                        y2 = self.maxJ
                        maxArea = area
                        print("max area:", maxArea)
                        # print(x1, " ", y1, " ", x2, " ", y2)

        logo = np.zeros((self.n, self.m, 3)) # it can also be of size(x2-x1, y2-y1) but for simplicity

        for i in range(1, len(self.captured_frames)):
            diff = self.captured_frames[i] - self.captured_frames[i-1]
            nonZero = 0
            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    nonZero += not np.all(diff[x][y] == 0)

            if nonZero <= constant.LOGO_DIFF_THRESHOLD*maxArea:
                logo = self.captured_frames[i]
                break

        img = Image.fromarray(logo, 'RGB')
        img.show()

        # temp = logo
        # for x in range(x1, x2+1):
        #     for y in range(y1, y2+1):
        #         temp[x][y] = [0, 0, 0]
        #
        #
        # img = Image.fromarray(temp, 'RGB')
        # img.show()

        return x1, y1, x2, y2, logo # we need also a value for comparing
