#!/usr/bin/env python3
"""Model synthetic wisdom, meaning, and development in later life."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "wisdom_meaning_later_life_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Run python/generate_wisdom_meaning_panel.py first.")

    panel = pd.read_csv(DATA_PATH).sort_values(["id", "time"]).reset_index(drop=True)
    panel["lag_score"] = panel.groupby("id")["meaning_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    meaning_model = smf.ols(
        """
        meaning_score ~ lag_score + time + current_connection +
        current_reflection + current_support + current_legacy +
        current_health + dignity_support + service_access +
        community_participation + wisdom_index
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    wisdom_model = smf.ols(
        """
        wisdom_index ~ time + current_connection + current_reflection +
        current_legacy + current_health + dignity_support +
        service_access + community_participation
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_wisdom_meaning_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC LATER-LIFE MEANING MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(meaning_model.summary().as_text())
        f.write("\n\nWISDOM INDEX MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(wisdom_model.summary().as_text())

    panel["connection_group"] = pd.qcut(
        panel["current_connection"],
        3,
        labels=["Lower connection", "Moderate connection", "Higher connection"],
    )

    trajectory = panel.groupby(["time", "connection_group"], as_index=False, observed=True).agg(
        average_meaning=("meaning_score", "mean"),
        average_wisdom=("wisdom_index", "mean"),
        standard_error=("meaning_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["lower"] = trajectory["average_meaning"] - 1.96 * trajectory["standard_error"]
    trajectory["upper"] = trajectory["average_meaning"] + 1.96 * trajectory["standard_error"]
    trajectory.to_csv(OUTPUTS_DIR / "python_meaning_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for group_name, group in trajectory.groupby("connection_group", observed=True):
        plt.plot(group["time"], group["average_meaning"], marker="o", label=str(group_name))
    plt.xlabel("Time")
    plt.ylabel("Average meaning score")
    plt.title("Synthetic Wisdom, Meaning, and Development in Later Life")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_meaning_trajectory.png", dpi=160)
    plt.close()

    wisdom_trajectory = panel.groupby("time", as_index=False).agg(
        average_wisdom=("wisdom_index", "mean"),
        average_connection=("current_connection", "mean"),
        average_reflection=("current_reflection", "mean"),
        average_health=("current_health", "mean"),
        average_legacy=("current_legacy", "mean"),
    )
    wisdom_trajectory.to_csv(OUTPUTS_DIR / "python_wisdom_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(wisdom_trajectory["time"], wisdom_trajectory["average_wisdom"], marker="o", label="wisdom index")
    plt.plot(wisdom_trajectory["time"], wisdom_trajectory["average_reflection"], marker="o", label="reflection")
    plt.plot(wisdom_trajectory["time"], wisdom_trajectory["average_connection"], marker="o", label="connection")
    plt.xlabel("Time")
    plt.ylabel("Average index")
    plt.title("Synthetic Wisdom, Reflection, and Connection")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_wisdom_trajectory.png", dpi=160)
    plt.close()

    profile_summary = panel.groupby("meaning_profile", as_index=False).agg(
        people=("id", "nunique"),
        average_meaning=("meaning_score", "mean"),
        average_wisdom=("wisdom_index", "mean"),
        average_connection=("current_connection", "mean"),
        average_reflection=("current_reflection", "mean"),
        average_health=("current_health", "mean"),
        average_support=("current_support", "mean"),
    )
    profile_summary.to_csv(OUTPUTS_DIR / "python_wisdom_meaning_profiles.csv", index=False)

    print("Wrote Python wisdom and meaning model outputs.")


if __name__ == "__main__":
    main()
