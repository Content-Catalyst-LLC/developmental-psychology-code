#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
script_path <- normalizePath(sub("--file=", "", args[grep("--file=", args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
data_path <- file.path(root, "data", "language_development_panel.csv")
outputs_dir <- file.path(root, "outputs")
if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)

panel <- read.csv(data_path)

model <- lmer(
  language_score ~ time + I(time^2) + current_interaction +
    current_reading + current_joint_attention + current_turn_taking +
    hearing_support + multilingual_exposure + current_stress +
    chronic_stress + language_ecology_support + book_access +
    early_education_quality + home_language_recognition +
    multilingual_exposure:home_language_recognition +
    language_support_context +
    (1 + time | context_id/child_id),
  data = panel
)

capture.output(summary(model), file = file.path(outputs_dir, "r_language_development_model_summary.txt"))

trajectory <- panel |>
  group_by(time, chronic_stress) |>
  summarize(
    average_language = mean(language_score),
    average_interaction = mean(current_interaction),
    average_reading = mean(current_reading),
    average_joint_attention = mean(current_joint_attention),
    average_turn_taking = mean(current_turn_taking),
    average_stress = mean(current_stress),
    average_language_support = mean(language_support_context),
    standard_error = sd(language_score) / sqrt(n()),
    .groups = "drop"
  ) |>
  mutate(
    stress_group = ifelse(chronic_stress == 1, "Higher chronic stress", "Lower chronic stress")
  )

write.csv(trajectory, file.path(outputs_dir, "r_stress_language_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_stress_language_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_language, linetype = stress_group)) +
    geom_line(linewidth = 1) +
    labs(
      title = "Synthetic Language Development Under Support and Stress",
      x = "Time",
      y = "Average language score",
      linetype = "Group"
    ) +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R language development outputs.")
