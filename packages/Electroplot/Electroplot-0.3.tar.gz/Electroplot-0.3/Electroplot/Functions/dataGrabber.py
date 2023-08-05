
from tifffile import TiffFile
try:
    import Image
except ImportError:
    from PIL import Image
from PIL import ImageEnhance
import numpy
import threading

#grabs an array of data from tif files, inluding raw pixel data, image j metadata, and full metadata.
def grabData (file):
    tifs = ('.tif', '.tiff', '.TIF', '.TIFF')
    rgbs = ('.png', '.jpeg', '.jpg')
    if file.endswith(tifs):                         
        with TiffFile(file) as tif:
            imagej_hyperstack = tif.asarray()
            imagej_metadata = tif.imagej_metadata
            #imagej_hyperstack.shape
        
            if tif.imagej_metadata is None:
                data = imagej_hyperstack
                info = {'Pixels': data, 'ImageJ' : None, 'Meta' : None } 
            else:     
                data = imagej_hyperstack
                meta_full = tif.imagej_metadata
                meta_IJ = tif.imagej_metadata['Info']
                info = {'Pixels': data, 'ImageJ' : meta_IJ, 'Meta' : meta_full } 
        return info
           
    elif file.endswith(rgbs):
        #insert code to load rgb images
        
        info = print('no images found in' + str(file))
        return info
    elif file.endswith('.nd'):
        info = print('no images found in' + str(file)) 
        pass
    else: 
        #ignores any other type
        pass
  
class loaderThread(threading.Thread):
    def __init__(self, threadID, name, counter, image): 
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name 
        self.counter = counter
    def run(self):
        print ("Initialising Loader Thread" + str(self.name))
        threadLock.acquire()
        grabData(image)
        threadlock.release()

#grabs just the tifdata, returns a numpy array containing pixel values for data.
def grabTifdata(file):
    with TiffFile(file) as tif:
        imagej_hyperstack = tif.asarray()
        imagej_hyperstack.shape

        #print(imagej_metadata)
        data = imagej_hyperstack
    return data

#takes a tif file, converts it to PNG     
def tif2png(inputdir, file, outputdir):
    path = inputdir + file
    im = Image.open(path)
    if im.mode == 'I;16B':                      #The if condition catches big-endian .TIF images from the microscope and converts into an image. 
        #im.convert("RGB")
        stack = grabData(path)['Pixels']
        im = Image.fromarray(stack)
    elif im.mode != "RGB":                      #Catches all other types, converts mode to RGB so it can be converted to png. This does not work for the I;16B type (above)
        im = im.convert("RGB")
    else:
        print("Unknown image type found!")
    pix = im.load()
    image = im.save(outputdir + file + '.png', format = 'PNG')  #saves image as png
    return image, pix                           # returns the saved image and a loaded pillow object for the image. 


def clearup(tempdir):
    #insert code to clean up temporary stack folders for figure processing
    return None
    

def grabMetadata(file):                         # grabs just the metadata for the image
    with TiffFile(file) as tif:
        imagej_hyperstack = tif.asarray()
        imagej_metadata = tif.imagej_metadata
    info = tif.imagej_metadata
    return info

def grabImageJdata(file):                       #specifically returns imagej metadata.
    with TiffFile(file) as tif:
        imagej_hyperstack = tif.asarray()
        imagej_metadata = tif.imagej_metadata
    print(imagej_hyperstack)
    info = tif.imagej_metadata['Info']
    
    #for x in tif.imagej_metadata['Info']:
     #   print(x)
    return info
