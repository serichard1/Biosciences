"""
import torch.nn as nn
from sklearn.feature_extraction import image
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np


from skimage import io

"""


import torch as T
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image

from os import listdir
from os.path import isdir
import sys



import patch_processing as PP
from customNet import Net

def bayesian_inference(H, E) :

    # P(A|B) = (P(B|A)*P(A))/P(B)
    # P(A|B) Probabilité à posteriori que l'hypothèse A0 soit vraie (ce que l'on cherche à calculer)
    # P(B|A) Probabilité que l'hypothèse soit vraie, selon le résultat d'un évenement (paramètre E pour évenement)
    # P(A) = Probabilité à prioiri que l'hypothèse A0 est vraie (paramètre H pour hypothèse)
    # P(B) = Probabilité de l'évenement, indépendament de l'hypothèse
         # En supposant que les seuls hypothèse sont A0 et A1 :
         #P(B) = P(B|A0)*P(A0|B) + P(B|A1)
        
    # On ne fait pas très confiance à la preuve 
    confiance = 0.5
    E = E*confiance + (1-confiance)/2
    # biais
    E = E*0.975
    
    
    return (H * E) / (H * E + (1-H)*(1-E))

def predictPatches(path,img_name,size,number_patches,threshold):
    transform = transforms.Compose([transforms.ToTensor()])

    predicted_list = []
    
    patches = PP.extract_singular(path+"/"+img_name, size, number_patches)
    patches = PP.filter(patches, size, threshold)
    
    # pour chacun des patch
    for i in range(len(patches)):
        # on applique les mêmes transformations et conditions que pour les images du training
        patches[i] = patches[i].astype('uint16')
        
        patch = Image.fromarray(patches[i])
        patch = patch.convert(mode='RGB')

        image_tensor = transform(patch)
        image_tensor = image_tensor.unsqueeze_(0)
            
        # on donne le patch à notre trained model
        output = net(image_tensor)
            
        # on récupère la probabilité que le patch soit issu d'une image de mitochondrie segmentée, 
        #selon l'algorithme
        output = output[0].tolist()
        confidence = F.softmax(T.tensor([[output[0],output[1]]],dtype=T.float),dim=1).tolist()[0][0]
        predicted_list.append(confidence)
                    
    return predicted_list

def predictImage(path,img_name,size,number_patches,threshold) :
    print(img_name + " : ")
    predicted_list = predictPatches(path,img_name,size,number_patches,threshold)
    
    if len(predicted_list) == 0 :
        print("No prediction can be made")
        return -1,0,0


    healthy_patches = 0
    fragmented_patches = 0
    consensus_prediction = 0.5

    for prediction in predicted_list :
        consensus_prediction = bayesian_inference(consensus_prediction, prediction)
        if prediction < 0.5 :
            healthy_patches += 1
        else :
            fragmented_patches += 1

    if consensus_prediction < 0.5:
        print("HEALTHY (%s)"%(1-consensus_prediction))
    else :
        print("FRAGMENTED (%s)" %(consensus_prediction))
    return consensus_prediction, healthy_patches, fragmented_patches

def predictFolder(path,size,number_patches,threshold, verbose = False):
    csv = ""
    healthy = 0
    fragmented = 0
    errors = 0
    healthy_patches = 0
    fragmented_patches = 0
    bayesian_prediction = 0.5
    average_prediction = 0
    # pour chaque image du répertoire
    for img_name in listdir(path) :
        res = predictImage(path,img_name,size,number_patches,threshold)
        healthy_patches += res[1]
        fragmented_patches += res[2]
        
        if verbose :
            # création d'un histogramme
            x = np.array(["Healthy", "Fragmented"])
            if(res == -1) :
                y = np.array([0,0])
            else :
                y = np.array([1-res,res])
            fig, ax = plt.subplots()
            barp = plt.bar(x,y, color=['green', 'red'])
            plt.show()
            # on ouvre et affiche l'image
            im = Image.open(path+"/"+img_name)
            im = im.resize((488,360), Image.NEAREST)
            display(im)
        
        csv += img_name + ";" #Les noms des images contiennent des ",", ne pas en utiliser comme séparateur
        if res[0] == -1 :
            csv += "none;none"
            errors += 1
        else :
            average_prediction += res [0]
            bayesian_prediction = bayesian_inference(bayesian_prediction, res[0])  
            if res[0] < 0.5 :
                csv += str(res[0]) + ";healthy"
                healthy += 1
            else :
                csv += str(res[0]) + ";fragmented"
                fragmented += 1
        csv += ";"+ str(res[1])+ ";" + str(res[2])+ "\n" 
        print("============================================================")

    average_prediction /= healthy + fragmented
    

    healthy_patches_percent = (healthy_patches/ (healthy_patches + fragmented_patches)) * 100
    healthy_percent = (healthy / (healthy + fragmented)) * 100
    print("Il y a un total de %s patches sain (%i%%) et  %s patches fragmenté (%i%%)" %(healthy_patches, healthy_patches_percent, fragmented_patches,  100-healthy_patches_percent))
    print("Il y a un total de %s images saines (%i%%)  et %s images fragmentées  (%i%%) " %(healthy, healthy_percent, fragmented, 100-healthy_percent))
    if(errors >0) :
        print("%s images n'ont pas pu être traitées" %(errors))
    print()
    print("En moyenne, la probabilité que le tissu soit fragmenté est de %s" %(average_prediction ))
    print("Par inférence bayésienne, la probabilité que le tissu soit fragmenté est de %s" %(bayesian_prediction))
    print()
    print("Voulez vous sauvegarder les résultats ?")
    print("Si oui, tapez le nom du fichier, sans l'extension")
    choice = input ("Si non, appuyez sur la touche Entrée : ")
    
    if choice == "" :
        print("Les résultats n'ont pas été sauvegardés")
    if choice != "" : 
        head = "image;P(fragmented);Prediction;Healthy patches;Fraggit stmented patches \n"
        
        head += "inférence bayésienne;%s;" %(bayesian_prediction)
        if(bayesian_prediction > 0.5) :
            head += "fragmented;"
        else :
            head += "healthy;"
        head += str(healthy_patches) + ";" + str(fragmented_patches) + "\n"
        
        head += "moyenne;%s;" %(average_prediction)    
        if(average_prediction > 0.5) :
            head += "fragmented;"
        else :
            head += "healthy;"
        head += str(healthy_patches) + ";" + str(fragmented_patches) + "\n"
        
        csv = head + csv
        #print(csv)
        fic=open(choice + ".csv","w")
        fic.write(csv)
        fic.close()
        print(choice + ".csv à bien été sauvegardé dans " + path)
        



# load the trained model
net = T.load("trained_net_test")
net.to('cpu')
net.eval()

path = "./Data/Images-Cytation/Experiment2_210326/Bad/Prediction"
path = "./Data/Images-Cytation"

#path = "./Data/All_good"
size = 320
number_patches = 10
threshold = 3


while True :
    print("Veuillez entrer le nom du dossier de l'experience, ")
    folder = input("ou tapez 0 pour sortir du programme : ")
    if folder == "0" :
        sys.exit()
    if isdir(path + "/" + folder + "/Prediction") :
        predictFolder(path+"/"+folder + "/Prediction",size,number_patches,threshold)
    elif isdir(path + "/" + folder) :
        print("ATTENTION ! Il n'y a pas de sous-dossier \"Prediction\", les images n'ont probablement pas été binarisées")
        print("Pour binariser les images, veuillez utiliser MitoS_Main_GPU.sh (https://github.com/MitoSegNet/MitoS-segmentation-tool)")
        choice = input("Si le dossier contient toutefois des images binarisées par MitoS_Main_GPU.sh, tapez \"oui\" : ")
        if choice in ("oui", "Oui", "OUI") :
            predictFolder(path+"/"+folder,size,number_patches,threshold)
            
    else :
        print("Le dossier n'existe pas !")
        print("Les dossier disponibles dans "+ path + " sont : ")
        for d in listdir(path) :
            print(" -"+d)
    
    print()
    print("==================================================")