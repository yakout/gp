import numpy as np
import constant
import cython

class Scoreboard(object):
    """docstring for Scoreboard."""
    x1 = y1 = x2 = y2 = -1
    scoreboards = []
    def __init__(self, x1, y1, x2, y2, scoreboards):
        super(Scoreboard, self).__init__()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.scoreboards = scoreboards
        return

    def hasScoreboard(self, img):
        for scoreboard in self.scoreboards:
            diff = 0
            for i in range(self.x1, self.x2+1):
                for j in range(self.y1, self.y2+1):
                    # print(np.abs(img[i][j] - self.scoreboard[i][j]))
                    diff += max(np.abs(img[i][j] - scoreboard[i][j])) > constant.MAX_COLOR_DIFF
            if(diff <= constant.SCOREBOARD_DIFF_THRESHOLD*(self.x2-self.x1+1)*(self.y2-self.y1+1)):
                return True

        return False
