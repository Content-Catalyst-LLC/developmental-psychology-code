#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
script_path <- normalizePath(sub("--file=", "", args[grep("--file=", args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
data_path <- file.path(root, "data", "adolescence_identity_panel.csv")
outputs_dir <- file.path(root, "outputs")
if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)

panel <- read.csv(data_path)

model <- lmer(
  identity_score ~ time + current_peer_support + current_family_support +
    current_connectedness + current_future_orientation + school_climate +
    counseling_access + extracurricular_access + identity_safety + digital_safety +
    current_exclusion + digital_stress + chronic_exclusion +
    (1 + time | school_id/adolescent_id),
  data = panel
)

capture.output(summary(model), file = file.path(outputs_dir, "r_adolescence_identity_model_summary.txt"))

trajectory <- panel |>
  group_by(time, chronic_exclusion) |>
  summarize(
    average_identity = mean(identity_score),
    average_support_context = mean(support_context),
    average_exclusion = mean(current_exclusion),
    average_digital_stress = mean(digital_stress),
    standard_error = sd(identity_score) / sqrt(n()),
    .groups = "drop"
  ) |>
  mutate(
    lower = average_identity - 1.96 * standard_error,
    upper = average_identity + 1.96 * standard_error,
    group_label = ifelse(chronic_exclusion == 1, "Higher exclusion risk", "Lower exclusion risk")
  )

write.csv(trajectory, file.path(outputs_dir, "r_exclusion_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_exclusion_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_identity, linetype = group_label)) +
    geom_line(linewidth = 1) +
    labs(title = "Synthetic Adolescence, Identity, and Psychological Transition", x = "Time", y = "Average identity score", linetype = "Group") +
    theme_minimal(),
  width = 8, height = 5, dpi = 160
)

message("Wrote R adolescence identity outputs.")
