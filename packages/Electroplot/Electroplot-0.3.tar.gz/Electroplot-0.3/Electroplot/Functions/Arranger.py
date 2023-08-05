import os
import moviepy.editor as mp
import matplotlib.pyplot as plt 
from Functions.dataGrabber import tif2png
from pathlib import Path

class subFigure(object):
    def __init__(self, epObjects, name, data, metadata, position = None, subtype = 'default' ):
        self.epObjects = epObjects
        self.name = name
        self.data = data
        self.metadata = metadata
        self.subtype = subtype
        self.animation = False
        self.clip = None
        self.treatment = None
        self.images = []
        self.temp_path = epObjects.path  + str(epObjects.name) + "_temp/"
        try:
            Path(self.temp_path).mkdir(parents = True, exist_ok = False)
            if epObjects.type == 'stack':
                print("Processing " + str(epObjects.name) + " dataset .TIFs into .png files... ")
                for file in os.listdir(epObjects.path):
                    if file.endswith('.tiff') or  file.endswith('.tif'):
                        self.images.append(tif2png(epObjects.path, file, self.temp_path)[1])    
                print('... Done!')   
            elif epObjects.type == 'image':
                if epObjects.path.endswith('.tif'):
                    self.images.append(tif2png(epObjects.path))
        
        except FileExistsError:
            print(self.images)
            for i in os.listdir(self.temp_path):
                print(i)
            print("Files found at " + str(self.temp_path))
            pass
              
    def makeSubfigure(self, fps , duration):
        if self.subtype == 'image':
            plot = plt.plot(self.images)
            if self.epObjects.type == 'stack':
                #print(self.images)
                image = os.listdir(self.images)[1]
                print(self.temp_path)
                print(image)
                print(self.temp_path + image)
                
                self.clip = mp.ImageClip(self.temp_path + image).set_duration(duration)
            elif self.epObjects.type == 'image':
                print('image success')
                self.clip = mp.ImageClip(self.images)
                
                self.clip = self.clip.set_duration(10)
                
        elif self.subtype == 'movie': #makes movie --working
            self.clip = mp.ImageSequenceClip(self.images, fps, load_images = True, with_mask = False)
            
        elif self.subtype == 'graph':
            if self.animation== True: 
                print("animation is a work in progress!")
            if self.animation == False:
                
            
                self.clip = mp.ImageClip('C:/Users/conor/Desktop/ElectroPlot/zprofile.png').set_duration(duration)
                #print(self.clip)
        else:
            raise Exception("no subtype is defined! Define subtypes as either 'image', 'movie' or 'graph' using <Figure>.defineSubs((position,subtype))")
    
    '''
    def transformSubfigure(self, transform, *args):
        if subfigure.subtype == 'image':
            self.
        elif subfigure.subtype == 'graph':
            
        elif subfigure.subtype == 'movie':
        
        else:
            raise Exception("Assign subfigure type prior to transformation!")

            '''

class objdict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
