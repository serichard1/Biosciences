//////////////////////////////////////// PARAMETERS ////////////////////////////////////////
const SIZE = 900;
const TYPE = "patchwork" // "stretch" / "patchwork" / "histogram"
//////////////////////////////////////// IMPORTS ////////////////////////////////////////
const IJ_PLUGINS = IJ.getDir('plugins');
load(`${IJ_PLUGINS}/javascript/nashorn_polyfill.js`);
load(`${IJ_PLUGINS}/javascript/utils-ij.js`);
//////////////////////////////////////// FUNCTIONS ////////////////////////////////////////

function correctROI(imp){
    let roi = imp.getRoi();
    let x = roi.getXBase();
    let y = roi.getYBase();
    let h = roi.getFloatHeight();
    let w = roi.getFloatWidth();
    if (h > w){h = w}
    if (w > h){w = h}
    imp.setRoi(x,y,w,h);
}

function stretchBG(imp,size){
    let out = imp.resize(size,size, "bilinear");
    return out;
}

function patchworkBG(imp,size){
    let w = imp.getWidth();
    let h = imp.getHeight();
    let w_copies = Math.ceil(size/w);
    let h_copies = Math.ceil(size/h);
    
    let stack = new ImageStack();
    for(let i=0 ; i<w_copies*h_copies ; i++){
        stack.addSlice(imp.getProcessor());
    }
    
    let ip = new ImagePlus();
    ip.setStack(stack)
    IJ.run(ip, "Make Montage...", "columns=" + w_copies +" rows=" + h_copies + " scale=1");
    let montage = IJ.getImage();
    IJ.run(montage, "Canvas Size...", "width=" + size + " height=" + size + " position=Center");

    return montage;
}

function histogramBG(imp,size){
    //Extract the histogram of imp
    //Uses that histogram to generate a random image
}

//////////////////////////////////////// MAIN ////////////////////////////////////////
ImageConverter.setDoScaling(true); 
let imp = IJ.getImage();
IJ.run(imp, "8-bit", "");

if(TYPE == "stretch"){ correctROI(imp)}
let crop = imp.crop();

let background;
switch(TYPE){
    case "stretch" :
        background = stretchBG(crop,SIZE);
        break;
    case "patchwork" :
        background = patchworkBG(crop,SIZE);
        break;
    case "histogram" :
        background = histogramBG(crop,SIZE);
        break;
}
background.show();

