# Subfigure Editor - Functions to edit images/movies/graphs within the subfigure dataset. 
#from moviepy import moviepy.Editor as mp 
import numpy as np  
import matplotlib.pyplot as plt 
try:
    import Image
except ImportError:
    from PIL import Image

def change_contrast(img, level):
    alpha = img.split()[-1]
    img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
    
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)

def change_brightness(img, level):
    enhancer = ImageEnhance.Brightness(img)

    im_output = enhancer.enhance(level)
    return im_output