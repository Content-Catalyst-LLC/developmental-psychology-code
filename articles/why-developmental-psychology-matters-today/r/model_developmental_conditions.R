#!/usr/bin/env Rscript

# Mixed-effects model for synthetic developmental conditions.
# This script uses generated data and writes model summaries and trajectory plots.

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = TRUE)
data_path <- file.path(root, "data", "developmental_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) {
  dir.create(outputs_dir, recursive = TRUE)
}

if (!file.exists(data_path)) {
  stop("Missing data/developmental_panel.csv. Run python/generate_developmental_panel.py first.")
}

panel <- read.csv(data_path)

model <- lmer(
  development_score ~ time + current_support + current_risk +
    policy_access + health_status + institutional_climate +
    resource_level + person_resilience + (1 + time | context_id),
  data = panel
)

capture.output(
  summary(model),
  file = file.path(outputs_dir, "r_model_summary.txt")
)

trajectory <- panel |>
  group_by(time) |>
  summarize(
    average_development = mean(development_score),
    standard_error = sd(development_score) / sqrt(n()),
    lower = average_development - 1.96 * standard_error,
    upper = average_development + 1.96 * standard_error,
    .groups = "drop"
  )

write.csv(
  trajectory,
  file.path(outputs_dir, "r_average_trajectory.csv"),
  row.names = FALSE
)

plot <- ggplot(trajectory, aes(x = time, y = average_development)) +
  geom_line(linewidth = 1) +
  geom_ribbon(aes(ymin = lower, ymax = upper), alpha = 0.15) +
  labs(
    title = "Synthetic Developmental Conditions Across the Life Course",
    x = "Time",
    y = "Average development score"
  ) +
  theme_minimal()

ggsave(
  filename = file.path(outputs_dir, "r_average_trajectory.png"),
  plot = plot,
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote outputs/r_model_summary.txt")
message("Wrote outputs/r_average_trajectory.csv")
message("Wrote outputs/r_average_trajectory.png")
