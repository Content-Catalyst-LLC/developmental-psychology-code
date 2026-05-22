#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
script_path <- normalizePath(sub("--file=", "", args[grep("--file=", args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
data_path <- file.path(root, "data", "brain_development_panel.csv")
outputs_dir <- file.path(root, "outputs")
if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)

panel <- read.csv(data_path)

model <- lmer(
  developmental_outcome ~ time + I(time^2) + neural_state +
    current_family_support + current_learning + current_sleep +
    current_sensory_support + school_support + neighborhood_safety +
    health_service_access + acute_stress + chronic_stress +
    environmental_risk + developmental_support_context +
    (1 + time | context_id/child_id),
  data = panel
)

capture.output(summary(model), file = file.path(outputs_dir, "r_brain_development_model_summary.txt"))

trajectory <- panel |>
  group_by(time, chronic_stress) |>
  summarize(
    average_developmental_outcome = mean(developmental_outcome),
    average_neural_state = mean(neural_state),
    average_stress = mean(acute_stress),
    average_support_context = mean(developmental_support_context),
    .groups = "drop"
  ) |>
  mutate(stress_group = ifelse(chronic_stress == 1, "Higher chronic stress", "Lower chronic stress"))

write.csv(trajectory, file.path(outputs_dir, "r_stress_neurodevelopment_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_stress_neurodevelopment_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_developmental_outcome, linetype = stress_group)) +
    geom_line(linewidth = 1) +
    labs(title = "Synthetic Brain Development Under Support and Adversity", x = "Time", y = "Average developmental outcome", linetype = "Group") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R brain development outputs.")
