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

data_path <- file.path(root, "data", "continuity_discontinuity_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_continuity_discontinuity_panel.py first.")

panel <- read.csv(data_path)
panel$time_squared <- panel$time^2

model <- lmer(
  development_score ~ time + time_squared + current_support + school_support +
    resource_stability + chronic_stress + institutional_rupture +
    intervention_exposure + threshold_sensitive +
    threshold_on + logistic_transition +
    threshold_sensitive:threshold_on +
    threshold_sensitive:logistic_transition +
    threshold_sensitive:threshold_on:transition_readiness +
    (1 + time | context_id/person_id),
  data = panel
)

capture.output(
  summary(model),
  file = file.path(outputs_dir, "r_continuity_discontinuity_model_summary.txt")
)

trajectory <- panel |>
  group_by(time, threshold_sensitive) |>
  summarize(
    average_score = mean(development_score),
    average_readiness = mean(transition_readiness),
    average_support = mean(current_support),
    average_stress = mean(chronic_stress),
    average_rupture = mean(institutional_rupture),
    average_intervention = mean(intervention_exposure),
    standard_error = sd(development_score) / sqrt(n()),
    .groups = "drop"
  ) |>
  mutate(
    lower = average_score - 1.96 * standard_error,
    upper = average_score + 1.96 * standard_error,
    group_label = ifelse(
      threshold_sensitive == 1,
      "Threshold-sensitive development",
      "Mostly continuous growth"
    )
  )

write.csv(trajectory, file.path(outputs_dir, "r_developmental_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_developmental_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_score, linetype = group_label)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper, group = group_label), alpha = 0.12) +
    labs(title = "Synthetic Continuous and Threshold-Sensitive Development", x = "Time", y = "Average development score", linetype = "Trajectory type") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

threshold_summary <- panel |>
  group_by(threshold_time, threshold_sensitive) |>
  summarize(
    average_score = mean(development_score),
    average_readiness = mean(transition_readiness),
    average_support = mean(current_support),
    average_stress = mean(chronic_stress),
    average_rupture = mean(institutional_rupture),
    average_intervention = mean(intervention_exposure),
    .groups = "drop"
  ) |>
  mutate(
    group_label = ifelse(
      threshold_sensitive == 1,
      "Threshold-sensitive development",
      "Mostly continuous growth"
    )
  )

write.csv(threshold_summary, file.path(outputs_dir, "r_threshold_summary.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_threshold_summary.png"),
  plot = ggplot(threshold_summary, aes(x = threshold_time, y = average_score, linetype = group_label)) +
    geom_line(linewidth = 1) +
    geom_point(size = 2) +
    labs(title = "Synthetic Threshold Timing and Developmental Outcome", x = "Threshold time", y = "Average development score", linetype = "Trajectory type") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R continuity/discontinuity outputs.")
