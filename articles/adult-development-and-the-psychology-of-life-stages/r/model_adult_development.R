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

data_path <- file.path(root, "data", "adult_development_life_stages_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_adult_development_panel.py first.")

panel <- read.csv(data_path)

adjustment_model <- lmer(
  adjustment_score ~ time + current_relational_support +
    current_work_integration + current_health_burden +
    current_adaptive_resources + current_role_burden +
    institutional_support + community_stability +
    young_stage + midlife_stage + later_stage +
    current_relational_support:current_adaptive_resources +
    (1 + time | context_id/id),
  data = panel
)

burden_model <- lmer(
  adjustment_score ~ time + current_role_burden + current_health_burden +
    current_relational_support + current_adaptive_resources +
    current_work_integration + institutional_support +
    life_stage + (1 + time | context_id/id),
  data = panel
)

capture.output(
  list(
    adjustment_model = summary(adjustment_model),
    burden_model = summary(burden_model)
  ),
  file = file.path(outputs_dir, "r_adult_development_model_summary.txt")
)

trajectory <- panel |>
  group_by(time, life_stage) |>
  summarize(
    average_adjustment = mean(adjustment_score),
    standard_error = sd(adjustment_score) / sqrt(n()),
    lower = average_adjustment - 1.96 * standard_error,
    upper = average_adjustment + 1.96 * standard_error,
    .groups = "drop"
  )

write.csv(trajectory, file.path(outputs_dir, "r_adult_stage_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_adult_stage_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_adjustment, linetype = life_stage)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper, group = life_stage), alpha = 0.12) +
    labs(title = "Synthetic Adult Development Across Life Stages", x = "Time", y = "Average adjustment", linetype = "Life stage") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

support_burden <- panel |>
  group_by(time) |>
  summarize(
    average_support = mean(current_relational_support),
    average_work = mean(current_work_integration),
    average_health = mean(current_health_burden),
    average_resources = mean(current_adaptive_resources),
    average_role_burden = mean(current_role_burden),
    .groups = "drop"
  )

write.csv(support_burden, file.path(outputs_dir, "r_adult_support_burden_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_adult_support_burden_trajectory.png"),
  plot = ggplot(support_burden, aes(x = time)) +
    geom_line(aes(y = average_support, linetype = "relational support"), linewidth = 1) +
    geom_line(aes(y = average_work, linetype = "work integration"), linewidth = 1) +
    geom_line(aes(y = average_health, linetype = "health burden"), linewidth = 1) +
    geom_line(aes(y = average_role_burden, linetype = "role burden"), linewidth = 1) +
    labs(title = "Synthetic Adult Support, Work, Health, and Role Burden", x = "Time", y = "Average index", linetype = "Measure") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R adult development outputs.")
