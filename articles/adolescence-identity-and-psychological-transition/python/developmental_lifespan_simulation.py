"""Synthetic developmental psychology lifespan simulation.

This script creates toy longitudinal data for article examples.
It is educational only and not a clinical, diagnostic, or assessment tool.
"""

from pathlib import Path
import csv
import random

random.seed(42)

n_people = 180
n_waves = 12

rows = []
observation_id = 1

for person_index in range(1, n_people + 1):
    participant = f"P{person_index:03d}"
    birth_cohort = random.choice([1980, 1990, 2000, 2010])

    caregiving = random.uniform(0.2, 0.95)
    opportunity = random.uniform(0.2, 0.95)
    self_regulation = random.uniform(0.2, 0.85)
    resilience = random.uniform(0.2, 0.85)
    risk = random.uniform(0.05, 0.90)

    for wave in range(1, n_waves + 1):
        age_years = wave * 5 + random.uniform(-0.5, 0.5)

        developmental_functioning = (
            0.18 * caregiving +
            0.18 * opportunity +
            0.20 * self_regulation +
            0.16 * resilience -
            0.20 * risk +
            random.gauss(0.0, 0.05)
        )

        developmental_functioning = max(0.0, min(1.0, developmental_functioning))

        rows.append({
            "observation_id": observation_id,
            "participant": participant,
            "birth_cohort": birth_cohort,
            "wave": wave,
            "age_years": round(age_years, 2),
            "caregiving_support": round(caregiving, 3),
            "educational_opportunity": round(opportunity, 3),
            "self_regulation": round(self_regulation, 3),
            "resilience_support": round(resilience, 3),
            "cumulative_risk": round(risk, 3),
            "developmental_functioning": round(developmental_functioning, 3),
        })

        # Simple recursive developmental update.
        self_regulation = max(0.0, min(1.0, self_regulation + 0.03 * (developmental_functioning - 0.4)))
        resilience = max(0.0, min(1.0, resilience + 0.025 * (developmental_functioning - 0.4)))
        risk = max(0.0, min(1.0, risk - 0.015 * developmental_functioning + random.gauss(0.0, 0.01)))

        observation_id += 1

out = Path(__file__).resolve().parents[1] / "data" / "processed" / "synthetic_lifespan_observations.csv"
out.parent.mkdir(parents=True, exist_ok=True)

with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} synthetic developmental observations to {out}")
