#!/usr/bin/env Rscript

# Analyze synthetic developmental research designs in R.

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- normalizePath(sub(file_arg, "", args[grep(file_arg, args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)

data_path <- file.path(root, "data", "developmental_design_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) {
  dir.create(outputs_dir, recursive = TRUE)
}

if (!file.exists(data_path)) {
  stop("Missing data/developmental_design_panel.csv. Run python/generate_developmental_designs.py first.")
}

panel <- read.csv(data_path)
observed_panel <- panel |>
  filter(observed == 1)

cross_section <- observed_panel |>
  filter(period == min(period))

cross_sectional_model <- lm(
  development_score ~ age + I(age^2) + support + risk + context_quality,
  data = cross_section
)

longitudinal_model <- lm(
  development_score ~ age + I(age^2) + support + risk +
    baseline_trait + context_quality,
  data = observed_panel
)

cohort_aware_model <- lm(
  development_score ~ age + I(age^2) + factor(birth_cohort) +
    factor(period) + support + risk + baseline_trait + context_quality,
  data = observed_panel
)

mixed_growth_model <- lmer(
  development_score ~ age + I(age^2) + factor(birth_cohort) +
    support + risk + baseline_trait + context_quality +
    (1 + age | person_id) + (1 | context_id),
  data = observed_panel
)

capture.output(
  list(
    cross_sectional_model = summary(cross_sectional_model),
    longitudinal_model = summary(longitudinal_model),
    cohort_aware_model = summary(cohort_aware_model),
    mixed_growth_model = summary(mixed_growth_model)
  ),
  file = file.path(outputs_dir, "r_design_model_summary.txt")
)

trajectory <- observed_panel |>
  group_by(birth_cohort, age) |>
  summarize(
    mean_development_score = mean(development_score),
    people = n_distinct(person_id),
    .groups = "drop"
  )

write.csv(
  trajectory,
  file.path(outputs_dir, "r_growth_trajectory.csv"),
  row.names = FALSE
)

missingness <- panel |>
  group_by(study_wave) |>
  summarize(
    observation_rate = mean(observed),
    observations = sum(observed),
    possible_observations = n(),
    .groups = "drop"
  )

write.csv(
  missingness,
  file.path(outputs_dir, "r_missingness_by_wave.csv"),
  row.names = FALSE
)

design_plot <- ggplot(
  trajectory,
  aes(x = age, y = mean_development_score, linetype = factor(birth_cohort))
) +
  geom_line(linewidth = 1) +
  geom_point() +
  labs(
    title = "Synthetic Cohort-Sequential Developmental Trajectories",
    x = "Age",
    y = "Average development score",
    linetype = "Birth cohort"
  ) +
  theme_minimal()

ggsave(
  filename = file.path(outputs_dir, "r_design_comparison.png"),
  plot = design_plot,
  width = 9,
  height = 5.5,
  dpi = 160
)

missingness_plot <- ggplot(missingness, aes(x = study_wave, y = observation_rate)) +
  geom_line(linewidth = 1) +
  geom_point() +
  labs(
    title = "Synthetic Observation Rate by Study Wave",
    x = "Study wave",
    y = "Observation rate"
  ) +
  theme_minimal()

ggsave(
  filename = file.path(outputs_dir, "r_missingness_by_wave.png"),
  plot = missingness_plot,
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote outputs/r_design_model_summary.txt")
message("Wrote outputs/r_growth_trajectory.csv")
message("Wrote outputs/r_design_comparison.png")
message("Wrote outputs/r_missingness_by_wave.csv")
message("Wrote outputs/r_missingness_by_wave.png")
