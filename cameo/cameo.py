import cv2
import os
from managers import WindowManger, CaptureManager

class Cameo(object):

    def __init__(self):
        self._windowManger = WindowManger("Cameo", self.onKeypress)
        self._captureManager = CaptureManager(cv2.VideoCapture(0), self._windowManger, True)

    def run(self):
      self._windowManger.createWindow()
      while self._windowManger._isWindowCreated:
          self._captureManager.enterFrame()
          frame = self._captureManager.frame

          if frame is not None:
              pass

          self._captureManager.exitFrame()
          self._windowManger.processEvent()

    def onKeypress(self, keycode):
        file_path = os.path.abspath(os.path.dirname(__file__))
        if keycode == 32: # space take screenshot

            self._captureManager.writeImage(os.path.join(file_path, 'screenshot.png'))
        if keycode == 9: # capture video on tab click
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo(os.path.join(file_path,'screencast.avi'))
            else:
                self._captureManager.stopWritingVideo()

        elif keycode == 27:
            self._windowManger.destroyWindow()


if __name__=="__main__":
    Cameo().run()