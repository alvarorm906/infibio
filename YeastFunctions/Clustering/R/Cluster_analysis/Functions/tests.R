tests <- function (df, path_save){
  anova_result <- aov(area_norm ~ Time, data = df)

  # browser()
  # Tukey post hoc test
  tukey_result <- TukeyHSD(anova_result)

  # Save ANOVA summary to CSV
  anova_summary <- summary(anova_result)
  capture.output(summary(anova_result),file=paste0(path_save,"\\results","\\anova.xls"))   
  # Extract individual tables from Tukey result and save to CSV
  capture.output(summary(tukey_result),file=paste0(path_save,"\\results","\\tukey.xls"))
}