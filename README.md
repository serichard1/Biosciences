Our program is self-contained within a folder. To import any data in the system, one must place the
Experiment folder within the ./Data/Images-Cytation folder. To train the neutral network, each experiment
must have a ./Bad (for fragmented mitochondria) and a ./Good (for healthy mitochondria) subfolder. If you
simply want to predict the result of an experiment, you don’t need to create any subfolder.

Then, you must use the MitoS_Main_GPU.sh program on each folder that contains the pictures (Experiment/Good and Experiment/Bad for training, Experiment for predictions)
If you wish to train the neural network, you’ll have to run ./patchesExtraction.ipynb on each experiment folder.

Then, you may move any number of the patches it created in ./Data/patches_train to ./Data/patches_test
(we chose to move around 1 in 10). Finally, run the ./learning.ipynb program to output a trained network
(alternatively, you could contact one of the authors to have a copy of a pretrained model)

Finally, run the ./prediction.py program on any Experiment folder (or Experiment/Good or Experiment/Bad
if you want to verify the results of the training). This will output some keys metrics about the result of the
prediction, and you may save them is a csv file.

Note : MitoS_Main_GPU.sh and MitoSegNet_model.hdf5 are not on this github (and were not developed by us; see links), but must be downloaded from : https://github.com/MitoSegNet/MitoS-segmentation-tool
(In the section MitoS segmentation tool documentation , dowload the pretrained model at  https://zenodo.org/record/3539340#.Xd-oN9V7lPY ,
and the GUI tool for GPU at https://zenodo.org/record/3556431#.XeAHNtV7lPY (linux) or  https://zenodo.org/record/3549840#.Xd-ol9V7lPY (windows)
