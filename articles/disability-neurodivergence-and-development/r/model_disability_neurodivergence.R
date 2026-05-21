#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- normalizePath(sub(file_arg, "", args[grep(file_arg, args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)

data_path <- file.path(root, "data", "disability_neurodivergence_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_disability_neurodivergence_panel.py first.")

panel <- read.csv(data_path)

development_model <- lmer(
  development_score ~ time + neuro_profile + current_support +
    current_access + current_communication + current_barrier +
    participation_score + current_advocacy + inclusion_climate +
    service_access + sensory_flexibility +
    current_support:current_access +
    current_barrier:neuro_profile +
    (1 + time | setting_id/child_id),
  data = panel
)

participation_model <- lmer(
  participation_score ~ time + neuro_profile + current_support +
    current_access + current_communication + current_barrier +
    current_advocacy + inclusion_climate + service_access +
    sensory_flexibility +
    (1 + time | setting_id/child_id),
  data = panel
)

capture.output(
  list(
    development_model = summary(development_model),
    participation_model = summary(participation_model)
  ),
  file = file.path(outputs_dir, "r_accessibility_model_summary.txt")
)

trajectory <- panel |>
  group_by(time) |>
  summarize(
    average_development = mean(development_score),
    average_participation = mean(participation_score),
    standard_error = sd(development_score) / sqrt(n()),
    lower = average_development - 1.96 * standard_error,
    upper = average_development + 1.96 * standard_error,
    .groups = "drop"
  )

write.csv(trajectory, file.path(outputs_dir, "r_development_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_development_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_development)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper), alpha = 0.15) +
    labs(title = "Synthetic Disability, Neurodivergence, and Development", x = "Time", y = "Average development") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

ggsave(
  filename = file.path(outputs_dir, "r_participation_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_participation)) +
    geom_line(linewidth = 1) +
    geom_point() +
    labs(title = "Synthetic Participation Trajectory", x = "Time", y = "Average participation") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R accessibility outputs.")
