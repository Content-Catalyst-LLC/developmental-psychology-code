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

data_path <- file.path(root, "data", "lifespan_baltes_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_lifespan_baltes_panel.py first.")

panel <- read.csv(data_path)

development_model <- lmer(
  development_score ~ time + gains + losses + plasticity +
    current_support + current_comp + health_resource +
    historical_support + institutional_security + soc_index +
    plasticity:current_support + losses:compensation +
    (1 + time | cohort_id/id),
  data = panel
)

soc_model <- lmer(
  soc_index ~ time + selection + optimization + compensation +
    current_support + current_comp + health_resource +
    historical_support + institutional_security +
    (1 + time | cohort_id/id),
  data = panel
)

capture.output(
  list(
    development_model = summary(development_model),
    soc_model = summary(soc_model)
  ),
  file = file.path(outputs_dir, "r_lifespan_baltes_model_summary.txt")
)

trajectory <- panel |>
  group_by(time) |>
  summarize(
    average_development = mean(development_score),
    average_gains = mean(gains),
    average_losses = mean(losses),
    average_soc = mean(soc_index),
    standard_error = sd(development_score) / sqrt(n()),
    lower = average_development - 1.96 * standard_error,
    upper = average_development + 1.96 * standard_error,
    .groups = "drop"
  )

write.csv(trajectory, file.path(outputs_dir, "r_lifespan_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_lifespan_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_development)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper), alpha = 0.12) +
    labs(title = "Synthetic Lifespan Development in the Baltes Tradition", x = "Time", y = "Average development") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

soc <- panel |>
  group_by(time) |>
  summarize(
    average_selection = mean(selection),
    average_optimization = mean(optimization),
    average_compensation = mean(compensation),
    average_soc = mean(soc_index),
    .groups = "drop"
  )

write.csv(soc, file.path(outputs_dir, "r_soc_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_soc_trajectory.png"),
  plot = ggplot(soc, aes(x = time)) +
    geom_line(aes(y = average_selection, linetype = "selection"), linewidth = 1) +
    geom_line(aes(y = average_optimization, linetype = "optimization"), linewidth = 1) +
    geom_line(aes(y = average_compensation, linetype = "compensation"), linewidth = 1) +
    labs(title = "Synthetic Selection, Optimization, and Compensation", x = "Time", y = "Average SOC component", linetype = "Component") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R lifespan Baltes outputs.")
