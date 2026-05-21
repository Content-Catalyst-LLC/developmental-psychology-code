#!/usr/bin/env python3
"""Model synthetic lifespan developmental psychology in the Baltes tradition."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "lifespan_baltes_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_lifespan_baltes_panel.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("id")["development_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    development_model = smf.ols(
        """
        development_score ~ lag_score + time + gains + losses +
        plasticity + current_support + current_comp + health_resource +
        historical_support + institutional_security + soc_index +
        plasticity:current_support + losses:compensation
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    soc_model = smf.ols(
        """
        soc_index ~ time + selection + optimization + compensation +
        current_support + current_comp + health_resource +
        historical_support + institutional_security
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_lifespan_baltes_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC LIFESPAN DEVELOPMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(development_model.summary().as_text())
        f.write("\n\nSOC ADAPTATION MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(soc_model.summary().as_text())

    trajectory = panel.groupby("time", as_index=False).agg(
        average_development=("development_score", "mean"),
        average_gains=("gains", "mean"),
        average_losses=("losses", "mean"),
        average_soc=("soc_index", "mean"),
        standard_error=("development_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["lower"] = trajectory["average_development"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_development"] + 1.96 * trajectory["standard_error"]
    trajectory.to_csv(OUTPUTS_DIR / "python_lifespan_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(trajectory["time"], trajectory["average_development"], marker="o")
    plt.fill_between(trajectory["time"], trajectory["lower"], trajectory["upper"], alpha=0.15)
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Lifespan Development in the Baltes Tradition")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_lifespan_trajectory.png", dpi=160)
    plt.close()

    soc_trajectory = panel.groupby("time", as_index=False).agg(
        average_selection=("selection", "mean"),
        average_optimization=("optimization", "mean"),
        average_compensation=("compensation", "mean"),
        average_soc=("soc_index", "mean"),
    )
    soc_trajectory.to_csv(OUTPUTS_DIR / "python_soc_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(soc_trajectory["time"], soc_trajectory["average_selection"], marker="o", label="selection")
    plt.plot(soc_trajectory["time"], soc_trajectory["average_optimization"], marker="o", label="optimization")
    plt.plot(soc_trajectory["time"], soc_trajectory["average_compensation"], marker="o", label="compensation")
    plt.xlabel("Time")
    plt.ylabel("Average SOC component")
    plt.title("Synthetic Selection, Optimization, and Compensation")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_soc_trajectory.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("adaptation_profile", as_index=False).agg(
        people=("id", "nunique"),
        average_development=("development_score", "mean"),
        average_gains=("gains", "mean"),
        average_losses=("losses", "mean"),
        average_support=("current_support", "mean"),
        average_soc=("soc_index", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_lifespan_profiles.csv", index=False)

    print("Wrote Python lifespan Baltes model outputs.")


if __name__ == "__main__":
    main()
