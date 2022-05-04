import numpy as np
from cv2 import imwrite
from skimage import io
from sklearn.feature_extraction import image
from os import listdir
import matplotlib.pyplot as plt

def extract(path, size, patch_count) :
    """
    Extrait <patch_count> patches de dimension <size>*<size> de chaque image située dans le dossier à l'adresse <path>
    """
    patches = np.ndarray((0,size,size))
    for file in listdir(path) :
        new_patches = extract_singular(path+"/"+file, size, patch_count)
        patches = np.concatenate((patches, new_patches))
    return patches

def extract_singular(path, size, patch_count) :
    img = io.imread(path)
    new_patches = image.extract_patches_2d(img, (size,size),max_patches=patch_count)
    return new_patches


def filter(patches,size,seuil) :
    out = np.ndarray((0,size,size))
    for i in range(len(patches)) :
        if np.mean(patches[i]) > seuil :
            out = np.concatenate([out, [patches[i]]])
    return out

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
    

def save(patches, path, name):
    for i in range(len(patches)):
        patch = patches[i].astype('uint16')
        true_path = path+"/"+name+"_"+str(i)+".png"
        imwrite(true_path, patch)
