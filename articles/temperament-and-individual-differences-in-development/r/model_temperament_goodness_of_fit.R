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

data_path <- file.path(root, "data", "temperament_individual_differences_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_temperament_panel.py first.")

panel <- read.csv(data_path)

temperament_model <- lmer(
  adjustment_score ~ time + temperament_reactivity + inhibition +
    activity_level + current_support + goodness_of_fit +
    acute_stress + chronic_stress + teacher_responsiveness +
    temperament_reactivity:current_support +
    temperament_reactivity:goodness_of_fit +
    temperament_reactivity:acute_stress +
    (1 + time | classroom_id/child_id),
  data = panel
)

fit_model <- lmer(
  goodness_of_fit ~ current_school_fit + teacher_responsiveness +
    movement_flexibility + current_accommodation + classroom_structure +
    temperament_reactivity + inhibition + activity_level +
    current_support + acute_stress +
    (1 | classroom_id),
  data = panel
)

capture.output(
  list(
    temperament_model = summary(temperament_model),
    goodness_of_fit_model = summary(fit_model)
  ),
  file = file.path(outputs_dir, "r_temperament_model_summary.txt")
)

panel <- panel |>
  mutate(reactivity_group = ntile(temperament_reactivity, 3))

trajectory <- panel |>
  group_by(time, reactivity_group) |>
  summarize(
    average_adjustment = mean(adjustment_score),
    average_fit = mean(goodness_of_fit),
    standard_error = sd(adjustment_score) / sqrt(n()),
    lower = average_adjustment - 1.96 * standard_error,
    upper = average_adjustment + 1.96 * standard_error,
    .groups = "drop"
  ) |>
  mutate(group = case_when(
    reactivity_group == 1 ~ "Lower reactivity",
    reactivity_group == 2 ~ "Moderate reactivity",
    TRUE ~ "Higher reactivity"
  ))

write.csv(trajectory, file.path(outputs_dir, "r_temperament_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_temperament_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_adjustment, linetype = group)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper, group = group), alpha = 0.12) +
    labs(title = "Synthetic Temperament and Developmental Adjustment", x = "Time", y = "Average adjustment", linetype = "Reactivity group") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

fit <- panel |>
  group_by(time) |>
  summarize(
    average_fit = mean(goodness_of_fit),
    average_support = mean(current_support),
    average_stress = mean(acute_stress),
    average_accommodation = mean(current_accommodation),
    average_adjustment = mean(adjustment_score),
    .groups = "drop"
  )

write.csv(fit, file.path(outputs_dir, "r_goodness_of_fit_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_goodness_of_fit_trajectory.png"),
  plot = ggplot(fit, aes(x = time)) +
    geom_line(aes(y = average_fit, linetype = "goodness of fit"), linewidth = 1) +
    geom_line(aes(y = average_support, linetype = "support"), linewidth = 1) +
    geom_line(aes(y = average_stress, linetype = "stress"), linewidth = 1) +
    geom_line(aes(y = average_accommodation, linetype = "accommodation"), linewidth = 1) +
    labs(title = "Synthetic Goodness of Fit, Support, Stress, and Accommodation", x = "Time", y = "Average index", linetype = "Measure") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R temperament outputs.")
