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

data_path <- file.path(root, "data", "developmental_psychopathology_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_developmental_psychopathology.py first.")

panel <- read.csv(data_path)

mixed_model <- lmer(
  adaptation_score ~ time + current_regulation + current_support +
    current_stability + current_risk + cumulative_risk +
    community_support + school_belonging + service_access +
    transition_support + biological_sensitivity +
    current_support:current_stability +
    (1 + time | context_id/child_id),
  data = panel
)

internalizing_model <- lmer(
  internalizing_score ~ time + current_risk + cumulative_risk +
    current_support + current_stability + community_support +
    school_belonging + service_access + biological_sensitivity +
    (1 + time | context_id/child_id),
  data = panel
)

externalizing_model <- lmer(
  externalizing_score ~ time + current_risk + cumulative_risk +
    current_support + current_stability + current_regulation +
    community_support + school_belonging + service_access +
    biological_sensitivity + (1 + time | context_id/child_id),
  data = panel
)

capture.output(
  list(
    adaptation_model = summary(mixed_model),
    internalizing_model = summary(internalizing_model),
    externalizing_model = summary(externalizing_model)
  ),
  file = file.path(outputs_dir, "r_psychopathology_model_summary.txt")
)

trajectory <- panel |>
  group_by(time) |>
  summarize(
    average_adaptation = mean(adaptation_score),
    average_internalizing = mean(internalizing_score),
    average_externalizing = mean(externalizing_score),
    standard_error = sd(adaptation_score) / sqrt(n()),
    lower = average_adaptation - 1.96 * standard_error,
    upper = average_adaptation + 1.96 * standard_error,
    .groups = "drop"
  )

write.csv(trajectory, file.path(outputs_dir, "r_adaptation_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_adaptation_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_adaptation)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper), alpha = 0.15) +
    labs(title = "Synthetic Developmental Psychopathology Trajectories", x = "Time", y = "Average adaptation") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

ggsave(
  filename = file.path(outputs_dir, "r_multifinality_pathways.png"),
  plot = ggplot(trajectory, aes(x = time)) +
    geom_line(aes(y = average_internalizing, linetype = "internalizing"), linewidth = 1) +
    geom_line(aes(y = average_externalizing, linetype = "externalizing"), linewidth = 1) +
    labs(title = "Synthetic Multifinality Pathways", x = "Time", y = "Average pathway score", linetype = "Pathway") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R outputs.")
