#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
script_path <- normalizePath(sub("--file=", "", args[grep("--file=", args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
data_path <- file.path(root, "data", "puberty_embodiment_panel.csv")
outputs_dir <- file.path(root, "outputs")
if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)

panel <- read.csv(data_path)

model <- lmer(
  adjustment_score ~ pubertal_progress + timing_deviation +
    current_family_support + current_peer_comparison +
    current_body_concern + current_stigma + digital_visibility_stress +
    chronic_stigma + school_support + health_education_quality +
    privacy_protection + menstrual_support + disability_accommodation +
    anti_harassment_climate + digital_safety + protective_context +
    (1 + pubertal_progress | school_id/adolescent_id),
  data = panel
)

capture.output(summary(model), file = file.path(outputs_dir, "r_puberty_embodiment_model_summary.txt"))

trajectory <- panel |>
  group_by(time, chronic_stigma) |>
  summarize(
    average_adjustment = mean(adjustment_score),
    average_protective_context = mean(protective_context),
    average_peer_comparison = mean(current_peer_comparison),
    average_stigma = mean(current_stigma),
    average_body_concern = mean(current_body_concern),
    standard_error = sd(adjustment_score) / sqrt(n()),
    .groups = "drop"
  ) |>
  mutate(group_label = ifelse(chronic_stigma == 1, "Higher stigma risk", "Lower stigma risk"))

write.csv(trajectory, file.path(outputs_dir, "r_stigma_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_stigma_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_adjustment, linetype = group_label)) +
    geom_line(linewidth = 1) +
    labs(title = "Synthetic Puberty, Embodiment, and Adolescent Transition", x = "Time", y = "Average adjustment score", linetype = "Group") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R puberty embodiment outputs.")
