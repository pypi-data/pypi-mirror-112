#maths.py - image maths for electroplot datasets.

import numpy as np


# a generic dataset operation function. 
#it takes the target dataset, the operator and the operation as arguments
#the operator may be another image stack, one image frame, or an individual value.
#available operations include divide, multiply, subtract and addition.
# output = target - operation - operator
# i.e. division: operation = divide; target / operator

def datasetOperation(target, operator, operation):
    #select the appropriate type of operator 
    if type(operator) == int:                               
        operatortype = 'value'
    elif len(operator.shape) == 2: 
        operatortype = 'image'
    elif len(operator.shape) == 3: 
        operatortype = 'stack'
        if len(target.shape) == 2:
            raise Exception("Cannot perform operations on an image with a stack as the operator!")
        else:
            pass
    else:
        raise Exception("Unrecognised operator type!")      
    
    if operatortype == ['image', 'value']:
        operator = np.full_like(target, operator)           #creates a stack of same shape as target, containing the operator image/value
    elif operatortype == 'stack':
        operator = operator                                 #redudndant but shows operator unchanged
    else:
        pass
        
    output = np.zeros_like(target, dtype=float)
        

    targetframeiterator = 0                                     #for iteration through frames of target dataset        
    for frame in operator:                                       #iterates through every frame in operator dataset
        new_frame = np.zeros_like(frame, dtype = float)         #creates an empty frame for casting transformed rows to.
            #targetrowiterator = 0                                   #for iteration through rows of target dataset - redundant unless scanning rows or pixels
        targetframe = target[targetframeiterator]
            
        if operation == 'divide':                               
            new_frame = targetframe / frame
        elif operation == 'subtract': 
            new_frame = targetframe - frame 
        elif operation == 'add':
            new_frame = targetframe + frame
                
        elif operation == 'logdivide':          #               #broken 
            new_frame = targetframe / frame
            for row in new_frame: 
                for pixel in row: 
                    pixel = log(0-pixel)
        else: 
            return('unrecognised operation! ')
            #the below is a more precise scanning version of dataframe iteration, instead of doing frame by frame operations, this does it on an individual pixel basis
            #the loops iterate through each frame in the stack, then each row within the selected frame, then each pixel within the selected row.
            #it is inherently much slower.
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
        output[targetframeiterator] = new_frame                 #append the transformed frame to the output dataset
        targetframeiterator +=1                                 #select the next frame in the target dataset
    
        return output


