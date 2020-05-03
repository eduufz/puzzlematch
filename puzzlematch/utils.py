import numpy as np

def mask_bbox(img):
    try:
        rows = np.any(img, axis=1)
        cols = np.any(img, axis=0)
        ymin, ymax = np.where(rows)[0][[0, -1]]
        xmin, xmax = np.where(cols)[0][[0, -1]]

        w,h = xmax-xmin, ymax-ymin

        return xmin,ymin,w,h

    except:
        return None

def same_length_ids(n):
    nlen = len(str(n))
    ids = [('0'*nlen + str(i+1))[-nlen:] for i in range(n)]

    return ids

def compute_grid(loc, size, offset=(0,0)):
    grid = []
    x,y,w,h = loc
    cols,rows = size
    xoff,yoff = offset
    
    for row in range(rows):
        for col in range(cols):
            xx = x + w*col + xoff
            yy = y + h*row + yoff
            grid.append((xx,yy,w,h))
            
    return grid