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

data_path <- file.path(root, "data", "stage_theory_development_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_stage_theory_panel.py first.")

panel <- read.csv(data_path)

model <- lmer(
  development_score ~ time + current_support + school_support +
    resource_stability + chronic_stress + stage_pattern +
    threshold_on + logistic_transition +
    stage_pattern:threshold_on +
    stage_pattern:logistic_transition +
    stage_pattern:threshold_on:transition_readiness +
    (1 + time | context_id/child_id),
  data = panel
)

capture.output(
  summary(model),
  file = file.path(outputs_dir, "r_stage_model_summary.txt")
)

trajectory <- panel |>
  group_by(time, stage_pattern) |>
  summarize(
    average_score = mean(development_score),
    average_readiness = mean(transition_readiness),
    standard_error = sd(development_score) / sqrt(n()),
    .groups = "drop"
  ) |>
  mutate(
    lower = average_score - 1.96 * standard_error,
    upper = average_score + 1.96 * standard_error,
    pattern_label = ifelse(stage_pattern == 1, "Stage-like reorganization", "Mostly continuous growth")
  )

write.csv(trajectory, file.path(outputs_dir, "r_stage_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_stage_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_score, linetype = pattern_label)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper, group = pattern_label), alpha = 0.12) +
    labs(title = "Synthetic Continuous and Stage-Like Developmental Patterns", x = "Time", y = "Average development score", linetype = "Pattern") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

threshold_summary <- panel |>
  group_by(threshold_time, stage_pattern) |>
  summarize(
    average_score = mean(development_score),
    average_readiness = mean(transition_readiness),
    average_support = mean(current_support),
    average_stress = mean(chronic_stress),
    .groups = "drop"
  ) |>
  mutate(pattern_label = ifelse(stage_pattern == 1, "Stage-like reorganization", "Mostly continuous growth"))

write.csv(threshold_summary, file.path(outputs_dir, "r_threshold_summary.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_threshold_summary.png"),
  plot = ggplot(threshold_summary, aes(x = threshold_time, y = average_score, linetype = pattern_label)) +
    geom_line(linewidth = 1) +
    geom_point(size = 2) +
    labs(title = "Synthetic Threshold Timing and Developmental Outcome", x = "Threshold time", y = "Average development score", linetype = "Pattern") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R stage-like development outputs.")
