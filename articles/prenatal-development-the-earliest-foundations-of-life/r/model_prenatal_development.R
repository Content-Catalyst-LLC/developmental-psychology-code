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

data_path <- file.path(root, "data", "prenatal_development_foundations_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_prenatal_development_panel.py first.")

prenatal <- read.csv(data_path)

model <- lmer(
  early_outcome ~ gestational_weeks + maternal_health + effective_care +
    nutrition_support + social_support + chronic_stress + toxic_exposure +
    environmental_burden + economic_security +
    maternal_health:effective_care +
    maternal_health:chronic_stress +
    developmental_risk:effective_care +
    (1 | neighborhood_context),
  data = prenatal
)

capture.output(
  summary(model),
  file = file.path(outputs_dir, "r_prenatal_development_model_summary.txt")
)

stress_summary <- prenatal |>
  mutate(stress_group = ntile(chronic_stress, 4)) |>
  group_by(stress_group) |>
  summarize(
    average_outcome = mean(early_outcome),
    average_care = mean(effective_care),
    average_risk = mean(developmental_risk),
    standard_error = sd(early_outcome) / sqrt(n()),
    lower = average_outcome - 1.96 * standard_error,
    upper = average_outcome + 1.96 * standard_error,
    .groups = "drop"
  ) |>
  mutate(group = case_when(
    stress_group == 1 ~ "Lowest stress",
    stress_group == 2 ~ "Moderate-low stress",
    stress_group == 3 ~ "Moderate-high stress",
    TRUE ~ "Highest stress"
  ))

write.csv(stress_summary, file.path(outputs_dir, "r_prenatal_stress_summary.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_prenatal_stress_summary.png"),
  plot = ggplot(stress_summary, aes(x = group, y = average_outcome, group = 1)) +
    geom_line(linewidth = 1) +
    geom_point(size = 2) +
    geom_errorbar(aes(ymin = lower, ymax = upper), width = 0.15) +
    labs(title = "Synthetic Prenatal Stress and Early Developmental Outcome", x = "Prenatal stress group", y = "Average early outcome") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

care_summary <- prenatal |>
  mutate(care_group = ntile(effective_care, 4)) |>
  group_by(care_group) |>
  summarize(
    average_outcome = mean(early_outcome),
    average_risk = mean(developmental_risk),
    average_gestation = mean(gestational_weeks),
    average_maternal_health = mean(maternal_health),
    .groups = "drop"
  )

write.csv(care_summary, file.path(outputs_dir, "r_effective_care_summary.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_effective_care_summary.png"),
  plot = ggplot(care_summary, aes(x = care_group, y = average_outcome)) +
    geom_line(linewidth = 1) +
    geom_point(size = 2) +
    labs(title = "Synthetic Effective Prenatal Care and Early Outcome", x = "Effective care quartile", y = "Average early outcome") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R prenatal development outputs.")
