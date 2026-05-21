#!/usr/bin/env python3
"""Model synthetic critical-period and sensitive-period timing effects."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "developmental_timing_panel.csv"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing {DATA_PATH}. Run python/generate_timing_panel.py first."
        )

    panel = pd.read_csv(DATA_PATH)

    critical_model = smf.ols(
        """
        critical_outcome ~ time + experience + critical_weight +
        experience:critical_weight + support + adversity +
        institutional_support + resource_level
        """,
        data=panel,
    ).fit(cov_type="HC3")

    sensitive_model = smf.ols(
        """
        sensitive_outcome ~ time + experience + early_sensitive_weight +
        experience:early_sensitive_weight + support + adversity +
        institutional_support + resource_level
        """,
        data=panel,
    ).fit(cov_type="HC3")

    multi_window_model = smf.ols(
        """
        multi_window_outcome ~ time + experience +
        early_sensitive_weight + adolescent_sensitive_weight +
        experience:early_sensitive_weight +
        experience:adolescent_sensitive_weight +
        support + adversity + institutional_support + resource_level
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUTPUTS_DIR / "python_timing_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("CRITICAL-PERIOD MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(critical_model.summary().as_text())
        f.write("\n\nSENSITIVE-PERIOD MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(sensitive_model.summary().as_text())
        f.write("\n\nMULTI-WINDOW MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(multi_window_model.summary().as_text())

    trajectory = panel.groupby("time", as_index=False).agg(
        critical_weight=("critical_weight", "mean"),
        early_sensitive_weight=("early_sensitive_weight", "mean"),
        adolescent_sensitive_weight=("adolescent_sensitive_weight", "mean"),
        residual_plasticity_weight=("residual_plasticity_weight", "mean"),
        critical_outcome=("critical_outcome", "mean"),
        sensitive_outcome=("sensitive_outcome", "mean"),
        multi_window_outcome=("multi_window_outcome", "mean"),
        recovery_outcome=("recovery_outcome", "mean"),
    )
    trajectory.to_csv(OUTPUTS_DIR / "python_timing_trajectory.csv", index=False)

    plt.figure(figsize=(9, 5.5))
    plt.plot(trajectory["time"], trajectory["critical_weight"], label="Critical period")
    plt.plot(
        trajectory["time"],
        trajectory["early_sensitive_weight"],
        label="Early sensitive period",
    )
    plt.plot(
        trajectory["time"],
        trajectory["adolescent_sensitive_weight"],
        label="Adolescent sensitive period",
    )
    plt.plot(
        trajectory["time"],
        trajectory["residual_plasticity_weight"],
        label="Residual plasticity",
    )
    plt.xlabel("Developmental time")
    plt.ylabel("Timing weight")
    plt.title("Synthetic Developmental Timing Windows")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_timing_windows.png", dpi=160)
    plt.close()

    plt.figure(figsize=(9, 5.5))
    plt.plot(trajectory["time"], trajectory["critical_outcome"], label="Critical outcome")
    plt.plot(trajectory["time"], trajectory["sensitive_outcome"], label="Sensitive outcome")
    plt.plot(trajectory["time"], trajectory["multi_window_outcome"], label="Multi-window outcome")
    plt.plot(trajectory["time"], trajectory["recovery_outcome"], label="Recovery outcome")
    plt.xlabel("Developmental time")
    plt.ylabel("Average synthetic outcome")
    plt.title("Synthetic Timing-Weighted Developmental Outcomes")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / "python_timing_outcomes.png", dpi=160)
    plt.close()

    print("Wrote outputs/python_timing_model_summary.txt")
    print("Wrote outputs/python_timing_trajectory.csv")
    print("Wrote outputs/python_timing_windows.png")
    print("Wrote outputs/python_timing_outcomes.png")


if __name__ == "__main__":
    main()
