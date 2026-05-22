#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(lme4)
})

args <- commandArgs(trailingOnly = FALSE)
script_path <- normalizePath(sub("--file=", "", args[grep("--file=", args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
data_path <- file.path(root, "data", "attachment_development_panel.csv")
outputs_dir <- file.path(root, "outputs")
if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)

panel <- read.csv(data_path)

model <- lmer(
  regulation_score ~ time + current_care + current_repair +
    current_caregiver_support + current_stress + chronic_stress +
    temperament_reactivity + disability_support_need +
    childcare_continuity + neighborhood_safety +
    family_service_access + caregiving_ecology_support +
    temperament_reactivity:current_stress +
    temperament_reactivity:current_care +
    disability_support_need:family_service_access +
    caregiving_support_context +
    (1 + time | context_id/child_id),
  data = panel
)

capture.output(summary(model), file = file.path(outputs_dir, "r_attachment_development_model_summary.txt"))

trajectory <- panel |>
  group_by(time, chronic_stress) |>
  summarize(
    average_regulation = mean(regulation_score),
    average_care = mean(current_care),
    average_repair = mean(current_repair),
    average_caregiver_support = mean(current_caregiver_support),
    average_stress = mean(current_stress),
    average_support_context = mean(caregiving_support_context),
    standard_error = sd(regulation_score) / sqrt(n()),
    .groups = "drop"
  ) |>
  mutate(
    stress_group = ifelse(chronic_stress == 1, "Higher chronic stress", "Lower chronic stress")
  )

write.csv(trajectory, file.path(outputs_dir, "r_stress_attachment_trajectory.csv"), row.names = FALSE)

ggsave(
  filename = file.path(outputs_dir, "r_stress_attachment_trajectory.png"),
  plot = ggplot(trajectory, aes(x = time, y = average_regulation, linetype = stress_group)) +
    geom_line(linewidth = 1) +
    labs(
      title = "Synthetic Attachment, Caregiving, and Early Emotional Development",
      x = "Time",
      y = "Average regulation score",
      linetype = "Group"
    ) +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

message("Wrote R attachment development outputs.")
