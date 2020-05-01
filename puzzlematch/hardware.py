from threading import Thread
from datetime import datetime

import cv2

from puzzlematch.processing import Draw


class Webcam:
    """OpenCV VideoCapture wrapper
    
    Attributes
    ----------
    source : int
        Device identification number

    stream : VideoCapture
        VideoCapture class for the selected device

    frame : numpy.ndarray
        Current frame
    
    _stopped : boolean
        Flag to control camera start and stop

    _start_timestamp : datetime.datetime
        Timestamp saved when the webcam starts

    _numFrames : int
        Total number of frames, increased every time a frame is obtained from the camera
    """

    def __init__(self, source=0):
        self.source = source
        self.stream = None
        self.frame = None

        self._stopped = True
        self._start_timestamp = None
        self._numFrames = 0

    def _update(self):
        """Reads and saves the frames from the device"""

        self._start_timestamp = datetime.now()
        self._stopped = False

        while not self._stopped:
            _, self.frame = self.stream.read()
            self._numFrames += 1
        
        self.stream.release()

    def open(self):
        """Opens the connection with the device"""

        self.stream = cv2.VideoCapture(self.source)
        
        if not self.isavailable():
            raise Exception('device not found')

        _, self.frame = self.stream.read()

        Thread(target=self._update, args=()).start()

    def read(self, hflip=False, vflip=False, scale=1.0, colorspace=None):
        """Returns the last frame extracted from the device

        Parameters
        ----------
        flip : boolean
            Apply horizontal flip on the image or not

        scale : float
            Factor by which the image is resized

        colorspace : int
            Colorspace to which the image is transformed
        """
        
        frame_ = self.frame.copy()

        if vflip:
            frame_ = cv2.flip(frame_,0)
        if hflip:
            frame_ = cv2.flip(frame_,1)
        if scale!=1.0:
            new_width,new_height = int(frame_.shape[0]*scale), int(frame_.shape[1]*scale)
            frame_ = cv2.resize(frame_, (new_height,new_width))
        if colorspace is not None:
            frame_ = cv2.cvtColor(frame_, colorspace)
        
        return frame_

    def close(self):
        """Stop recording"""

        self._stopped = True
    
    def isavailable(self):
        """States wether the camera is available"""

        return (self.stream is not None and self.stream.isOpened())

    @property
    def dimensions(self):
        w = self.frame.shape[1]
        h = self.frame.shape[0]

        return (w,h)

    @property
    def frame_count(self):
        return self._numFrames

    @property
    def fps(self):
        _end_timestamp = datetime.now()
        fps = 0
        
        try: fps = self._numFrames / (_end_timestamp - self._start_timestamp).total_seconds()
        except: pass
            
        return fps