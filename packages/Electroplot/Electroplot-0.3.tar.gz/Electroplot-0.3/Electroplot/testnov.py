#testnov
import numpy as np
import Electroplot as ep
from PIL import Image
import concurrent.futures
import lmdb
import sys
import h5py
input_stack = ep.Dataset('electroplotdataset', imagetype = 'stack', path ='input/shock')

h5f = h5py.File(str(input_stack.name) + '.h5', 'w')
for i in range(0, len(input_stack.data)):
    print(i)
    
    #
    h5f.create_dataset('image' + str(i), data=input_stack.data[i])
h5f.close()

from multiprocessing import Pool, cpu_count

print(cpu_count())
def division(image, divisor):
    division = image / divisor
    return division

# = division(input_stack)
#print(input_stack.data[1])

x = input_stack.data[18]
y = input_stack.data[1]

A = np.divide(x, y)

B = Image.fromarray(A )
B.convert('RGB')
B.save('test1', ".PNG")
'''
def store_single_lmdb(image, image_id, label):
    """ Stores a single image to a LMDB.
        Parameters:
        ---------------
        image       image array, (32, 32, 3) to be stored
        image_id    integer unique ID for image
        label       image label
    """
    map_size = image.nbytes * 10
    lmdb_
    # Create a new LMDB environment
    env = lmdb.open(str(lmdb_dir / f"single_lmdb"), map_size=map_size)

    # Start a new write transaction
    with env.begin(write=True) as txn:
        # All key-value pairs need to be strings
        value = CIFAR_Image(image, label)
        key = f"{image_id:08}"
        txn.put(key.encode("ascii"), pickle.dumps(value))
    env.close()
''' 
#z = store_single_lmdb(input_stack.data[1], 0x0, 'test')
print(sys.getsizeof(input_stack))