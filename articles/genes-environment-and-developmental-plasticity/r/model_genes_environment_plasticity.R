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

data_path <- file.path(root, "data", "genes_environment_plasticity_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_genes_environment_panel.py first.")

panel <- read.csv(data_path)

development_model <- lmer(
  development_score ~ time + bio_sensitivity + current_care +
    current_stress + current_nutrition + school_support +
    neighborhood_safety + service_access + early_exposure +
    timing_weight + embedded_stress + embedded_support +
    intervention_support + bio_sensitivity:current_care +
    bio_sensitivity:current_stress +
    (1 + time | context_id/child_id),
  data = panel
)

embedding_model <- lmer(
  embedded_stress ~ time + current_stress + current_care +
    current_nutrition + school_support + neighborhood_safety +
    service_access + bio_sensitivity + intervention_support +
    (1 + time | context_id/child_id),
  data = panel
)

capture.output(
  list(
    development_model = summary(development_model),
    embedding_model = summary(embedding_model)
  ),
  file = file.path(outputs_dir, "r_plasticity_model_summary.txt")
)

trajectory <- panel |>
  group_by(time, early_exposure) |>
  summarize(
    average_development = mean(development_score),
    standard_error = sd(development_score) / sqrt(n()),
    lower = average_development - 1.96 * standard_error,
    upper = average_development + 1.96 * standard_error,
    .groups = "drop"
  ) |>
  mutate(group = ifelse(early_exposure == 1, "Early exposure", "No early exposure"))

write.csv(trajectory, file.path(outputs_dir, "r_development_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_development_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_development, linetype = group)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper, group = group), alpha = 0.12) +
    labs(title = "Synthetic Genes, Environment, and Developmental Plasticity", x = "Time", y = "Average development", linetype = "Group") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

embedded <- panel |>
  group_by(time) |>
  summarize(
    average_embedded_stress = mean(embedded_stress),
    average_embedded_support = mean(embedded_support),
    average_care = mean(current_care),
    average_stress = mean(current_stress),
    .groups = "drop"
  )

write.csv(embedded, file.path(outputs_dir, "r_embedded_exposure_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_embedded_exposure_trajectory.png"),
  plot = ggplot(embedded, aes(x = time)) +
    geom_line(aes(y = average_embedded_stress, linetype = "embedded stress"), linewidth = 1) +
    geom_line(aes(y = average_embedded_support, linetype = "embedded support"), linewidth = 1) +
    labs(title = "Synthetic Embedded Stress and Support", x = "Time", y = "Average embedded exposure", linetype = "Exposure") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R plasticity outputs.")
