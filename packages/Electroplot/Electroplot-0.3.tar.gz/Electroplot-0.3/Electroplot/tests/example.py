#testing script

import Electroplot as ep
from tkinter.filedialog import askopenfilename, askdirectory
#from PIL import Image, ImageOps, ImageEnhance
import numpy as np
from wand.image import Image 
#Load 4 stacks as electrodes
from math import log

#Load a single image as a dataset 
TestTif = ep.Dataset('Test', imagetype='stack', path='C:\\Users\\conor\\Desktop\\TestStack\\BLA\\E00010\\1' )

# Import the image 
'''
with Image(filename ='D:\\E00075\\1\\cytecount_0001.tiff') as image: 
    # Clone the image in order to process 
    with image.clone() as auto_level: 
        # Invoke auto_level function 
        a = 0.25
        b = 0.45
        image.function('polynomial', [a, b])
        #auto_level.auto_level() 
        #auto_level.auto_level() 
        # Save the image 
        image.save(filename ='C:\\Users\\conor\\Desktop\\Autoed.png')

'''
#image = Image.open('D:\\E00075\\1\\cytecount_0001.tiff')
a = (1,2,3)
b = (3,4,3)
c = (5,6,5)

d = (a , b , c)
e = (b , b , b)
f = (a , a , c)
g = (c , a , b)
#print(type(a))
testarr1 = np.array([d, d]) ## works with ints as array members ## test arrays as members next
testarr2 = np.array([e, e])


target = TestTif.data
#need integration into the main body
'''
def datasetOperation(Dataset, operator, operation, operatortype = 'image'):
     
    #need to implement internal catches for operator type perhaps.
    if operatortype = 'image':
        operator = np.full_like(Dataset, divisionFrame)
    if operatortype = 'value':
        #add code to fill in the blanks
        pass
    elif operator.type = 'stack':
        pass
    else: 
        'unrecognised operator type found!'
    
    output = np.zeros_like(Dataset, dtype=float)
    '''
'''
    print('divisor')
    print(divisor)

    print('target')
    print(target)
    print('=======')
    '''
    '''
    targetframeiterator = 0                                     #for iteration through frames of target dataset        
    for frame in operator:                                       #iterates through every frame in operator dataset
        new_frame = np.zeros_like(frame, dtype = float)         #creates an empty frame for casting transformed rows to.
        #targetrowiterator = 0                                   #for iteration through rows of target dataset - redundant unless scanning rows or pixels
        targetframe = target[targetframeiterator]
        
        if operation == 'divide':                               #works
            new_frame = targetframe / frame
        elif operation == 'subtract': 
            new_frame = targetframe - frame 
        elif operation == 'add':
            new_frame = targetframe + frame
            
        elif operation == 'logdivide': 
            new_frame = targetframe / frame
            for row in new_frame: 
                for pixel in row: 
                    pixel = log(0-pixel)
        else: 
            return('unrecognised operation! ')
        
        '''
        for row in frame:                                       #iterates through every row in the selected operator dataset frame
            #new_row = np.zeros_like(row, dtype=float)           #creates an empty row for casting transformed pixels to.
            targetpixeliterator = 0                             #for iteration through pixels of target dataset
            
            targetrow = target[targetframeiterator][targetrowiterator]
            new_row = targetrow / row
            print (new_row)
        
            for divpixel in row:                                #iterates through each pixel in the row
                targetpixel = target[targetframeiterator][targetrowiterator][targetpixeliterator]       #the pixel of the input image
                result = targetpixel / divpixel                 #need to replace '/' with operation. for now just divides 
                print(result)
                new_row[targetpixeliterator] = result           #append the transformed pixel to the selected output row
                targetpixeliterator+=1                          #select the next pixel in current target row
            
            new_frame[targetrowiterator] = new_row              #append the entire transformed row to the selected output frame
            targetrowiterator += 1                              #select the next row in the current target frame
        '''
        output[targetframeiterator] = new_frame                #append the transformed frame to the output dataset
        targetframeiterator +=1                                 #select the next frame in the target dataset
    #print(divided)
    #print(divided.shape)
    #print(len(TestTif.data))
    
    return output

test = datasetDivision(TestTif.data, TestTif.data[10], operation='logdivide')
print(test)
    #print(len(divisor))
    #print(divisor.shape)
'''
for i in target:
    
    #print(iterator)
    #print(num)
    #print(i)
    counteriter +=1
    #print(divisor[div][1])
    #print(divisor[div])
    #divided= i / divisor[div][0]
        #print(divided)
    #iterator +=1#
    #print(counteriter)
    #print(iterator)
    
    iterator = 0           
    if iterator >= len(divisor[div]):
        iterator = 0
    else:
        iterator +=1
'''
'''
    #intshit
    dividedpixel = i / testarr2[div-1]
    divided[iterator] = dividedpixel
    iterator += 1
    '''
    
##above


#print(divided)

#print(TestTif.data[10])
#TestTif.divide(divisionFrame=10)
'''
print(TestTif.data[1])
output = np.zeros_like(TestTif.data[1])


divided = TestTif.divide(2)

print("Divided Data \n \n \n")

print(TestTif.data)
#for image in TestTif.data:
    
#    np.divide(np.array(image), np.array(TestTif.data[1]), out=output)
#    print(output)
#TestTif.visualise()
#print(TestTif.data)
#TestTif.save()
#TestTif.mask(threshold = 400, masktype='region')
#np.save('test.npy', TestTif.data[0])
#test = Image.fromarray(TestTif.data[0])
#test.show()
#test.save('test.Tif')
#TestTif.visualise()
#Apply a mask to the image
#TestTif.applyMask(1500, masktype='edges', show=True)
#TestTif.visualise()
#Create a figure out of electrodes 1, 2, 3 and 4
#Figure1 = ep.Figure('Figure1', Electrode1, Electrode2, Electrode3, Electrode4, duration=10 )

#Show positional layout of figures
#Figure1.showlayout()

#rearrange the positional layout of figures (2x2)
#Figure1.arrange(2,2)

#assign subfigure types for plotting: graph, movie or image based on their positional label. This step is essential to render a figure
#Figure1.assignSubfigures((0, 'movie'), (1, 'movie'), (2, 'movie', True), (3, 'movie'))

#render the animated figure
#Figure1.renderFigure(fps=30, preview=True)

#select figure at position 1
#subfigure2 = Figure1.subfigures[1]

'''