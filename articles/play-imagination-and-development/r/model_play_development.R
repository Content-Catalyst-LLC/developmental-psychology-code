#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
script_path <- normalizePath(sub("--file=", "", args[grep("--file=", args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
data_path <- file.path(root, "data", "play_development_panel.csv")
outputs_dir <- file.path(root, "outputs")
if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)

panel <- read.csv(data_path)

model <- lmer(
  development_score ~ time + current_pretend + current_social_play +
    current_constructive + current_outdoor + current_support +
    current_stress + chronic_stress + play_restriction +
    peer_inclusion + play_space_quality + adult_responsiveness +
    inclusion_climate + outdoor_safety + play_material_access +
    play_support_context +
    (1 + time | context_id/child_id),
  data = panel
)

capture.output(summary(model), file = file.path(outputs_dir, "r_play_development_model_summary.txt"))

trajectory <- panel |>
  group_by(time, chronic_stress) |>
  summarize(
    average_development = mean(development_score),
    average_pretend = mean(current_pretend),
    average_social_play = mean(current_social_play),
    average_constructive = mean(current_constructive),
    average_outdoor = mean(current_outdoor),
    average_stress = mean(current_stress),
    average_restriction = mean(play_restriction),
    average_peer_inclusion = mean(peer_inclusion),
    standard_error = sd(development_score) / sqrt(n()),
    .groups = "drop"
  ) |>
  mutate(
    stress_group = ifelse(chronic_stress == 1, "Higher chronic stress", "Lower chronic stress")
  )

write.csv(trajectory, file.path(outputs_dir, "r_stress_play_development_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_stress_play_development_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_development, linetype = stress_group)) +
    geom_line(linewidth = 1) +
    labs(
      title = "Synthetic Play, Imagination, and Development Across Time",
      x = "Time",
      y = "Average development score",
      linetype = "Group"
    ) +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R play development outputs.")
