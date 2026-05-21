#!/usr/bin/env Rscript

# Mixed-effects workflow for synthetic culture and development data.

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- normalizePath(sub(file_arg, "", args[grep(file_arg, args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)

data_path <- file.path(root, "data", "cultural_development_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) {
  dir.create(outputs_dir, recursive = TRUE)
}

if (!file.exists(data_path)) {
  stop("Missing data/cultural_development_panel.csv. Run python/generate_cultural_development_panel.py first.")
}

panel <- read.csv(data_path)

mixed_model <- lmer(
  development_score ~ time + current_family + current_fit +
    current_support + current_flexibility + current_mismatch +
    society_climate + institutional_inclusion + linguistic_support +
    pluralism_index + child_resilience +
    (1 + time | society_id/child_id),
  data = panel
)

condition_model <- lm(
  development_score ~ time + cultural_condition + current_family +
    current_fit + current_support + institutional_inclusion + linguistic_support,
  data = panel
)

capture.output(
  list(
    mixed_model = summary(mixed_model),
    condition_model = summary(condition_model)
  ),
  file = file.path(outputs_dir, "r_culture_model_summary.txt")
)

trajectory <- panel |>
  group_by(time) |>
  summarize(
    average_development = mean(development_score),
    standard_error = sd(development_score) / sqrt(n()),
    lower = average_development - 1.96 * standard_error,
    upper = average_development + 1.96 * standard_error,
    average_mismatch = mean(current_mismatch),
    average_support = mean(current_support),
    .groups = "drop"
  )

write.csv(
  trajectory,
  file.path(outputs_dir, "r_culture_trajectory.csv"),
  row.names = FALSE
)

trajectory_plot <- ggplot(trajectory, aes(x = time, y = average_development)) +
  geom_line(linewidth = 1) +
  geom_ribbon(aes(ymin = lower, ymax = upper), alpha = 0.15) +
  labs(
    title = "Synthetic Culture and Development Across Societies",
    x = "Time",
    y = "Average development score"
  ) +
  theme_minimal()

ggsave(
  filename = file.path(outputs_dir, "r_culture_trajectory.png"),
  plot = trajectory_plot,
  width = 8,
  height = 5,
  dpi = 160
)

condition_trajectory <- panel |>
  group_by(cultural_condition, time) |>
  summarize(
    average_development = mean(development_score),
    .groups = "drop"
  )

write.csv(
  condition_trajectory,
  file.path(outputs_dir, "r_condition_trajectories.csv"),
  row.names = FALSE
)

condition_plot <- ggplot(
  condition_trajectory,
  aes(x = time, y = average_development, linetype = cultural_condition)
) +
  geom_line(linewidth = 1) +
  geom_point() +
  labs(
    title = "Synthetic Developmental Trajectories by Cultural Condition",
    x = "Time",
    y = "Average development score",
    linetype = "Condition"
  ) +
  theme_minimal()

ggsave(
  filename = file.path(outputs_dir, "r_condition_trajectories.png"),
  plot = condition_plot,
  width = 9,
  height = 5.5,
  dpi = 160
)

message("Wrote outputs/r_culture_model_summary.txt")
message("Wrote outputs/r_culture_trajectory.csv")
message("Wrote outputs/r_culture_trajectory.png")
message("Wrote outputs/r_condition_trajectories.csv")
message("Wrote outputs/r_condition_trajectories.png")
