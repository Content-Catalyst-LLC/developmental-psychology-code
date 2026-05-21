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

data_path <- file.path(root, "data", "gender_sexual_development_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_gender_sexual_development_panel.py first.")

panel <- read.csv(data_path)

model <- lmer(
  adjustment_score ~ pubertal_progress + current_family_support +
    current_recognition + current_consent_knowledge +
    current_connectedness + school_climate +
    health_education_quality + anti_harassment_support +
    current_stigma + chronic_stigma +
    current_stigma:protective_context +
    (1 + pubertal_progress | school_id/id),
  data = panel
)

capture.output(
  summary(model),
  file = file.path(outputs_dir, "r_gender_sexual_development_model_summary.txt")
)

trajectory <- panel |>
  group_by(time, chronic_stigma) |>
  summarize(
    average_adjustment = mean(adjustment_score),
    average_protective_context = mean(protective_context),
    average_stigma = mean(current_stigma),
    standard_error = sd(adjustment_score) / sqrt(n()),
    .groups = "drop"
  ) |>
  mutate(
    lower = average_adjustment - 1.96 * standard_error,
    upper = average_adjustment + 1.96 * standard_error,
    group_label = ifelse(chronic_stigma == 1, "Higher stigma risk", "Lower stigma risk")
  )

write.csv(trajectory, file.path(outputs_dir, "r_stigma_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_stigma_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_adjustment, linetype = group_label)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper, group = group_label), alpha = 0.12) +
    labs(title = "Synthetic Gender Development, Sexual Development, and Adjustment", x = "Time", y = "Average adjustment", linetype = "Group") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

support_summary <- panel |>
  group_by(time) |>
  summarize(
    average_family_support = mean(current_family_support),
    average_recognition = mean(current_recognition),
    average_consent_knowledge = mean(current_consent_knowledge),
    average_connectedness = mean(current_connectedness),
    average_stigma = mean(current_stigma),
    average_protective_context = mean(protective_context),
    average_adjustment = mean(adjustment_score),
    .groups = "drop"
  )

write.csv(support_summary, file.path(outputs_dir, "r_protective_context_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_protective_context_trajectory.png"),
  plot = ggplot(support_summary, aes(x = time)) +
    geom_line(aes(y = average_family_support, linetype = "family support"), linewidth = 1) +
    geom_line(aes(y = average_recognition, linetype = "recognition"), linewidth = 1) +
    geom_line(aes(y = average_consent_knowledge, linetype = "consent knowledge"), linewidth = 1) +
    geom_line(aes(y = average_connectedness, linetype = "connectedness"), linewidth = 1) +
    geom_line(aes(y = average_stigma, linetype = "stigma"), linewidth = 1) +
    labs(title = "Synthetic Protective Context and Stigma Over Time", x = "Time", y = "Average index", linetype = "Measure") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R gender/sexual development outputs.")
