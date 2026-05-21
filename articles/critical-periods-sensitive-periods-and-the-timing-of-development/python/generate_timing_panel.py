#!/usr/bin/env python3
"""Generate synthetic timing-window panel data.

The data demonstrate critical-period, sensitive-period, multi-window, and
residual-plasticity assumptions using synthetic developmental observations.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def gaussian_weight(time: np.ndarray, center: float, sd: float) -> np.ndarray:
    """Return a smooth sensitive-period timing weight."""
    return np.exp(-((time - center) ** 2) / (2 * sd**2))


def generate_panel(
    n_people: int = 900,
    n_periods: int = 14,
    n_contexts: int = 30,
    seed: int = 2026,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    people = pd.DataFrame(
        {
            "person_id": np.arange(1, n_people + 1),
            "context_id": rng.integers(1, n_contexts + 1, size=n_people),
            "baseline_capacity": rng.normal(0, 1, n_people),
            "baseline_support": rng.normal(0, 1, n_people),
            "baseline_adversity": rng.normal(0, 1, n_people),
            "person_plasticity": rng.normal(0, 0.7, n_people),
        }
    )

    contexts = pd.DataFrame(
        {
            "context_id": np.arange(1, n_contexts + 1),
            "institutional_support": rng.normal(0, 0.7, n_contexts),
            "resource_level": rng.normal(0, 0.7, n_contexts),
        }
    )

    panel = people.loc[people.index.repeat(n_periods)].copy()
    panel["time"] = np.tile(np.arange(1, n_periods + 1), n_people)
    panel = panel.merge(contexts, on="context_id", how="left")

    panel["experience"] = rng.normal(
        panel["baseline_support"] + 0.35 * panel["institutional_support"],
        0.75,
    )
    panel["support"] = rng.normal(
        panel["baseline_support"] + 0.40 * panel["resource_level"],
        0.65,
    )
    panel["adversity"] = rng.normal(panel["baseline_adversity"], 0.70)
    panel["late_intervention"] = np.where(
        panel["time"] >= 9,
        rng.normal(0.80 + 0.30 * panel["institutional_support"], 0.50, len(panel)),
        rng.normal(0.05, 0.20, len(panel)),
    )

    panel["critical_weight"] = np.where(
        (panel["time"] >= 3) & (panel["time"] <= 5),
        1.0,
        0.0,
    )
    panel["early_sensitive_weight"] = gaussian_weight(panel["time"].to_numpy(), 4.0, 2.0)
    panel["adolescent_sensitive_weight"] = gaussian_weight(
        panel["time"].to_numpy(),
        10.0,
        2.2,
    )
    panel["residual_plasticity_weight"] = gaussian_weight(
        panel["time"].to_numpy(),
        11.0,
        3.5,
    )

    panel = panel.sort_values(["person_id", "time"]).reset_index(drop=True)

    panel["critical_exposure"] = panel["experience"] * panel["critical_weight"]
    panel["sensitive_exposure"] = panel["experience"] * panel["early_sensitive_weight"]
    panel["multi_window_exposure"] = panel["experience"] * (
        0.65 * panel["early_sensitive_weight"]
        + 0.55 * panel["adolescent_sensitive_weight"]
    )

    panel["cumulative_critical_exposure"] = panel.groupby("person_id")[
        "critical_exposure"
    ].cumsum()
    panel["cumulative_sensitive_exposure"] = panel.groupby("person_id")[
        "sensitive_exposure"
    ].cumsum()

    noise = rng.normal(0, 2.0, len(panel))

    panel["critical_outcome"] = (
        50
        + 0.30 * panel["time"]
        + 2.20 * panel["critical_exposure"]
        + 0.65 * panel["support"]
        - 0.75 * panel["adversity"]
        + 0.55 * panel["baseline_capacity"]
        + noise
    )

    panel["sensitive_outcome"] = (
        50
        + 0.30 * panel["time"]
        + 2.00 * panel["sensitive_exposure"]
        + 0.70 * panel["support"]
        - 0.80 * panel["adversity"]
        + 0.60 * panel["person_plasticity"]
        + rng.normal(0, 2.0, len(panel))
    )

    panel["multi_window_outcome"] = (
        50
        + 0.30 * panel["time"]
        + 2.10 * panel["multi_window_exposure"]
        + 0.75 * panel["support"]
        - 0.85 * panel["adversity"]
        + 0.45 * panel["institutional_support"]
        + rng.normal(0, 2.0, len(panel))
    )

    panel["recovery_outcome"] = (
        50
        + 0.25 * panel["time"]
        + 1.60 * panel["sensitive_exposure"]
        + 1.10 * panel["late_intervention"] * panel["residual_plasticity_weight"]
        + 0.65 * panel["support"]
        - 0.75 * panel["adversity"]
        + rng.normal(0, 2.1, len(panel))
    )

    contexts.to_csv(DATA_DIR / "context_metadata.csv", index=False)
    return panel


def main() -> None:
    panel = generate_panel()

    panel_path = DATA_DIR / "developmental_timing_panel.csv"
    panel.to_csv(panel_path, index=False)

    timing_summary = panel.groupby("time", as_index=False).agg(
        critical_weight=("critical_weight", "mean"),
        early_sensitive_weight=("early_sensitive_weight", "mean"),
        adolescent_sensitive_weight=("adolescent_sensitive_weight", "mean"),
        residual_plasticity_weight=("residual_plasticity_weight", "mean"),
        mean_critical_outcome=("critical_outcome", "mean"),
        mean_sensitive_outcome=("sensitive_outcome", "mean"),
        mean_multi_window_outcome=("multi_window_outcome", "mean"),
        mean_recovery_outcome=("recovery_outcome", "mean"),
    )
    timing_summary.to_csv(DATA_DIR / "timing_window_summary.csv", index=False)

    print(f"Wrote {panel_path}")
    print(f"Rows: {len(panel):,}")
    print(f"People: {panel['person_id'].nunique():,}")
    print(f"Contexts: {panel['context_id'].nunique():,}")


if __name__ == "__main__":
    main()
