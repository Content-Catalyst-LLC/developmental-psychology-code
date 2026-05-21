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

data_path <- file.path(root, "data", "family_systems_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_family_systems_panel.py first.")

panel <- read.csv(data_path)

development_model <- lmer(
  development_score ~ time + current_parenting + current_family +
    current_stress + household_stability + kin_support +
    economic_security + current_sibling + current_regulation +
    caregiver_support + current_parenting:current_family +
    (1 + time | household_id/child_id),
  data = panel
)

support_model <- lmer(
  family_support_index ~ time + current_parenting + current_family +
    current_stress + household_stability + kin_support +
    economic_security + current_sibling + current_regulation +
    caregiver_support +
    (1 + time | household_id/child_id),
  data = panel
)

capture.output(
  list(
    development_model = summary(development_model),
    family_support_model = summary(support_model)
  ),
  file = file.path(outputs_dir, "r_family_systems_model_summary.txt")
)

trajectory <- panel |>
  group_by(time, caregiver_support) |>
  summarize(
    average_development = mean(development_score),
    average_family_support = mean(family_support_index),
    standard_error = sd(development_score) / sqrt(n()),
    lower = average_development - 1.96 * standard_error,
    upper = average_development + 1.96 * standard_error,
    .groups = "drop"
  ) |>
  mutate(group = ifelse(caregiver_support == 1, "Caregiver support", "No added support"))

write.csv(trajectory, file.path(outputs_dir, "r_development_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_development_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_development, linetype = group)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper, group = group), alpha = 0.12) +
    labs(title = "Synthetic Parenting, Family Systems, and Development", x = "Time", y = "Average development", linetype = "Group") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

family_support <- panel |>
  group_by(time) |>
  summarize(
    average_family_support = mean(family_support_index),
    average_parenting = mean(current_parenting),
    average_family = mean(current_family),
    average_stress = mean(current_stress),
    .groups = "drop"
  )

write.csv(family_support, file.path(outputs_dir, "r_family_support_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_family_support_trajectory.png"),
  plot = ggplot(family_support, aes(x = time, y = average_family_support)) +
    geom_line(linewidth = 1) +
    geom_point() +
    labs(title = "Synthetic Family Support Trajectory", x = "Time", y = "Average family support") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R family systems outputs.")
