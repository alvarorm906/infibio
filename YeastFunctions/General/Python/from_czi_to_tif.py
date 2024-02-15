# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# Get the directory containing subfolders with images
main_dir = r'C:/Users/Visitor/Desktop/alvaro/Zymoliase_analyse_trials/Exp_Zymolyase01-005_ConA03-2024110'  # Remove leading/trailing spaces


import os
import sys

try:
    from .czifile import czi2tif
except ImportError:
    try:
        from czifile.czifile import czi2tif
    except ImportError:
        from czifile import czi2tif

def convert_czi_to_tif(directory):
    # List all files and subdirectories in the current directory
    contents = os.listdir(directory)
    
    # Check if any CZI files are present in the current directory
    czi_files = [f for f in contents if f.endswith('.czi')]
    if czi_files:
        print(f"Found CZI files in directory: {directory}")
        # Convert each CZI file to TIFF
        for czi_file in czi_files:
            czi_path = os.path.join(directory, czi_file)
            try:
                tif_path = os.path.splitext(czi_path)[0] + ".tif"
                czi2tif(czi_path, tif_path)
                print(f"Converted {czi_file} to TIFF.")
                # Delete the original .czi file
                os.remove(czi_path)
                print(f"Deleted {czi_file}.")
            except Exception as e:
                print(f"Error converting {czi_path}:", str(e))
    
    # Recursively search subdirectories for CZI files
    for item in contents:
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            convert_czi_to_tif(item_path)

# Get the directory containing subfolders with images
main_dir = input("Enter the directory path: ").strip()  # Remove leading/trailing spaces

# Check if the provided directory exists
if not os.path.exists(main_dir):
    print(f"The directory '{main_dir}' does not exist.")
    sys.exit(1)

# Start the recursive conversion process
convert_czi_to_tif(main_dir)



