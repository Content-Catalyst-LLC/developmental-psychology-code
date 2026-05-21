#!/usr/bin/env Rscript

# Synthetic timing-window models for critical and sensitive periods.

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- normalizePath(sub(file_arg, "", args[grep(file_arg, args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
data_path <- file.path(root, "data", "developmental_timing_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) {
  dir.create(outputs_dir, recursive = TRUE)
}

if (!file.exists(data_path)) {
  stop("Missing data/developmental_timing_panel.csv. Run python/generate_timing_panel.py first.")
}

panel <- read.csv(data_path)

critical_model <- lm(
  critical_outcome ~ time + experience * critical_weight +
    support + adversity + institutional_support + resource_level,
  data = panel
)

sensitive_model <- lm(
  sensitive_outcome ~ time + experience * early_sensitive_weight +
    support + adversity + institutional_support + resource_level,
  data = panel
)

multi_window_model <- lm(
  multi_window_outcome ~ time +
    experience * early_sensitive_weight +
    experience * adolescent_sensitive_weight +
    support + adversity + institutional_support + resource_level,
  data = panel
)

mixed_model <- lmer(
  multi_window_outcome ~ time +
    experience * early_sensitive_weight +
    experience * adolescent_sensitive_weight +
    support + adversity + institutional_support + resource_level +
    (1 | context_id),
  data = panel
)

capture.output(
  list(
    critical_model = summary(critical_model),
    sensitive_model = summary(sensitive_model),
    multi_window_model = summary(multi_window_model),
    mixed_model = summary(mixed_model)
  ),
  file = file.path(outputs_dir, "r_timing_model_summary.txt")
)

trajectory <- panel |>
  group_by(time) |>
  summarize(
    critical_weight = mean(critical_weight),
    early_sensitive_weight = mean(early_sensitive_weight),
    adolescent_sensitive_weight = mean(adolescent_sensitive_weight),
    residual_plasticity_weight = mean(residual_plasticity_weight),
    critical_outcome = mean(critical_outcome),
    sensitive_outcome = mean(sensitive_outcome),
    multi_window_outcome = mean(multi_window_outcome),
    recovery_outcome = mean(recovery_outcome),
    .groups = "drop"
  )

write.csv(
  trajectory,
  file.path(outputs_dir, "r_timing_trajectory.csv"),
  row.names = FALSE
)

windows_plot <- ggplot(trajectory, aes(x = time)) +
  geom_line(aes(y = critical_weight, linetype = "Critical period"), linewidth = 1) +
  geom_line(aes(y = early_sensitive_weight, linetype = "Early sensitive period"), linewidth = 1) +
  geom_line(aes(y = adolescent_sensitive_weight, linetype = "Adolescent sensitive period"), linewidth = 1) +
  geom_line(aes(y = residual_plasticity_weight, linetype = "Residual plasticity"), linewidth = 1) +
  labs(
    title = "Synthetic Critical and Sensitive Period Timing Weights",
    x = "Developmental time",
    y = "Timing weight",
    linetype = "Timing model"
  ) +
  theme_minimal()

ggsave(
  filename = file.path(outputs_dir, "r_timing_windows.png"),
  plot = windows_plot,
  width = 9,
  height = 5.5,
  dpi = 160
)

outcomes_plot <- ggplot(trajectory, aes(x = time)) +
  geom_line(aes(y = critical_outcome, linetype = "Critical outcome"), linewidth = 1) +
  geom_line(aes(y = sensitive_outcome, linetype = "Sensitive outcome"), linewidth = 1) +
  geom_line(aes(y = multi_window_outcome, linetype = "Multi-window outcome"), linewidth = 1) +
  geom_line(aes(y = recovery_outcome, linetype = "Recovery outcome"), linewidth = 1) +
  labs(
    title = "Synthetic Timing-Weighted Developmental Outcomes",
    x = "Developmental time",
    y = "Average synthetic outcome",
    linetype = "Outcome"
  ) +
  theme_minimal()

ggsave(
  filename = file.path(outputs_dir, "r_timing_outcomes.png"),
  plot = outcomes_plot,
  width = 9,
  height = 5.5,
  dpi = 160
)

message("Wrote outputs/r_timing_model_summary.txt")
message("Wrote outputs/r_timing_trajectory.csv")
message("Wrote outputs/r_timing_windows.png")
message("Wrote outputs/r_timing_outcomes.png")
