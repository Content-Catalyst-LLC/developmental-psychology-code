#!/usr/bin/env python3
"""Model synthetic culture and development trajectories."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "cultural_development_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing {DATA_PATH}. Run python/generate_cultural_development_panel.py first."
        )

    panel = pd.read_csv(DATA_PATH)
    panel = panel.sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("child_id")["development_score"].shift(1)

    regression_data = panel.dropna(subset=["lag_score"]).copy()

    model = smf.ols(
        formula="""
        development_score ~ lag_score + time + current_family +
        current_fit + current_mismatch + current_support +
        current_flexibility + society_climate + institutional_inclusion +
        linguistic_support + pluralism_index + child_resilience
        """,
        data=regression_data,
    ).fit(cov_type="HC3")

    condition_model = smf.ols(
        formula="""
        development_score ~ time + C(cultural_condition) +
        current_family + current_fit + current_support +
        institutional_inclusion + linguistic_support
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_culture_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC CULTURAL-DEVELOPMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(model.summary().as_text())
        f.write("\n\nCULTURAL CONDITION MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(condition_model.summary().as_text())

    trajectory = panel.groupby("time", as_index=False).agg(
        average_development=("development_score", "mean"),
        standard_error=("development_score", lambda x: x.std() / (len(x) ** 0.5)),
        average_family=("current_family", "mean"),
        average_fit=("current_fit", "mean"),
        average_mismatch=("current_mismatch", "mean"),
        average_support=("current_support", "mean"),
    )
    trajectory["lower"] = trajectory["average_development"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_development"] + 1.96 * trajectory["standard_error"]
    trajectory.to_csv(OUTPUTS_DIR / "python_culture_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(trajectory["time"], trajectory["average_development"], linewidth=2)
    plt.fill_between(trajectory["time"], trajectory["lower"], trajectory["upper"], alpha=0.2)
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Culture and Development Across Societies")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_culture_trajectory.png", dpi=160)
    plt.close()

    child_summary = panel.groupby("child_id", as_index=False).agg(
        cultural_condition=("cultural_condition", "first"),
        average_mismatch=("current_mismatch", "mean"),
        average_support=("current_support", "mean"),
        average_fit=("current_fit", "mean"),
        final_score=("development_score", "last"),
    )

    condition_summary = child_summary.groupby("cultural_condition", as_index=False).agg(
        children=("child_id", "count"),
        average_final_score=("final_score", "mean"),
        average_mismatch=("average_mismatch", "mean"),
        average_support=("average_support", "mean"),
        average_fit=("average_fit", "mean"),
    )
    condition_summary.to_csv(OUTPUTS_DIR / "python_cultural_conditions.csv", index=False)

    condition_trajectory = panel.groupby(
        ["cultural_condition", "time"],
        as_index=False,
    ).agg(average_development=("development_score", "mean"))

    condition_trajectory.to_csv(OUTPUTS_DIR / "python_condition_trajectories.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    for condition, group in condition_trajectory.groupby("cultural_condition"):
        plt.plot(group["time"], group["average_development"], marker="o", label=condition)
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Developmental Trajectories by Cultural Condition")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_condition_trajectories.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_culture_model_summary.txt")
    print("Wrote outputs/python_culture_trajectory.csv")
    print("Wrote outputs/python_culture_trajectory.png")
    print("Wrote outputs/python_cultural_conditions.csv")
    print("Wrote outputs/python_condition_trajectories.csv")
    print("Wrote outputs/python_condition_trajectories.png")


if __name__ == "__main__":
    main()
