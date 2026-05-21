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

data_path <- file.path(root, "data", "wisdom_meaning_later_life_panel.csv")
outputs_dir <- file.path(root, "outputs")

if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)
if (!file.exists(data_path)) stop("Run python/generate_wisdom_meaning_panel.py first.")

panel <- read.csv(data_path)

meaning_model <- lmer(
  meaning_score ~ time + current_connection + current_reflection +
    current_support + current_legacy + current_health +
    dignity_support + service_access + community_participation +
    wisdom_index + (1 + time | care_context_id/id),
  data = panel
)

wisdom_model <- lmer(
  wisdom_index ~ time + current_connection + current_reflection +
    current_legacy + current_health + dignity_support +
    service_access + community_participation +
    (1 + time | care_context_id/id),
  data = panel
)

capture.output(
  list(
    meaning_model = summary(meaning_model),
    wisdom_model = summary(wisdom_model)
  ),
  file = file.path(outputs_dir, "r_wisdom_meaning_model_summary.txt")
)

panel <- panel |>
  mutate(connection_group = ntile(current_connection, 3))

trajectory <- panel |>
  group_by(time, connection_group) |>
  summarize(
    average_meaning = mean(meaning_score),
    average_wisdom = mean(wisdom_index),
    standard_error = sd(meaning_score) / sqrt(n()),
    lower = average_meaning - 1.96 * standard_error,
    upper = average_meaning + 1.96 * standard_error,
    .groups = "drop"
  ) |>
  mutate(group = case_when(
    connection_group == 1 ~ "Lower connection",
    connection_group == 2 ~ "Moderate connection",
    TRUE ~ "Higher connection"
  ))

write.csv(trajectory, file.path(outputs_dir, "r_meaning_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_meaning_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_meaning, linetype = group)) +
    geom_line(linewidth = 1) +
    geom_ribbon(aes(ymin = lower, ymax = upper, group = group), alpha = 0.12) +
    labs(title = "Synthetic Wisdom, Meaning, and Development in Later Life", x = "Time", y = "Average meaning", linetype = "Connection group") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

wisdom <- panel |>
  group_by(time) |>
  summarize(
    average_wisdom = mean(wisdom_index),
    average_connection = mean(current_connection),
    average_reflection = mean(current_reflection),
    average_health = mean(current_health),
    average_legacy = mean(current_legacy),
    .groups = "drop"
  )

write.csv(wisdom, file.path(outputs_dir, "r_wisdom_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_wisdom_trajectory.png"),
  plot = ggplot(wisdom, aes(x = time)) +
    geom_line(aes(y = average_wisdom, linetype = "wisdom index"), linewidth = 1) +
    geom_line(aes(y = average_connection, linetype = "connection"), linewidth = 1) +
    geom_line(aes(y = average_reflection, linetype = "reflection"), linewidth = 1) +
    labs(title = "Synthetic Wisdom, Reflection, and Connection", x = "Time", y = "Average index", linetype = "Measure") +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R wisdom and meaning outputs.")
