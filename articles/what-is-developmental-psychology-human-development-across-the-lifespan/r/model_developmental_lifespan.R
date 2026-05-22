#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
script_path <- normalizePath(sub("--file=", "", args[grep("--file=", args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
data_path <- file.path(root, "data", "developmental_lifespan_panel.csv")
outputs_dir <- file.path(root, "outputs")
if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)

panel <- read.csv(data_path)

model <- lmer(
  development_score ~ time + caregiver_support + family_support +
    school_support + school_climate + disability_support_need +
    disability_accommodation + counseling_access + language_access +
    community_resource_index + structural_risk + acute_stress +
    current_support + intervention + protective_context +
    (1 + time | school_id/child_id),
  data = panel
)

capture.output(summary(model), file = file.path(outputs_dir, "r_developmental_lifespan_model_summary.txt"))

trajectory <- panel |>
  group_by(time, structural_risk) |>
  summarize(
    average_development = mean(development_score),
    average_support = mean(current_support),
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
    labs(
      title = "Synthetic Developmental Trajectories by Structural Risk",
      x = "Time",
      y = "Average development score",
      linetype = "Group"
    ) +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

support_summary <- panel |>
  group_by(time) |>
  summarize(
    average_support = mean(current_support),
    average_stress = mean(acute_stress),
    average_intervention = mean(intervention),
    average_protective_context = mean(protective_context),
    average_development = mean(development_score),
    .groups = "drop"
  )

write.csv(support_summary, file.path(outputs_dir, "r_support_context_trajectory.csv"), row.names = FALSE)

message("Wrote R developmental lifespan outputs.")
