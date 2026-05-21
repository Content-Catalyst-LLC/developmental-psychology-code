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

data_path <- file.path(root, "data", "nature_nurture_development_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_nature_nurture_panel.py first.")

panel <- read.csv(data_path)

model <- lmer(
  development_score ~ time + biological_sensitivity + caregiver_support +
    acute_stress + structural_risk + chronic_adversity +
    institutional_support + disability_support + resource_stability +
    intervention + protective_context +
    biological_sensitivity:caregiver_support +
    biological_sensitivity:acute_stress +
    biological_sensitivity:protective_context +
    (1 + time | school_id/child_id),
  data = panel
)

capture.output(
  summary(model),
  file = file.path(outputs_dir, "r_nature_nurture_model_summary.txt")
)

trajectory <- panel |>
  group_by(time, structural_risk) |>
  summarize(
    average_development = mean(development_score),
    average_support = mean(caregiver_support),
    average_stress = mean(acute_stress),
    average_protective_context = mean(protective_context),
    standard_error = sd(development_score) / sqrt(n()),
    .groups = "drop"
  ) |>
  mutate(
    lower = average_development - 1.96 * standard_error,
    upper = average_development + 1.96 * standard_error,
    risk_group = ifelse(structural_risk == 1, "Higher structural risk", "Lower structural risk")
  )

write.csv(trajectory, file.path(outputs_dir, "r_structural_risk_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_structural_risk_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_development, linetype = risk_group)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper, group = risk_group), alpha = 0.12) +
    labs(title = "Synthetic Developmental Trajectories by Structural Risk", x = "Time", y = "Average development score", linetype = "Group") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

support_summary <- panel |>
  group_by(time) |>
  summarize(
    average_caregiver_support = mean(caregiver_support),
    average_acute_stress = mean(acute_stress),
    average_protective_context = mean(protective_context),
    average_intervention = mean(intervention),
    average_development = mean(development_score),
    .groups = "drop"
  )

write.csv(support_summary, file.path(outputs_dir, "r_protective_context_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_protective_context_trajectory.png"),
  plot = ggplot(support_summary, aes(x = time)) +
    geom_line(aes(y = average_caregiver_support, linetype = "caregiver support"), linewidth = 1) +
    geom_line(aes(y = average_acute_stress, linetype = "acute stress"), linewidth = 1) +
    geom_line(aes(y = average_protective_context, linetype = "protective context"), linewidth = 1) +
    geom_line(aes(y = average_intervention, linetype = "intervention"), linewidth = 1) +
    labs(title = "Synthetic Nature-Nurture Protective Context Over Time", x = "Time", y = "Average index", linetype = "Measure") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R nature-nurture development outputs.")
