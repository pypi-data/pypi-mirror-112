# masks.py -> write custom mask functions for the z-profile
import skimage
from skimage import io
from skimage import feature
from skimage.filters import sobel
from skimage.exposure import histogram
import numpy as np
# logarithm 
from scipy import ndimage as ndi
from skimage.segmentation import watershed
import matplotlib.pyplot as plt

def applyMask(image, threshold = 1500, masktype = 'edges', show = False):
    if masktype == 'edges': 
        image = image[0]
        edges = feature.canny(image/threshold)  
        print(edges)
        mask = ndi.binary_fill_holes(edges)
        print(mask)
        
        combined = mask * image
        print(combined)
        
        return mask
    elif masktype == 'region': 
        im = image[0]
        #hist, hist_centers = histogram(im)
        #print(hist)
        #plt.plot(hist)
        #plt.show()
        elevation_map = sobel(im)
        markers = np.zeros_like(im)
        markers[im < 100] = 1
        markers[im > 4000] = 2 
        segmentation = watershed(elevation_map)
        segmentation = ndi.binary_fill_holes(segmentation - 1)
        #io.imshow(segmentation)
        #io.show()
        return segmentation
    elif masktype == 'electrode':
        for i in image[0]:
            if i == 'test':
                print(str(masktype))

    elif masktype == 'hyperpolarised':
        print(str(masktype))

    elif masktype == 'depolarised':
        print(str(masktype))

    else:
        raise Exception("< 'masktype = " + str(masktype) + " > \n unknown mask type, choose from 'edges', 'electrode', 'hyperpolarise', 'depolarise' ")
    
    return combined

        
        
        
    