% Specify the folder where the files are.
myFolder = 'C:\Users\uib\Desktop\Experimentos homogeneizacion\Exp_Hom_2\Tiff\trial';
% Check to make sure that folder actually exists. 
if ~isfolder(myFolder)
    errorMessage = sprintf('Error: The following folder does not exist:\n%s\nPlease specify a new folder.', myFolder);
    uiwait(warndlg(errorMessage));
    myFolder = uigetdir(); % Ask for a new one
    % 
    % 
    % .
    if myFolder == 0;
         % User clicked Cancel
         return;
    end
end
% Initialize an empty table to store the cumulative results
cumulativeTable = table();
% Get a list of all files in the folder with the desired file name pattern.
filePattern = fullfile(myFolder, '*.tif'); 
theFiles = dir(filePattern);
for k = 1 : length(theFiles)
    baseFileName = theFiles(k).name;
    fullFileName = fullfile(theFiles(k).folder, baseFileName);
    fprintf(1, 'Now reading %s\n', fullFileName);
    image_analysis_agg_AR_V1(fullFileName, myFolder);
    
end