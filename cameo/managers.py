import cv2
import numpy
import time


class CaptureManager(object):
    def __init__(self, capture, previewWindowManager =None, shouldMirrorPreview = False):
        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview

        self._capture = capture
        self._channel = 0
        self._enteredFrame =0
        self._frame = None
        self._imageFileName = None
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None

        self._startTime = None
        self._framesElapsed = 0
        self._fpsEstimate = None

    @property
    def channel(self):
        return self._channel
    @channel.setter
    def channel(self,value):
        if self._channel != value:
            self._channel = value
            self._frame = None


    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve(
                self._frame, self._channel)
        return self._frame

    @property
    def isWritingImage(self):
        return self._imageFileName is not None
    @property
    def isWritingVideo(self):
        return self._videoFilename is not None

    def enterFrame(self):
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exitFrame(self):
        if self.frame is None:
            self._enteredFrame = False

        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime ## keep track of the time passed
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1

        if self.previewWindowManager is not None: ## make the frames mirrored if asked
            if self.shouldMirrorPreview:
                mirroreFrame = numpy.fliplr(self._frame)
                self.previewWindowManager.show(mirroreFrame)
            else:
                self.previewWindowManager.show(self._frame)

        if self.isWritingImage:
            cv2.imwrite(self._imageFileName, self._frame)
            self._imageFileName = None

        self._writeVideoFrame()

        self._frame = None
        self._enteredFrame = False

    def writeImage(self, filename):
        self._imageFileName = filename

    def startWritingVideo(self, filename, encoding = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')):
        self._videoFilename = filename
        self._videoEncoding = encoding

    def stopWritingVideo(self):
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None

    def _writeVideoFrame(self):
        if not self.isWritingVideo:
            return

        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps <= 0.0:
                if self._framesElapsed < 20:
                    return
                else:
                    fps = self._fpsEstimate
            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter = cv2.VideoWriter(self._videoFilename,self._videoEncoding, fps, size)
        self._videoWriter.write(self._frame)

class WindowManger(object):

    def __init__(self, windowName, keypressCallback = None):
        self._windowName = windowName
        self.keypressCallback = keypressCallback
        self._isWindowCreated = False

    @property
    def isWindowCreated(self):
            return self._isWindowCreated

    @isWindowCreated.setter
    def isWindowCreated(self,value):
        self._isWindowCreated = value
    def createWindow(self):
            cv2.namedWindow(self._windowName)
            self._isWindowCreated = True

    def show(self, frame):
            cv2.imshow(self._windowName, frame)

    def destroyWindow(self):
            cv2.destroyWindow(self._windowName)
            self.isWindowCreated = False

    def processEvent(self):
            keycode = cv2.waitKey(1)
            if self.keypressCallback is not None and keycode != -1:
                self.keypressCallback(keycode)

