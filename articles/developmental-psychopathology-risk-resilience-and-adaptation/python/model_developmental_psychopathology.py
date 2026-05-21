#!/usr/bin/env python3
"""Model synthetic developmental psychopathology trajectories."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "developmental_psychopathology_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_developmental_psychopathology.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["child_id", "time"]).reset_index(drop=True)
    panel["lag_adaptation"] = panel.groupby("child_id")["adaptation_score"].shift(1)
    panel["lag_internalizing"] = panel.groupby("child_id")["internalizing_score"].shift(1)
    panel["lag_externalizing"] = panel.groupby("child_id")["externalizing_score"].shift(1)
    model_data = panel.dropna(subset=["lag_adaptation"]).copy()

    adaptation_model = smf.ols(
        """
        adaptation_score ~ lag_adaptation + time + current_regulation +
        current_support + current_risk + cumulative_risk +
        current_stability + community_support + school_belonging +
        service_access + transition_support + biological_sensitivity +
        current_support:current_stability
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    internalizing_model = smf.ols(
        """
        internalizing_score ~ lag_internalizing + time + current_risk +
        cumulative_risk + current_support + current_stability +
        community_support + school_belonging + service_access +
        biological_sensitivity
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    externalizing_model = smf.ols(
        """
        externalizing_score ~ lag_externalizing + time + current_risk +
        cumulative_risk + current_support + current_stability +
        community_support + school_belonging + service_access +
        current_regulation + biological_sensitivity
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_psychopathology_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC ADAPTATION MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(adaptation_model.summary().as_text())
        f.write("\n\nINTERNALIZING PATHWAY MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(internalizing_model.summary().as_text())
        f.write("\n\nEXTERNALIZING PATHWAY MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(externalizing_model.summary().as_text())

    trajectory = panel.groupby("time", as_index=False).agg(
        average_adaptation=("adaptation_score", "mean"),
        average_internalizing=("internalizing_score", "mean"),
        average_externalizing=("externalizing_score", "mean"),
        standard_error=("adaptation_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["lower"] = trajectory["average_adaptation"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_adaptation"] + 1.96 * trajectory["standard_error"]
    trajectory.to_csv(OUTPUTS_DIR / "python_adaptation_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(trajectory["time"], trajectory["average_adaptation"], linewidth=2)
    plt.fill_between(trajectory["time"], trajectory["lower"], trajectory["upper"], alpha=0.2)
    plt.xlabel("Time")
    plt.ylabel("Average adaptation score")
    plt.title("Synthetic Developmental Psychopathology Trajectories")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_adaptation_trajectory.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(trajectory["time"], trajectory["average_internalizing"], marker="o", label="internalizing")
    plt.plot(trajectory["time"], trajectory["average_externalizing"], marker="o", label="externalizing")
    plt.xlabel("Time")
    plt.ylabel("Average pathway score")
    plt.title("Synthetic Multifinality Pathways")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_multifinality_pathways.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("risk_support_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_adaptation=("adaptation_score", "mean"),
        average_internalizing=("internalizing_score", "mean"),
        average_externalizing=("externalizing_score", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_risk_support_profiles.csv", index=False)

    print("Wrote Python model outputs.")


if __name__ == "__main__":
    main()
