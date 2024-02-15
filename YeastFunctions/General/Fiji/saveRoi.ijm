roiManager("Select All");

// Get the directory path
var directory = getDirectory("Select directory to save...");


var path = directory + "RoiSet.zip";
    

roiManager("Save", path);


run("Close");
