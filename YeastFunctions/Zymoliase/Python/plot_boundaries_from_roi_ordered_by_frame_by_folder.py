
import os
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from read_roi import read_roi_file
import shutil
from statsmodels.nonparametric.smoothers_lowess import lowess

# Simulating the function calculate_mass_center()
def calculate_mass_center(x, y):
    x_center = np.mean(x)
    y_center = np.mean(y)
    return x_center, y_center

# Simulating the function angles()
def angles(x, y, x_center, y_center):
    x_rel = x - x_center
    y_rel = y - y_center
    r = np.sqrt(x_rel ** 2 + y_rel ** 2)
    theta = np.arctan2(y_rel, x_rel)
    return x_rel, y_rel, theta, r

# Path to root folder
root_folder = "C:/Users/Visitor/Desktop/alvaro/Zymoliase_analyse_trials/"

# Function to process ROI files in a folder
def process_folder(folder):
    for dirpath, dirnames, filenames in os.walk(folder):
        if 'RoiSet' in dirnames and 'export.csv' in filenames:
            roi_folder = os.path.join(dirpath, 'RoiSet')
            csv_path = os.path.join(dirpath, 'export.csv')
            process_roi_files(roi_folder, csv_path)  # <-- Pass roi_folder and csv_path as arguments

# Function to process ROI files in a specific folder
def process_roi_files(roi_folder, csv_path):
    df = pd.read_csv(csv_path, skiprows=range(1, 4))
    plots_folder = os.path.join(os.path.dirname(roi_folder), 'plots')
    # Check if the 'plots' folder already exists
    if not os.path.exists(plots_folder):
        os.makedirs(plots_folder)
    else:
        print(f"'plots' folder already exists in {os.path.dirname(roi_folder)}. Proceeding to the next folder.")
        return
    os.makedirs(plots_folder, exist_ok=True)
    angle_plots_by_number = {}
    profile_plots_by_number = {}

    # Function to process a specific ROI file
    def process_archivo_roi(roi_file):
        path_archivo_roi = os.path.join(roi_folder, roi_file)
        # Leer el archivo de ROI
        rois = read_roi_file(path_archivo_roi)

        # Process the ROI data
        for roi_name, roi_data in rois.items():
            # Obtain number associated to ROI
            number_associated = df.loc[df['LABEL'] == roi_name.split('.')[0], 'TRACK_ID'].iloc[0]

            # Obtain ROI's xy coordinates
            x = np.array(roi_data['x'])
            y = np.array(roi_data['y'])
            smoothed_x = lowess(x, range(len(x)), frac=0.1, return_sorted=False)
            smoothed_y = lowess(y, range(len(y)), frac=0.1, return_sorted=False)
            
            # Calculate mass center
            x_center, y_center = calculate_mass_center(x, y)
            
            # Double the first point at the end to close the plot
            smoothed_x = np.append(smoothed_x, smoothed_x[0])
            smoothed_y = np.append(smoothed_y, smoothed_y[0])
            
            # Generate polar angles plot
            fig_angles = plt.figure()
            ax_angles = fig_angles.add_subplot(111, projection='polar')
            x_rel, y_rel, theta, r = angles(smoothed_x, smoothed_y, x_center, y_center)
            ax_angles.plot(theta, r, '-')
            plt.title(f"plot_angles_{number_associated}_{roi_name}")
            plt.savefig(os.path.join(plots_folder, f"plot_angles_{number_associated}_{roi_name}.png"))
            plt.close(fig_angles)

            # Generate profile plot
            fig_profiles = plt.figure()
            ax_profiles = fig_profiles.add_subplot(111)
           
            x_mean = np.mean(x)
            y_mean = np.mean(y)
            x = x - x_mean
            y = y - y_mean

            # Smoothing the plot
            # Adjust windows amplitud for a smoother or rougher profile
            smoothed_x = lowess(x, range(len(x)), frac=0.1, return_sorted=False)
            smoothed_y = lowess(y, range(len(y)), frac=0.1, return_sorted=False)

            ax_profiles.plot(smoothed_x, label='x(L)')
            ax_profiles.plot(smoothed_y, label='y(L)')
            ax_profiles.legend()
            plt.title(f"plot_profiles_{number_associated}_{roi_name}")
            plt.savefig(os.path.join(plots_folder, f"plot_profiles_{number_associated}_{roi_name}.png"))
            plt.close(fig_profiles)

            # Save plots in dictionaries for overlapping
            if number_associated not in angle_plots_by_number:
                angle_plots_by_number[number_associated] = []
            angle_plots_by_number[number_associated].append(fig_angles)

            if number_associated not in profile_plots_by_number:
                profile_plots_by_number[number_associated] = []
            profile_plots_by_number[number_associated].append(fig_profiles)

    # Process ROI files
    for roi_file in os.listdir(roi_folder):
        process_archivo_roi(roi_file)


    # Iterate over each file in plot folder
    for file_name in os.listdir(plots_folder):
        # Obtain plot ID
        plot_id = file_name.split('_')[-1].split('.')[0]
        
        # Look for the correspondent frame in the DF
        frame = df[df['LABEL'].str.contains(plot_id)]['FRAME'].values
        
        
        # Folder to move the plot
        nuevo_dir = os.path.join(plots_folder, f'frame_{frame}/')
        
        # Create the path if it doesn't exist
        if not os.path.exists(nuevo_dir):
            os.makedirs(nuevo_dir)
        
        # Path of the current plot
        path_plot = os.path.join(plots_folder, file_name)
        
        # New paht
        new_path_plot = os.path.join(nuevo_dir, file_name)
        
        # Move the plot
        shutil.move(path_plot, new_path_plot)
       
    for number_associated, figuras in angle_plots_by_number.items():
        fig_combinada_angles = plt.figure()
        ax_angles = fig_combinada_angles.add_subplot(111, projection='polar')
        for fig in figuras:
            if fig.gca().lines:
                for line in fig.gca().lines:
                    ax_angles.plot(line.get_xdata(), line.get_ydata())
        plt.title(f"Gráficas de ángulos para número associated {number_associated}")
        plt.savefig(os.path.join(plots_folder, f"Gráficas de ángulos para número associated {number_associated}.png"))
                    
    for number_associated, figuras in profile_plots_by_number.items():
        fig_combinada_profiles = plt.figure()
        ax_profiles = fig_combinada_profiles.add_subplot(111)
        for fig in figuras:
            if fig.gca().lines:
                for line in fig.gca().lines:
                    ax_profiles.plot(line.get_xdata(), line.get_ydata())
        plt.title(f"Gráficas de profiles para número associated {number_associated}")
        plt.savefig(os.path.join(plots_folder, f"Gráficas de profiles para número associated {number_associated}.png"))


for folder in os.listdir(root_folder):
    folder_completa = os.path.join(root_folder, folder)
    if os.path.isdir(folder_completa):
        process_folder(folder_completa)
