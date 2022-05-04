import numpy as np
from cv2 import imwrite
from skimage import io
from sklearn.feature_extraction import image
from os import listdir
import matplotlib.pyplot as plt

def extract_multiple(path, size, patch_count, verbose = False) :
    patches = np.ndarray((0,size,size))
    i = 0
    imax = len(listdir(path))
    for file in listdir(path) :
        new_patches = extract_singular(path+"/"+file, size, patch_count)
        patches = np.concatenate((patches, new_patches))
        i += 1
        if verbose and i%10 == 0 :
            
            print("%i/%i"%(i,imax))
    return patches

def extract_singular(path, size, patch_count) :
    img = io.imread(path)
    new_patches = image.extract_patches_2d(img, (size,size),max_patches=patch_count)
    return new_patches


def filter(patches,size,seuil, verbose = False) :
    boolarray = []
    for i in range(len(patches)) :
        if verbose and i%1000 == 0 :
            print("%i/%i"%(i,len(patches)))
        boolarray.append(np.mean(patches[i]) > seuil)
            
    return patches[boolarray]

def stats(patches) :
    print("Il y a %s patches" %(len(patches)))
    averages = np.mean(patches,axis=(1,2))
    histogramme, classes = np.histogram(averages, bins=128)

    plt.figure()
    plt.xlabel("mean pixel value of a patch")
    plt.ylabel("number of patch")
    plt.yscale('log')
    plt.plot(classes[0:-1], histogramme)
    plt.show()
    
def save(patches, path, name, verbose = False):
    for i in range(len(patches)):
        if verbose and i%1000 == 0 :
            print("%i/%i"%(i,len(patches)))
        patch = patches[i].astype('uint16')
        true_path = path+"/"+name+"_"+str(i)+".png"
        imwrite(true_path, patch)
