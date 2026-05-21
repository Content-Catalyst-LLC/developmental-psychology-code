#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(tidyr)
})

args <- commandArgs(trailingOnly = FALSE)
script_path <- normalizePath(sub("--file=", "", args[grep("--file=", args)]))
root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
data_path <- file.path(root, "data", "developmental_psychology_history_panel.csv")
outputs_dir <- file.path(root, "outputs")
if (!dir.exists(outputs_dir)) dir.create(outputs_dir, recursive = TRUE)

df <- read.csv(data_path)

paradigm_cols <- c(
  "child_study",
  "maturational",
  "psychoanalytic",
  "behaviorist",
  "cognitive_developmental",
  "sociocultural",
  "attachment_social",
  "ecological",
  "lifespan",
  "developmental_psychopathology",
  "neuroscience_genetics",
  "developmental_systems"
)

selected <- df |>
  filter(year %in% c(1900, 1930, 1950, 1975, 2000, 2025))

write.csv(selected, file.path(outputs_dir, "r_selected_historical_years.csv"), row.names = FALSE)

plot_df <- df |>
  select(year, all_of(paradigm_cols)) |>
  pivot_longer(cols = -year, names_to = "paradigm", values_to = "share")

ggsave(
  filename = file.path(outputs_dir, "r_paradigm_history.png"),
  plot = ggplot(plot_df, aes(x = year, y = share, linetype = paradigm)) +
    geom_line(linewidth = 1) +
    labs(
      title = "Simulated Intellectual History of Developmental Psychology",
      x = "Year",
      y = "Synthetic relative prominence",
      linetype = "Paradigm"
    ) +
    theme_minimal(),
  width = 10,
  height = 6,
  dpi = 160
)

index_df <- df |>
  select(year, child_centered_index, lifespan_index, ecological_systems_index, broadening_index) |>
  pivot_longer(cols = -year, names_to = "index", values_to = "value")

ggsave(
  filename = file.path(outputs_dir, "r_broadening_indexes.png"),
  plot = ggplot(index_df, aes(x = year, y = value, linetype = index)) +
    geom_line(linewidth = 1) +
    labs(
      title = "Historical Broadening Indexes in Developmental Psychology",
      x = "Year",
      y = "Synthetic index",
      linetype = "Index"
    ) +
    theme_minimal(),
  width = 8,
  height = 5,
  dpi = 160
)

peak_summary <- data.frame(
  paradigm = paradigm_cols,
  peak_year = sapply(paradigm_cols, function(col) df$year[which.max(df[[col]])]),
  peak_share = sapply(paradigm_cols, function(col) max(df[[col]]))
)

write.csv(peak_summary, file.path(outputs_dir, "r_paradigm_peak_summary.csv"), row.names = FALSE)
capture.output(summary(df), file = file.path(outputs_dir, "r_history_panel_summary.txt"))

message("Wrote R developmental history outputs.")
