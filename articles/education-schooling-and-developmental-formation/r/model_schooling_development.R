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

data_path <- file.path(root, "data", "schooling_development_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_schooling_development_panel.py first.")

panel <- read.csv(data_path)

development_model <- lmer(
  development_score ~ time + current_teacher + current_peer +
    school_climate + curriculum_opportunity + current_family +
    current_confidence + resource_capacity + intervention +
    connectedness_score + current_stress +
    current_teacher:current_peer +
    (1 + time | school_id/student_id),
  data = panel
)

connectedness_model <- lmer(
  connectedness_score ~ time + current_teacher + current_peer +
    school_climate + restorative_practice + current_stress +
    current_family + current_confidence +
    (1 + time | school_id/student_id),
  data = panel
)

capture.output(
  list(
    development_model = summary(development_model),
    connectedness_model = summary(connectedness_model)
  ),
  file = file.path(outputs_dir, "r_schooling_model_summary.txt")
)

trajectory <- panel |>
  group_by(time, intervention) |>
  summarize(
    average_development = mean(development_score),
    average_connectedness = mean(connectedness_score),
    standard_error = sd(development_score) / sqrt(n()),
    lower = average_development - 1.96 * standard_error,
    upper = average_development + 1.96 * standard_error,
    .groups = "drop"
  ) |>
  mutate(group = ifelse(intervention == 1, "Support program", "No program"))

write.csv(trajectory, file.path(outputs_dir, "r_development_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_development_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_development, linetype = group)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper, group = group), alpha = 0.12) +
    labs(title = "Synthetic Education, Schooling, and Developmental Formation", x = "Time", y = "Average development", linetype = "Group") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

connectedness <- panel |>
  group_by(time) |>
  summarize(
    average_connectedness = mean(connectedness_score),
    average_teacher = mean(current_teacher),
    average_peer = mean(current_peer),
    average_stress = mean(current_stress),
    .groups = "drop"
  )

write.csv(connectedness, file.path(outputs_dir, "r_connectedness_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_connectedness_trajectory.png"),
  plot = ggplot(connectedness, aes(x = time, y = average_connectedness)) +
    geom_line(linewidth = 1) +
    geom_point() +
    labs(title = "Synthetic School Connectedness Trajectory", x = "Time", y = "Average connectedness") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R schooling outputs.")
