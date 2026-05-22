#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
script_path <- normalizePath(sub("--file=", "", args[grep("--file=", args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
data_path <- file.path(root, "data", "regulation_development_panel.csv")
outputs_dir <- file.path(root, "outputs")
if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)

panel <- read.csv(data_path)

model <- lmer(
  regulation_score ~ time + current_support + current_structure +
    current_sleep + school_climate + regulation_scaffolding +
    transition_predictability + disability_support_need +
    disability_accommodation + intervention_exposure +
    acute_stress + chronic_stress + temperament_reactivity +
    temperament_reactivity:current_support +
    temperament_reactivity:acute_stress +
    regulatory_support_context +
    (1 + time | school_id/child_id),
  data = panel
)

capture.output(summary(model), file = file.path(outputs_dir, "r_regulation_model_summary.txt"))

trajectory <- panel |>
  group_by(time, chronic_stress) |>
  summarize(
    average_regulation = mean(regulation_score),
    average_regulatory_context = mean(regulatory_support_context),
    average_support = mean(current_support),
    average_structure = mean(current_structure),
    average_sleep = mean(current_sleep),
    average_stress = mean(acute_stress),
    intervention_rate = mean(intervention_exposure),
    standard_error = sd(regulation_score) / sqrt(n()),
    .groups = "drop"
  ) |>
  mutate(
    stress_group = ifelse(chronic_stress == 1, "Higher chronic stress", "Lower chronic stress")
  )

write.csv(trajectory, file.path(outputs_dir, "r_stress_regulation_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_stress_regulation_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_regulation, linetype = stress_group)) +
    geom_line(linewidth = 1) +
    labs(
      title = "Synthetic Self-Regulation Across Development",
      x = "Time",
      y = "Average regulation score",
      linetype = "Group"
    ) +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R regulation outputs.")
