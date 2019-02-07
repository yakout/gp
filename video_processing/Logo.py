import numpy as np
import constant

class Logo(object):
    """docstring for Logo."""
    x1 = y1 = x2 = y2 = -1
    logo = []
    def __init__(self, x1, y1, x2, y2, logo):
        super(Logo, self).__init__()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.logo = logo
        return

    def hasLogo(self, img):
        diff = 0
        for i in range(self.x1, self.x2+1):
            for j in range(self.y1, self.y2+1):
                # print(np.abs(img[i][j] - self.logo[i][j]))
                diff += max(np.abs(img[i][j] - self.logo[i][j])) > constant.MAX_COLOR_DIFF
            # print()
        # print(diff, " ", constant.LOGO_DIFF_THRESHOLD*(self.x2-self.x1+1)*(self.y2-self.y1+1))
        return diff <= constant.LOGO_DIFF_THRESHOLD*(self.x2-self.x1+1)*(self.y2-self.y1+1)
