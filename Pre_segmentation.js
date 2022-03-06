/*
Créé les segmentation mask
(A besoin du folder crazybio du Jen Christophe pour fonctionner)
*/
//////////////////////////////////////// PARAMETERS ////////////////////////////////////////
const radius = 15; // Min filter (à vérifier quelle valeur choisir)
const sigma = 5; // Gaussian blurr filter (à vérifier quelle valeur choisir)

const min_size = 3000;
//////////////////////////////////////// IMPORTS ////////////////////////////////////////
const IJ_PLUGINS = IJ.getDir('plugins');
load(`${IJ_PLUGINS}/crazybio/nashorn_polyfill.js`);
load(`${IJ_PLUGINS}/crazybio/utils-ij.js`);
//////////////////////////////////////// FUNCTIONS ////////////////////////////////////////

//////////////////////////////////////// MAIN ////////////////////////////////////////
// Duplicate
let imp = IJ.getImage();
let mask = imp.duplicate();

IJ.run(mask, "Invert", "");

// Blur
IJ.run(mask, "Minimum...", "radius="+radius.toString());
IJ.run(mask, "Gaussian Blur...", "sigma="+ sigma.toString());
//mask.show();
//aaaa
// Threshold
IJ.setAutoThreshold(mask, "Otsu");
IJ.run(mask, "Convert to Mask", "");
// Fill holes
IJ.run(mask, "Fill Holes", "");
// Delete Smaller particles
IJ.run(mask, "Analyze Particles...", "size=" + min_size.toString()+ "-Infinity show=Masks display clear");
mask = IJ.getImage();

//Display
IJ.run(mask, "16-bit", "");
IJ.run(mask, "Multiply...", "value=257");
mask.hide();
mask = ImageCalculator.run(imp, mask, "OR create");

const out = ImagesToStack.run([imp,mask]);
out.show();
mask.close();


