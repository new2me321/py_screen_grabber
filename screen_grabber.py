import numpy as np
import cv2
import time
import threading

from mss import mss


class ScreenGrab:

    def __init__(self, bounding_box):
        self.region = bounding_box
        self.frame = None
        self.running = True

    def get_frame(self):
        return self.frame

    def grab_screen(self):
        sct = mss()
        loop_time = time.time()
        while True:
            sct_img = sct.grab(self.region)
            self.frame = np.array(sct_img)

            cv2.putText(
                self.frame,
                'FPS: {:.2f}'.format(round(1 / (time.time() - loop_time), 2)),
                (800, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('screen', self.frame)
            loop_time = time.time()

            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                self.running = False
                cv2.destroyAllWindows()
                break

    def is_running(self):
        return self.running


if __name__ == '__main__':
    bounding_box = {'top': 154, 'left': 8, 'width': 1118, 'height': 851}
    screen = ScreenGrab(bounding_box)
    threading.Thread(target=screen.grab_screen).start()
    while screen.is_running():
        print(screen.get_frame())
