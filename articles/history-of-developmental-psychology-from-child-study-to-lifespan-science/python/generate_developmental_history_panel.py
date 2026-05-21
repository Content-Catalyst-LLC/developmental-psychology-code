#!/usr/bin/env python3
"""Generate synthetic historical panel data for developmental psychology."""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)


def logistic(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))


def wave(years: np.ndarray, rise: float, fall: float | None = None, growth: float = 0.08, decline: float = 0.06) -> np.ndarray:
    rising = logistic(growth * (years - rise))
    if fall is None:
        return rising
    return np.clip(rising - logistic(decline * (years - fall)), 0.001, None)


def main(seed: int = 2026) -> None:
    rng = np.random.default_rng(seed)
    years = np.arange(1900, 2026)

    df = pd.DataFrame({"year": years})
    df["child_study"] = 1 / (1 + np.exp(0.060 * (years - 1925)))
    df["maturational"] = wave(years, rise=1918, fall=1962, growth=0.090, decline=0.070)
    df["psychoanalytic"] = wave(years, rise=1915, fall=1980, growth=0.075, decline=0.055)
    df["behaviorist"] = wave(years, rise=1925, fall=1970, growth=0.100, decline=0.075)
    df["cognitive_developmental"] = wave(years, rise=1955, fall=None, growth=0.105)
    df["sociocultural"] = wave(years, rise=1975, fall=None, growth=0.070)
    df["attachment_social"] = wave(years, rise=1965, fall=None, growth=0.075)
    df["ecological"] = wave(years, rise=1975, fall=None, growth=0.080)
    df["lifespan"] = wave(years, rise=1970, fall=None, growth=0.095)
    df["developmental_psychopathology"] = wave(years, rise=1985, fall=None, growth=0.080)
    df["neuroscience_genetics"] = wave(years, rise=1995, fall=None, growth=0.090)
    df["developmental_systems"] = wave(years, rise=1995, fall=None, growth=0.090)

    paradigm_cols = [
        "child_study",
        "maturational",
        "psychoanalytic",
        "behaviorist",
        "cognitive_developmental",
        "sociocultural",
        "attachment_social",
        "ecological",
        "lifespan",
        "developmental_psychopathology",
        "neuroscience_genetics",
        "developmental_systems",
    ]

    for col in paradigm_cols:
        df[col] = np.clip(df[col] + rng.normal(0, 0.018, len(df)), 0.001, None)

    df[paradigm_cols] = df[paradigm_cols].div(df[paradigm_cols].sum(axis=1), axis=0)

    df["institutional_support"] = np.clip(
        logistic(0.055 * (years - 1930)) + 0.15 * logistic(0.070 * (years - 1962)) + rng.normal(0, 0.015, len(df)),
        0,
        None,
    )
    df["methodological_advantage"] = np.clip(
        logistic(0.050 * (years - 1940)) + 0.20 * logistic(0.075 * (years - 1980)) + rng.normal(0, 0.015, len(df)),
        0,
        None,
    )
    df["social_relevance"] = np.clip(
        logistic(0.045 * (years - 1950)) + 0.20 * logistic(0.065 * (years - 1990)) + rng.normal(0, 0.015, len(df)),
        0,
        None,
    )
    df["critique_index"] = np.clip(
        logistic(0.060 * (years - 1970)) + 0.25 * logistic(0.090 * (years - 2000)) + rng.normal(0, 0.015, len(df)),
        0,
        None,
    )

    df["child_centered_index"] = df["child_study"] + df["maturational"] + df["behaviorist"] * 0.35
    df["lifespan_index"] = df["lifespan"] + 0.30 * df["developmental_systems"]
    df["ecological_systems_index"] = df["ecological"] + df["developmental_systems"] + 0.30 * df["sociocultural"]
    df["broadening_index"] = (
        df["sociocultural"]
        + df["ecological"]
        + df["lifespan"]
        + df["developmental_psychopathology"]
        + df["developmental_systems"]
        + 0.50 * df["neuroscience_genetics"]
    )

    df.to_csv(DATA / "developmental_psychology_history_panel.csv", index=False)
    df[df["year"].isin([1900, 1930, 1950, 1975, 2000, 2025])].to_csv(
        DATA / "developmental_psychology_history_selected_years.csv",
        index=False,
    )

    metadata = pd.DataFrame({
        "paradigm": paradigm_cols,
        "interpretive_note": [
            "Early child-study observation and educational reform traditions",
            "Biologically guided sequences and maturational timing",
            "Early experience, conflict, identity, and psychosocial development",
            "Learning, conditioning, reinforcement, and observable behavior",
            "Piagetian and cognitive-developmental transformation of thought",
            "Vygotskian, cultural, mediated, and participatory development",
            "Attachment, caregiving, relationship, and social development",
            "Bronfenbrennerian and ecological person-context models",
            "Life-span developmental psychology and aging",
            "Risk, resilience, maladaptation, and developmental pathways",
            "Brain, genetics, epigenetics, and biological embedding",
            "Relational developmental systems and multilevel coaction",
        ],
    })
    metadata.to_csv(DATA / "paradigm_metadata.csv", index=False)

    print(f"Wrote {DATA / 'developmental_psychology_history_panel.csv'} with {len(df)} rows")


if __name__ == "__main__":
    main()
