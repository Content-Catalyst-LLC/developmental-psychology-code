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

data_path <- file.path(root, "data", "life_course_inequality_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_life_course_inequality.py first.")

panel <- read.csv(data_path)

mixed_model <- lmer(
  development_score ~ time + cumulative_resources + cumulative_burden +
    current_support + transition_support + health_status +
    community_opportunity + institutional_support + environmental_safety +
    person_resilience + (1 + time | context_id/person_id),
  data = panel
)

profile_model <- lm(
  development_score ~ time + inequality_profile + current_support +
    health_status + community_opportunity + institutional_support,
  data = panel
)

capture.output(
  list(mixed_model = summary(mixed_model), profile_model = summary(profile_model)),
  file = file.path(outputs_dir, "r_life_course_model_summary.txt")
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

write.csv(trajectory, file.path(outputs_dir, "r_life_course_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_life_course_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_development)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper), alpha = 0.15) +
    labs(
      title = "Synthetic Development, Inequality, and the Life Course",
      x = "Time",
      y = "Average development score"
    ) +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

profile_trajectory <- panel |>
  group_by(inequality_profile, time) |>
  summarize(average_development = mean(development_score), .groups = "drop")

write.csv(profile_trajectory, file.path(outputs_dir, "r_profile_trajectories.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_profile_trajectories.png"),
  plot = ggplot(profile_trajectory, aes(x = time, y = average_development, linetype = inequality_profile)) +
    geom_line(linewidth = 1) +
    geom_point() +
    labs(
      title = "Synthetic Developmental Trajectories by Inequality Profile",
      x = "Time",
      y = "Average development score",
      linetype = "Profile"
    ) +
    theme_minimal(),
  width = 9,
  height = 5.5,
  dpi = 160
)

message("Wrote R model outputs.")
