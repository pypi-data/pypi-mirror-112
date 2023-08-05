#microscope emulator
import shutil
import os
from time import sleep

def microscope_emulation(source, target, interval):
    #path = os.path.(source)
    if os.path.exists(target) == False: 
        os.chdir('..')
        os.mkdir('output')
    else:
        shutil.rmtree(target)
        os.chdir('..')
        os.mkdir('output')
    #print(os.listdir(source))
    
    for image in os.listdir(source):
        shutil.copy(src = source + '/' + image, dst= target )
        print(image)
        sleep(interval)
    
microscope_emulation('../input/shock', '../output', interval = 1)