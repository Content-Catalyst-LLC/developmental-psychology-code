#!/usr/bin/env python3
"""Model synthetic historical broadening in developmental psychology."""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "developmental_psychology_history_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

PARADIGMS = [
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


def main() -> None:
    df = pd.read_csv(DATA)

    selected = df[df["year"].isin([1900, 1930, 1950, 1975, 2000, 2025])]
    selected.to_csv(OUT / "python_selected_historical_years.csv", index=False)

    summary = pd.DataFrame({
        "paradigm": PARADIGMS,
        "peak_year": [int(df.loc[df[col].idxmax(), "year"]) for col in PARADIGMS],
        "peak_share": [float(df[col].max()) for col in PARADIGMS],
        "share_1900": [float(df.loc[df["year"] == 1900, col].iloc[0]) for col in PARADIGMS],
        "share_2025": [float(df.loc[df["year"] == 2025, col].iloc[0]) for col in PARADIGMS],
    })
    summary.to_csv(OUT / "python_paradigm_peak_summary.csv", index=False)

    plt.figure(figsize=(11, 6))
    for col in PARADIGMS:
        plt.plot(df["year"], df[col], label=col)
    plt.xlabel("Year")
    plt.ylabel("Synthetic relative prominence")
    plt.title("Simulated Intellectual History of Developmental Psychology")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(OUT / "python_paradigm_history.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    for col in ["child_centered_index", "lifespan_index", "ecological_systems_index", "broadening_index"]:
        plt.plot(df["year"], df[col], label=col)
    plt.xlabel("Year")
    plt.ylabel("Synthetic index")
    plt.title("Historical Broadening Indexes in Developmental Psychology")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_broadening_indexes.png", dpi=160)
    plt.close()

    field_forces = df[["year", "institutional_support", "methodological_advantage", "social_relevance", "critique_index"]]
    field_forces.to_csv(OUT / "python_field_forces.csv", index=False)

    with open(OUT / "python_history_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("Synthetic developmental psychology historical model\n")
        f.write("=" * 72 + "\n\n")
        f.write("Selected years\n")
        f.write(selected.to_string(index=False))
        f.write("\n\nParadigm peak summary\n")
        f.write(summary.to_string(index=False))
        f.write("\n\nInterpretive note: values are synthetic teaching data, not empirical bibliometric estimates.\n")

    print("Wrote Python developmental history outputs.")


if __name__ == "__main__":
    main()
