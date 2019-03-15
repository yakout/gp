import numpy as np
import constant
import cython
from skimage.measure import compare_ssim as ssim
import cv2

class Scoreboard(object):
    """docstring for Scoreboard."""
    x1 = y1 = x2 = y2 = -1
    scoreboards = []
    edScoreboards = []
    def __init__(self, x1, y1, x2, y2, scoreboards):
        super(Scoreboard, self).__init__()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.scoreboards = scoreboards
        for img in scoreboards:
            self.edScoreboards.append(self.getEdgeDetection(img))
        return

    def getEdgeDetection(self, img):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (7,7), 0)
        canny = cv2.Canny(blurred_image, 10, 30) # low threshold
        return canny

    def hasScoreboard(self, img):
        edImg = self.getEdgeDetection(img)
        # print(edImg.shape)
        for i in range(len(self.scoreboards)):
            scoreboard = self.scoreboards[i]
            edScorboard = self.edScoreboards[i]
            diff = 0
            sim = ssim(scoreboard[self.x1:self.x2+1, self.y1:self.y2+1, :], img[self.x1:self.x2+1, self.y1:self.y2+1, :], multichannel=True)
            edSim = ssim(edScorboard[self.x1:self.x2+1, self.y1:self.y2+1], edImg[self.x1:self.x2+1, self.y1:self.y2+1], multichannel=True)
            if (1 - min(sim, edSim) < constant.SCOREBOARD_DIFF_THRESHOLD):
                return True
            # for i in range(self.x1, self.x2+1):
            #     for j in range(self.y1, self.y2+1):
            #         # print(np.abs(img[i][j] - self.scoreboard[i][j]))
            #         diff += max(np.abs(img[i][j] - scoreboard[i][j])) > constant.MAX_COLOR_DIFF
            # if(diff <= constant.SCOREBOARD_DIFF_THRESHOLD*(self.x2-self.x1+1)*(self.y2-self.y1+1)):
            #     return True

        return False
