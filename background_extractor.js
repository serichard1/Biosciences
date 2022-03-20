//////////////////////////////////////// PARAMETERS ////////////////////////////////////////
const SIZE = 900;
const TYPE = "histogram" // "stretch" / "patchwork" / "histogram"
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

function random_value(table, total){
    let random = Math.floor(Math.random() * total);
    for (let i = 0; i < table.length; i++) {
        random -= table[i];
        if (random < 0) {
            return i;
        }
    }
}

function histogramBG(imp,size){
    //Extract the histogram of imp
    let histogram = new HistogramPlot();
    histogram.draw("hist",imp,256)
    let table = histogram.getHistogram();
    let total = imp.getWidth() * imp.getHeight()

    //Uses that histogram to generate a random image
    let ip = new ByteProcessor(size,size);
    for (let i = 0 ; i < size*size ; i++){
        let pix = random_value(table,total) ;
        ip.set(i,pix);
    }
    
    return new ImagePlus("background", ip);
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

