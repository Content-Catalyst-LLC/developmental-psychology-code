#!/usr/bin/env python3
"""Model synthetic developmental trajectories.

This script estimates a dynamic developmental model and writes reproducible
outputs. It assumes data/developmental_panel.csv already exists.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "developmental_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing {DATA_PATH}. Run python/generate_developmental_panel.py first."
        )

    panel = pd.read_csv(DATA_PATH)
    panel = panel.sort_values(["person_id", "time"]).reset_index(drop=True)
    panel["lag_development_score"] = panel.groupby("person_id")[
        "development_score"
    ].shift(1)

    model_data = panel.dropna(subset=["lag_development_score"]).copy()

    model = smf.ols(
        formula="""
        development_score ~ lag_development_score + time + current_support +
        current_risk + policy_access + health_status +
        institutional_climate + resource_level + person_resilience
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_model_summary.txt", "w", encoding="utf-8") as f:
        f.write(model.summary().as_text())

    trajectory = panel.groupby("time", as_index=False).agg(
        average_development=("development_score", "mean"),
        standard_error=("development_score", lambda x: x.std() / (len(x) ** 0.5)),
        average_support=("current_support", "mean"),
        average_risk=("current_risk", "mean"),
        average_policy_access=("policy_access", "mean"),
    )
    trajectory["lower"] = (
        trajectory["average_development"] - 1.96 * trajectory["standard_error"]
    )
    trajectory["upper"] = (
        trajectory["average_development"] + 1.96 * trajectory["standard_error"]
    )

    trajectory.to_csv(OUTPUTS_DIR / "python_developmental_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(trajectory["time"], trajectory["average_development"], linewidth=2)
    plt.fill_between(
        trajectory["time"],
        trajectory["lower"],
        trajectory["upper"],
        alpha=0.2,
    )
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Developmental Trajectories Across Time")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_average_trajectory.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_model_summary.txt")
    print("Wrote outputs/python_developmental_trajectory.csv")
    print("Wrote outputs/python_average_trajectory.png")


if __name__ == "__main__":
    main()
