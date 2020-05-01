import cv2

from puzzlematch.processing import Processor

def display(image, scale=1.0, name='image', wait=0, destroy=27, callback=None):
    if scale!=1.0:
        image = Processor.scale(image, scale)

    if callback is not None:
        cv2.setMouseCallback(name, callback)

    cv2.imshow(name, image)
    key = cv2.waitKey(wait)

    if key==destroy:
        cv2.destroyWindow(name)

    return key