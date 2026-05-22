#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
script_path <- normalizePath(sub("--file=", "", args[grep("--file=", args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
data_path <- file.path(root, "data", "social_development_panel.csv")
outputs_dir <- file.path(root, "outputs")
if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)

panel <- read.csv(data_path)

model <- lmer(
  social_self_score ~ time + current_peer_support +
    current_friendship_quality + current_family_support +
    current_social_interpretation + school_connectedness +
    teacher_support + anti_bullying_climate + inclusion_climate +
    restorative_practice_access + current_exclusion +
    bullying_exposure + digital_comparison_stress +
    chronic_exclusion + social_support_context +
    (1 + time | school_id/child_id),
  data = panel
)

capture.output(summary(model), file = file.path(outputs_dir, "r_social_development_model_summary.txt"))

trajectory <- panel |>
  group_by(time, chronic_exclusion) |>
  summarize(
    average_social_self = mean(social_self_score),
    average_social_context = mean(social_support_context),
    average_exclusion = mean(current_exclusion),
    average_bullying = mean(bullying_exposure),
    average_digital_comparison = mean(digital_comparison_stress),
    standard_error = sd(social_self_score) / sqrt(n()),
    .groups = "drop"
  ) |>
  mutate(
    exclusion_group = ifelse(chronic_exclusion == 1, "Higher exclusion risk", "Lower exclusion risk")
  )

write.csv(trajectory, file.path(outputs_dir, "r_exclusion_social_self_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_exclusion_social_self_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_social_self, linetype = exclusion_group)) +
    geom_line(linewidth = 1) +
    labs(
      title = "Synthetic Social Development and Self Formation",
      x = "Time",
      y = "Average social-self score",
      linetype = "Group"
    ) +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R social development outputs.")
