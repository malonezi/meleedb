from __future__ import division
import cv2
import numpy as np
from sys import argv

vid = cv2.VideoCapture(argv[1])

total_frames = vid.get(7)
avg = np.zeros([vid.get(4), vid.get(3), 3])

while vid.grab():
    flag, frame = vid.retrieve()
    cv2.accumulate(frame, avg)

    # every 30 seconds
    if vid.get(1) % (60 * 30) == 0:
        hsv = cv2.convertScaleAbs(avg / vid.get(1))
        
        # extract saturation channel
        hsv = cv2.cvtColor(hsv, cv2.COLOR_RGB2HSV)[:, :, 1]

        # threshold for greys
        retval, hsv = cv2.threshold(hsv, 100, 0xFF, cv2.THRESH_TOZERO)
        retval, hsv = cv2.threshold(hsv, 156, 0xFF, cv2.THRESH_BINARY_INV)

        cv2.imshow("b", hsv)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
