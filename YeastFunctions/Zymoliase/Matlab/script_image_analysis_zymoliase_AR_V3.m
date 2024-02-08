% Specify the folder where the files are.
myFolder = 'C:\Users\uib\Desktop\prueba_script_python\prueba_zymoliasa\tiff';

% Check if the folder exists.
if ~isfolder(myFolder)
    errorMessage = sprintf('Error: The following folder does not exist:\n%s\nPlease specify a new folder.', myFolder);
    uiwait(warndlg(errorMessage));
    myFolder = uigetdir(); % Ask for a new one
    if myFolder == 0
        % User clicked Cancel
        return;
    end
end

% Initialize an empty table to store the cumulative results
cumulativeTable = table();

% Get a list of all files in the folder with the desired file name pattern.
filePattern = fullfile(myFolder, '*.tif');
theFiles = dir(filePattern);

% Initialize reference point
x_reference = [];
y_reference = [];

for k = 1 : length(theFiles)
    baseFileName = theFiles(k).name;
    fullFileName = fullfile(theFiles(k).folder, baseFileName);
    fprintf(1, 'Now reading %s\n', fullFileName);
    
    % Use reference point if available
    if isempty(x_reference) || isempty(y_reference)
        image_analysis_cell_AR_V3(fullFileName, myFolder);
        
        % Load propsbw_cleaned from the saved MAT file
        [~, name, ~] = fileparts(baseFileName);
        try
            load(fullfile(myFolder, [name, '_results.mat']), 'propsbw_cleaned');
        catch
            % Handle the case when loading fails
            disp('Error loading propsbw_cleaned.');
            propsbw_cleaned = []; % Set propsbw_cleaned to empty if loading fails
        end
        
        % Use centroid of the first cell as reference point if available
        if ~isempty(propsbw_cleaned)
            x_reference = propsbw_cleaned(1).Centroid(1);
            y_reference = propsbw_cleaned(1).Centroid(2);
        else
            % Handle the case when propsbw_cleaned is empty
            % You may want to define default values for x_reference and y_reference here
            % For example:
            x_reference = 0;
            y_reference = 0;
        end
    end
    
    % Use reference point
    image_analysis_cell_AR_V3(fullFileName, myFolder, x_reference, y_reference);
    
    % Save the processed image with a new name (you can customize the name)
    [~, name, ext] = fileparts(baseFileName);
    saveFileName = fullfile(myFolder, [name, '_processed', ext]);
end


