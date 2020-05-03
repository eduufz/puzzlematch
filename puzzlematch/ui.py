import cv2

from puzzlematch.processing import Processor

def display(images, scale=1.0, wait=0, destroy=27):
    if type(images) != list:
        images = [images]

    for i,image in enumerate(images):
        if scale!=1.0:
            image = Processor.scale(image, scale)

        cv2.imshow('window{}'.format(i), image)
    
    key = cv2.waitKey(wait)
    if key==destroy:
        cv2.destroyAllWindows()

    return key