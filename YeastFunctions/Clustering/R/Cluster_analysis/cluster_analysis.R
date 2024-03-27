library(tidyverse)

# Work directory
setwd("C:\\Users\\uib\\Nextcloud\\LAB\\Wetlab\\alvaro_desktop\\Experimentos\\Experimentos homogeneizacion\\Exp_ClusterSK1_shaker20hz_C1000_RT_20240305_tiff")
path <- "C:\\Users\\uib\\Nextcloud\\LAB\\Wetlab\\alvaro_desktop\\Experimentos\\Experimentos homogeneizacion\\Exp_ClusterSK1_shaker20hz_C1000_RT_20240305_tiff"

source('C:\\Users\\uib\\Desktop\\Scripts\\R_functions\\clean_weird_shapes.r')
source('C:\\Users\\uib\\Desktop\\Scripts\\R_functions\\combine_csv.r')
source('C:\\Users\\uib\\Desktop\\Scripts\\R_functions\\plots.r')
source('C:\\Users\\uib\\Desktop\\Scripts\\R_functions\\tests.r')

model_path <- paste0('C:\\Users\\uib\\Desktop\\spor_differentiation\\labeled\\', "classification_cells_not_wanted.rds")

csv_combined <- combine_csv(path)
csv_cleaned <- clean_weird_shapes(csv_combined, model_path)
plots(csv_cleaned, 100, path)
tests(csv_cleaned, path)