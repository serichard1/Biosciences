/*
Script ImageJ _ mitochondria segmentation
24/02
*/


'use strict';


/////// MACRO VOLÉE sur un forum

// imagej-macro "mitochondria" (Herbie G., 03. Nov. 2018)
// this macro works with plain ImageJ and BioFormats-plugin installed
requires( "1.52h" );
filePath = File.openDialog("");
setOption("BlackBackground", true);
run("Bio-Formats Importer", "open=["+filePath+"] color_mode=Default view=Hyperstack stack_order=XYCZT");
run("Z Project...", "projection=[Sum Slices]"); // CETTE LIGNE IL FAUT L'ENLEVER POUR NOTRE PROJET CAR ELLE FAIT LA SOMME DE TOUS LES STACKS EN UNE SEULE
run("Bandpass Filter...", "filter_large=10 filter_small=1 suppress=None tolerance=5");
setAutoThreshold("Otsu dark no-reset");
run("Convert to Mask");
run("Watershed"); // this operation is optional
exit();
// imagej-macro "maximum" (Herbie G., 03. Nov. 2018)

//////////////////////////////////////
// https://we.tl/t-1W9rnCNTsi
