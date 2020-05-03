import cv2
import numpy as np


class Draw:
    @classmethod
    def rectangle(cls, image, p1, p2=None, dims=None, color=(0,255,0), thickness=0):
        image_ = image.copy()

        if p2 is None and dims is None:
            raise ValueError('missing second point or dimensions')
        elif p2 is None:
            x,y = p1
            w,h = dims
            p2 = (x+w, y+h)

        image_ = cv2.rectangle(image_, p1, p2, color, thickness)

        return image_

    @classmethod
    def text(cls, image, text, alignment, size=1, color=(255,255,255), bgcolor=(0,0,0), thickness=1):
        image_ = image.copy()

        font = cv2.FONT_HERSHEY_SIMPLEX
        image_h, image_w = image_.shape[:2]
        text_w, text_h = cv2.getTextSize(text, font, size, thickness)[0]

        x1 = text_h
        y1 = text_h * 2
        x2 = int(image_w/2 - text_w/2)
        y2 = int(image_h/2 + text_h/2)
        x3 = image_w - text_w - text_h
        y3 = image_h - text_h

        locations = {
            'top-left': (x1, y1), 'top-center': (x2, y1), 'top-right':  (x3, y1),
            'mid-left': (x1, y2), 'mid-center': (x2, y2), 'mid-right':  (x3, y2),
            'bot-left': (x1, y3), 'bot-center': (x2, y3), 'bot-right':  (x3, y3)
        }

        x,y = locations[alignment]
        if bgcolor != -1:
            image_ = cls.rectangle(image_, p1=(x-2,y-text_h-2), p2=None, dims=(text_w+5,text_h+5), color=bgcolor, thickness=-1)
        image_ = cv2.putText(image_, text, (x,y), font, size, color, thickness)

        return image_

    @classmethod
    def lines(cls, image, points, color=(0,255,0), thickness=5, fade=False):
        image_ = image.copy()

        for i in range(1,len(points)):
            if fade:
                current_thickness = round(1 + (thickness*i/len(points)))
            else:
                current_thickness = thickness
            image_ = cv2.line(image_, points[i-1], points[i], color, current_thickness)

        return image_

    @classmethod
    def crosshair(cls, image, center, size, cross_size=10, corner_size=10, color=(0,255,0), thickness=1):
        image_ = image.copy()

        x, y = center
        size = size//2
        cross_size = cross_size//2

        lines = [
            # cross
            [
                (x,y-cross_size),
                (x,y+cross_size)
            ],
            [
                (x-cross_size,y),
                (x+cross_size,y)
            ],
            # corners
            [
                (x-size, y-size+corner_size),
                (x-size, y-size),
                (x-size+corner_size, y-size)
            ],
            [
                (x+size, y-size+corner_size),
                (x+size, y-size),
                (x+size-corner_size, y-size)
            ],
            [
                (x-size, y+size-corner_size),
                (x-size, y+size),
                (x-size+corner_size, y+size)
            ],
            [
                (x+size, y+size-corner_size),
                (x+size, y+size),
                (x+size-corner_size, y+size)
            ]
        ]

        for line in lines:
            image_ = cls.lines(image_, line, color=color, thickness=thickness, fade=False)
        
        return image_


class Processor:
    @staticmethod
    def scale(image, scale):
        w,h = int(image.shape[1]*scale), int(image.shape[0]*scale)
        image = cv2.resize(image, (w,h))
        
        return image

    @staticmethod
    def binarize(image, threshold=127, method=None):
        if len(image.shape)!=2:
            if image.shape[-1] != 1:
                raise ValueError('image must have 1 channel only')

        image_ = image.copy()

        # Set thresholding method
        if method is None:
            method = cv2.THRESH_BINARY+cv2.THRESH_OTSU
        
        # Process binarization
        img_blur = cv2.GaussianBlur(image_, (7,7), 0)
        _, img_thresh = cv2.threshold(img_blur, threshold, 255, method)
        
        return img_thresh

    @staticmethod
    def canny_edges(image, channel):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        b,g,r = cv2.split(hsv)
        channels = {'r':r, 'g':g, 'b':b}

        gray = cv2.bilateralFilter(channels[channel], 11, 17, 17)
        edged = cv2.Canny(gray, 30, 200)

        return edged

    @staticmethod
    def kmeans(image, k):
        k = (k if k>0 else 1)
        Z = np.float32(image.reshape((-1,3)))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, label, center = cv2.kmeans(Z, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        clusters = np.uint8(center)[label.flatten()]
        image = clusters.reshape((image.shape))

        return image

    @staticmethod
    def gray(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def hsv(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    @staticmethod
    def rotate(image, angle, center=None, scale=1):
        w,h = image.shape[1], image.shape[0]

        if center is None:
            center = (w//2, h//2)

        M = cv2.getRotationMatrix2D(center, angle, scale)
        image = cv2.warpAffine(image, M, (w,h))

        return image