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

data_path <- file.path(root, "data", "aging_adaptation_later_life_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_aging_adaptation_panel.py first.")

panel <- read.csv(data_path)

adjustment_model <- lmer(
  adjustment_score ~ time + functional_fit + current_support +
    current_adaptation + current_meaning + current_health +
    dignity_support + service_access +
    (1 + time | care_context_id/id),
  data = panel
)

fit_model <- lmer(
  functional_fit ~ time + current_function + environmental_accessibility +
    current_function:environmental_accessibility + current_support +
    dignity_support + service_access +
    (1 + time | care_context_id/id),
  data = panel
)

capture.output(
  list(
    adjustment_model = summary(adjustment_model),
    functional_fit_model = summary(fit_model)
  ),
  file = file.path(outputs_dir, "r_aging_adaptation_model_summary.txt")
)

panel <- panel |>
  mutate(health_group = ntile(current_health, 3))

trajectory <- panel |>
  group_by(time, health_group) |>
  summarize(
    average_adjustment = mean(adjustment_score),
    average_functional_fit = mean(functional_fit),
    standard_error = sd(adjustment_score) / sqrt(n()),
    lower = average_adjustment - 1.96 * standard_error,
    upper = average_adjustment + 1.96 * standard_error,
    .groups = "drop"
  ) |>
  mutate(group = case_when(
    health_group == 1 ~ "Lower burden",
    health_group == 2 ~ "Moderate burden",
    TRUE ~ "Higher burden"
  ))

write.csv(trajectory, file.path(outputs_dir, "r_adjustment_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_adjustment_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_adjustment, linetype = group)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper, group = group), alpha = 0.12) +
    labs(title = "Synthetic Aging, Adaptation, and Later-Life Development", x = "Time", y = "Average adjustment", linetype = "Health group") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

fit <- panel |>
  group_by(time) |>
  summarize(
    average_functional_fit = mean(functional_fit),
    average_function = mean(current_function),
    average_support = mean(current_support),
    average_health = mean(current_health),
    average_adaptation = mean(current_adaptation),
    .groups = "drop"
  )

write.csv(fit, file.path(outputs_dir, "r_functional_fit_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_functional_fit_trajectory.png"),
  plot = ggplot(fit, aes(x = time)) +
    geom_line(aes(y = average_functional_fit, linetype = "functional fit"), linewidth = 1) +
    geom_line(aes(y = average_support, linetype = "support"), linewidth = 1) +
    geom_line(aes(y = average_health, linetype = "health burden"), linewidth = 1) +
    labs(title = "Synthetic Functional Fit, Support, and Health Burden", x = "Time", y = "Average index", linetype = "Measure") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R aging adaptation outputs.")
