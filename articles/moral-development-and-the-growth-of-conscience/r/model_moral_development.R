#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
script_path <- normalizePath(sub("--file=", "", args[grep("--file=", args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
data_path <- file.path(root, "data", "moral_development_panel.csv")
outputs_dir <- file.path(root, "outputs")
if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)

panel <- read.csv(data_path)

model <- lmer(
  conscience_score ~ time + current_guidance + current_empathy +
    current_peer_fairness + current_self_regulation +
    current_harm_recognition + current_repair_opportunity +
    school_moral_climate + restorative_practice_access +
    punitive_inconsistency + anti_bullying_climate +
    digital_moral_safety + current_exclusion + digital_cruelty_exposure +
    chronic_exclusion + moral_support_context +
    (1 + time | school_id/child_id),
  data = panel
)

capture.output(summary(model), file = file.path(outputs_dir, "r_moral_development_model_summary.txt"))

trajectory <- panel |>
  group_by(time, chronic_exclusion) |>
  summarize(
    average_conscience = mean(conscience_score),
    average_moral_action = mean(moral_action_score),
    average_moral_context = mean(moral_support_context),
    average_exclusion = mean(current_exclusion),
    average_peer_pressure = mean(peer_pressure),
    standard_error = sd(conscience_score) / sqrt(n()),
    .groups = "drop"
  ) |>
  mutate(
    exclusion_group = ifelse(chronic_exclusion == 1, "Higher exclusion risk", "Lower exclusion risk")
  )

write.csv(trajectory, file.path(outputs_dir, "r_exclusion_conscience_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_exclusion_conscience_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_conscience, linetype = exclusion_group)) +
    geom_line(linewidth = 1) +
    labs(
      title = "Synthetic Moral Development and Growth of Conscience",
      x = "Time",
      y = "Average conscience score",
      linetype = "Group"
    ) +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R moral development outputs.")
