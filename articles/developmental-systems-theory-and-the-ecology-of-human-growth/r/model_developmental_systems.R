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

data_path <- file.path(root, "data", "developmental_systems_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_developmental_systems_panel.py first.")

panel <- read.csv(data_path)

development_model <- lmer(
  development_score ~ time + biological_sensitivity +
    current_family + current_peer + school_climate +
    curriculum_opportunity + neighborhood_safety + service_access +
    material_security + intervention_exposure + ecological_stress +
    biological_sensitivity:current_family +
    biological_sensitivity:ecological_stress +
    (1 + time | school_id/child_id),
  data = panel
)

stress_model <- lmer(
  ecological_stress ~ time + current_family + current_peer +
    school_climate + curriculum_opportunity + neighborhood_safety +
    service_access + material_security + intervention_exposure +
    (1 + time | school_id/child_id),
  data = panel
)

capture.output(
  list(
    development_model = summary(development_model),
    ecological_stress_model = summary(stress_model)
  ),
  file = file.path(outputs_dir, "r_developmental_systems_model_summary.txt")
)

trajectory <- panel |>
  group_by(time, intervention_exposure) |>
  summarize(
    average_development = mean(development_score),
    average_ecological_support = mean(ecological_support),
    average_ecological_stress = mean(ecological_stress),
    standard_error = sd(development_score) / sqrt(n()),
    lower = average_development - 1.96 * standard_error,
    upper = average_development + 1.96 * standard_error,
    .groups = "drop"
  ) |>
  mutate(group = ifelse(intervention_exposure == 1, "Intervention", "No intervention"))

write.csv(trajectory, file.path(outputs_dir, "r_development_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_development_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_development, linetype = group)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper, group = group), alpha = 0.12) +
    labs(title = "Synthetic Developmental Systems Trajectories", x = "Time", y = "Average development", linetype = "Group") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

support <- panel |>
  group_by(time) |>
  summarize(
    average_ecological_support = mean(ecological_support),
    average_ecological_stress = mean(ecological_stress),
    average_family = mean(current_family),
    average_peer = mean(current_peer),
    .groups = "drop"
  )

write.csv(support, file.path(outputs_dir, "r_ecological_support_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_ecological_support_trajectory.png"),
  plot = ggplot(support, aes(x = time)) +
    geom_line(aes(y = average_ecological_support, linetype = "ecological support"), linewidth = 1) +
    geom_line(aes(y = average_ecological_stress, linetype = "ecological stress"), linewidth = 1) +
    labs(title = "Synthetic Ecological Support and Stress", x = "Time", y = "Average ecological index", linetype = "Index") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R developmental systems outputs.")
