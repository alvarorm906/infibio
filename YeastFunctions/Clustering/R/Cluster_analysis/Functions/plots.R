plots <- function (df, bins=100, path_save){
  library(dplyr)
  library(ggplot2)

  
  
  # Define outlier criterion (for example, values outside 1.5 * IQR)
  lower_bound <- quantile(df$area_norm, 0.25) - 5 * IQR(df$area_norm)
  upper_bound <- quantile(df$area_norm, 0.75) + 5 * IQR(df$area_norm)
  
  # Filter out outliers
  df_filtered <- df %>%
    filter(area_norm >= lower_bound  & area_norm <= upper_bound )
  
  # Plot relative count of areas per time using bins after filtering outliers
  ggplot(df_filtered, aes(x = area_norm, fill = as.factor(Time))) +
    geom_histogram(binwidth = (max(df_filtered$area_norm) - min(df_filtered$area_norm)) / bins, alpha = 0.5, position = "identity") +
    ggtitle("Distribution of Areas per Time (Excluding Outliers)") +
    xlab("Area normalized") +
    ylab("Count") +
    theme_minimal() +
    facet_wrap(~Time)
  
  ggsave("Distribution of Areas per Time (Excluding Outliers).png", path = paste0(path_save,"\\results"), width = 1920, height = 1216, units = "px",bg = 'white')

    ggplot(df_filtered, aes(x = area_norm, fill = as.factor(Time))) +
    geom_histogram(binwidth = (max(df_filtered$area_norm) - min(df_filtered$area_norm)) / bins, alpha = 0.5, position = "identity",  aes(y = ..count.. / sum(..count..))) +
    ggtitle("Relative distribution of Areas per Time (Excluding Outliers)") +
    xlab("Area normalized") +
    ylab("Count") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1))+
    facet_wrap(~Time)
    ggsave( "Relative distribution of Areas per Time (Excluding Outliers).png", path = paste0(path_save,"\\results"), width = 1920, height = 1216, units = "px", bg = 'white')
    
  # Define the percentile threshold for extreme values
  percentile_threshold <- 0.95  # Consider values beyond the 95th percentile as extreme
  percentile_threshold_2 <- 0.99
  # Calculate the threshold value
  threshold <- quantile(df$area_norm, percentile_threshold)
  threshold_2 <- quantile (df$area_norm, percentile_threshold_2)
  # Filter out extreme values
  df_extreme <- df %>%
    filter(area_norm > threshold & area_norm < threshold_2)
  
  # Plot extreme values per time
  ggplot(df_extreme, aes(x = as.factor(Time), y = area_norm)) +
    geom_point() +
    ggtitle("Extreme Values per Time") +
    xlab("Time") +
    ylab("Area") +
    theme_minimal()
  ggsave("Extreme Values per Time.png", path = paste0(path_save,"\\results"), width = 1920, height = 1216, units = "px", bg = 'white')
  
  # Plot violin plots per time after filtering outliers
  ggplot(df_filtered, aes(x = as.factor(Time), y = area_norm, fill = as.factor(Time))) +
    geom_violin() +
    ggtitle("Distribution of Areas per Time Violin Plot (Excluding Outliers)") +
    xlab("Time") +
    ylab("Area") +
    theme_minimal()
  ggsave( "Distribution of Areas per Time Violin Plot (Excluding Outliers).png", path = paste0(path_save,"\\results"),  width = 1920, height = 1216, units = "px", bg = 'white')
  
  
}
