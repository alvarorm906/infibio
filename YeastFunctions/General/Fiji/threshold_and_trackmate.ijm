setAutoThreshold("Default no-reset");
//run("Threshold...");
setOption("BlackBackground", false);
run("Convert to Mask", "method=Default background=Light calculate");
run("Fill Holes", "stack");
run("TrackMate");
