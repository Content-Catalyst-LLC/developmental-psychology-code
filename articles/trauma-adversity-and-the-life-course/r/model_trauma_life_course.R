#!/usr/bin/env Rscript

# Mixed-effects workflow for synthetic trauma/adversity life-course data.

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- normalizePath(sub(file_arg, "", args[grep(file_arg, args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)

data_path <- file.path(root, "data", "trauma_life_course_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) {
  dir.create(outputs_dir, recursive = TRUE)
}

if (!file.exists(data_path)) {
  stop("Missing data/trauma_life_course_panel.csv. Run python/generate_trauma_life_course.py first.")
}

panel <- read.csv(data_path)

mixed_model <- lmer(
  adaptation_score ~ time + cumulative_adversity + current_adversity +
    early_timing_weight + current_support + current_stability +
    transition_support + community_buffer + institutional_safety +
    service_access + current_health + child_resilience +
    current_support:current_stability +
    (1 + time | context_id/child_id),
  data = panel
)

profile_model <- lm(
  adaptation_score ~ time + adversity_support_profile +
    current_support + current_stability + community_buffer +
    institutional_safety + service_access,
  data = panel
)

capture.output(
  list(
    mixed_model = summary(mixed_model),
    profile_model = summary(profile_model)
  ),
  file = file.path(outputs_dir, "r_trauma_model_summary.txt")
)

trajectory <- panel |>
  group_by(time) |>
  summarize(
    average_adaptation = mean(adaptation_score),
    standard_error = sd(adaptation_score) / sqrt(n()),
    lower = average_adaptation - 1.96 * standard_error,
    upper = average_adaptation + 1.96 * standard_error,
    average_adversity = mean(current_adversity),
    average_support = mean(current_support),
    average_stability = mean(current_stability),
    .groups = "drop"
  )

write.csv(
  trajectory,
  file.path(outputs_dir, "r_adaptation_trajectory.csv"),
  row.names = FALSE
)

trajectory_plot <- ggplot(trajectory, aes(x = time, y = average_adaptation)) +
  geom_line(linewidth = 1) +
  geom_ribbon(aes(ymin = lower, ymax = upper), alpha = 0.15) +
  labs(
    title = "Synthetic Trauma, Adversity, and the Life Course",
    x = "Time",
    y = "Average adaptation score"
  ) +
  theme_minimal()

ggsave(
  filename = file.path(outputs_dir, "r_adaptation_trajectory.png"),
  plot = trajectory_plot,
  width = 8,
  height = 5,
  dpi = 160
)

profile_trajectory <- panel |>
  group_by(adversity_support_profile, time) |>
  summarize(
    average_adaptation = mean(adaptation_score),
    .groups = "drop"
  )

write.csv(
  profile_trajectory,
  file.path(outputs_dir, "r_profile_trajectories.csv"),
  row.names = FALSE
)

profile_plot <- ggplot(
  profile_trajectory,
  aes(x = time, y = average_adaptation, linetype = adversity_support_profile)
) +
  geom_line(linewidth = 1) +
  geom_point() +
  labs(
    title = "Synthetic Adaptation Trajectories by Adversity-Support Profile",
    x = "Time",
    y = "Average adaptation score",
    linetype = "Profile"
  ) +
  theme_minimal()

ggsave(
  filename = file.path(outputs_dir, "r_profile_trajectories.png"),
  plot = profile_plot,
  width = 9,
  height = 5.5,
  dpi = 160
)

message("Wrote outputs/r_trauma_model_summary.txt")
message("Wrote outputs/r_adaptation_trajectory.csv")
message("Wrote outputs/r_adaptation_trajectory.png")
message("Wrote outputs/r_profile_trajectories.csv")
message("Wrote outputs/r_profile_trajectories.png")
