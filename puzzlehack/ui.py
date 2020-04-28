import cv2

from puzzlehack.processing import Processor

class Window:
    @staticmethod
    def view(image, scale=1.0, name='image', wait=0, destroy=True):
        image = Processor.scale(image, scale)

        cv2.imshow(name,image)
        cv2.waitKey(wait)

        if destroy: cv2.destroyWindow(name)
    
    @staticmethod
    def view_many(imagelist, scale=1.0, name='image', wait=0, destroy=True):
        for i, image in enumerate(imagelist):
            image = Processor.scale(image, scale)
            windowname = '{}{}'.format(name,i)
            cv2.imshow(windowname,image)

        cv2.waitKey(wait)
        
        if destroy:
            for i, image in enumerate(imagelist):
                windowname = '{}{}'.format(name,i)
                cv2.destroyWindow(windowname)