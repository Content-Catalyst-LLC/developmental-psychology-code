# Synthetic developmental psychology analysis.
# Run after the Python script creates data/processed/synthetic_lifespan_observations.csv.

data_path <- file.path("data", "processed", "synthetic_lifespan_observations.csv")

if (!file.exists(data_path)) {
  stop("Run: python3 python/developmental_lifespan_simulation.py")
}

dat <- read.csv(data_path)

summary_table <- aggregate(
  cbind(developmental_functioning, self_regulation, resilience_support, cumulative_risk) ~ wave,
  data = dat,
  FUN = mean
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(summary_table, file.path("outputs", "lifespan_wave_summary.csv"), row.names = FALSE)

model <- lm(
  developmental_functioning ~ caregiving_support + educational_opportunity +
    self_regulation + resilience_support - cumulative_risk,
  data = dat
)

print(summary(model))
print(summary_table)
