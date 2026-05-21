#!/usr/bin/env python3
"""Model synthetic schooling, connectedness, and developmental formation."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "schooling_development_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_schooling_development_panel.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["student_id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("student_id")["development_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    development_model = smf.ols(
        """
        development_score ~ lag_score + time + current_teacher +
        current_peer + school_climate + curriculum_opportunity +
        current_family + current_confidence + resource_capacity +
        intervention + connectedness_score + current_stress +
        current_teacher:current_peer
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    connectedness_model = smf.ols(
        """
        connectedness_score ~ time + current_teacher + current_peer +
        school_climate + restorative_practice + current_stress +
        current_family + current_confidence
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_schooling_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC DEVELOPMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(development_model.summary().as_text())
        f.write("\n\nCONNECTEDNESS MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(connectedness_model.summary().as_text())

    trajectory = panel.groupby(["time", "intervention"], as_index=False).agg(
        average_development=("development_score", "mean"),
        average_connectedness=("connectedness_score", "mean"),
        standard_error=("development_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["lower"] = trajectory["average_development"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_development"] + 1.96 * trajectory["standard_error"]
    trajectory["group"] = trajectory["intervention"].map({0: "No program", 1: "Support program"})
    trajectory.to_csv(OUTPUTS_DIR / "python_development_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for group_name, group in trajectory.groupby("group"):
        plt.plot(group["time"], group["average_development"], marker="o", label=group_name)
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Education, Schooling, and Developmental Formation")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_development_trajectory.png", dpi=160)
    plt.close()

    connectedness = panel.groupby("time", as_index=False).agg(
        average_connectedness=("connectedness_score", "mean"),
        average_teacher=("current_teacher", "mean"),
        average_peer=("current_peer", "mean"),
        average_stress=("current_stress", "mean"),
    )
    connectedness.to_csv(OUTPUTS_DIR / "python_connectedness_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(connectedness["time"], connectedness["average_connectedness"], marker="o")
    plt.xlabel("Time")
    plt.ylabel("Average connectedness score")
    plt.title("Synthetic School Connectedness Trajectory")
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_connectedness_trajectory.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("school_support_profile", as_index=False).agg(
        students=("student_id", "nunique"),
        average_development=("development_score", "mean"),
        average_connectedness=("connectedness_score", "mean"),
        average_teacher=("current_teacher", "mean"),
        average_peer=("current_peer", "mean"),
        average_stress=("current_stress", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_school_support_profiles.csv", index=False)

    print("Wrote Python schooling model outputs.")


if __name__ == "__main__":
    main()
