'''
import matplotlib.pyplot as plt
import numpy as np
import mplcursors

data = np.outer(range(10), range(1, 5))

fig, ax = plt.subplots()
lines = ax.plot(data)
ax.set_title("Click somewhere on a line.\nRight-click to deselect.\n"
             "Annotations can be dragged.")

x= mplcursors.cursor(lines) # or just mplcursors.cursor()

y = mplcursors.compute_pick(x)
print(y)
plt.show()
'''
'''
from matplotlib import pyplot as plt
import mplcursors
from pandas import DataFrame


df = DataFrame(
    [("Alice", 163, 54),
     ("Bob", 174, 67),
     ("Charlie", 177, 73),
     ("Diane", 168, 57)],
    columns=["name", "height", "weight"])

df.plot.scatter("height", "weight")
mplcursors.cursor().connect(
    "add", lambda sel: sel.annotation.set_text(df["name"][sel.target.index]))
plt.show()
'''
'''
import matplotlib.pyplot as plt
import numpy as np
import mplcursors

data = np.arange(100).reshape((10, 10))
save = []
fig, axes = plt.subplots(ncols=2)
axes[0].imshow(data, interpolation="nearest", origin="lower")
axes[1].imshow(data, interpolation="nearest", origin="upper",
                     extent=[200, 300, 400, 500])
mplcursors.cursor(High)

fig.suptitle("Click anywhere on the image")

plt.show()
'''
import cv2
from Functions.dataGrabber import grabData, tif2png
from PIL import Image
import numpy as np
class regionSelector(object):
    def __init__(self, data, regions = None, extractnumber = 3):
        self.data = Image.fromarray(data)
        self.data.save('test.png')
        self.regions = regions
        self.valuestore = []
        if self.regions == None: 
            self.regions = {'electrode': None, 'background': None, 'cells': None}
        else: 
            pass 
        self.kill_val = 0
        self.regionCount = 0
        self.totalcount = extractnumber
        
    def regionSelector(self):
        
        def Value_Selector(event, x, y, flags, param):
            
            #kill_val = len(regions)
            colorsBGR = image[y, x]
            if event == cv2.EVENT_MOUSEMOVE:
                colorsTIF=tuple(reversed(colorsBGR))
                #print("Pixel value at (x = {}, y = {}):{}".format(x,y,colorsTIF))
            elif event == cv2.EVENT_LBUTTONDOWN :  # checks mouse moves
                #colorsRGB=tuple(reversed(colorsBGR)) #Reversing the OpenCV BGR format to RGB format
                colorsTIF=tuple(reversed(colorsBGR))
                self.valuestore.append(colorsTIF)
                #print("TIF value at (x = {}, y= {}):{}".format(x,y,colorsTIF))
                self.regionCount = self.regionCount + 1
                print(self.regionCount)
                #print("RGB Value at ({},{}):{} ".format(x,y,colorsRGB))
            if self.regionCount == self.totalcount:
                #print("kill process")
                self.kill_val = 1
                
        
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10,500)
        fontScale              = 100
        fontColor              = (255,255,255)
        lineType               = 2

        # Read an image

        #Image.save(y, 'banter.jpg'
        #Image.fromarray(self.data)
        #image = cv2.imread('C:\\Users\\conor\\Pictures\\contrast_adjusted.png')
        
        image = cv2.cvtColor(np.load('test.npy'), cv2.COLOR_RGB2BGR)
        #image = cv2.imread(self.data)
        # Create a window and set Mousecallback to a function for that window
        cv2.namedWindow('Select 3 Values', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Select 3 Values', 600,600)
        cv2.setMouseCallback('Select 3 Values', Value_Selector)

        loopCount = 0
        #print(len(regions))
        # Do until esc pressed
        while (self.kill_val == 0):
            cv2.imshow('Select 3 Values', image)

            if cv2.waitKey(10) & 0xFF == 27:
                break
            if self.kill_val == True:
                print('dead')
                break
        
        # if esc is pressed, close all windows.
        cv2.destroyAllWindows()
        return self.valuestore
y = np.load('test.npy')
print(y)
x = regionSelector(y)
yes = x.regionSelector()
print(yes)