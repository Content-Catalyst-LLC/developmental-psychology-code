#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "puberty_embodiment_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA).sort_values(["adolescent_id", "time"])
    panel["lag_score"] = panel.groupby("adolescent_id")["adjustment_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"])

    model = smf.ols(
        """
        adjustment_score ~ lag_score + pubertal_progress + timing_deviation +
        current_family_support + current_peer_comparison +
        current_body_concern + current_stigma + digital_visibility_stress +
        chronic_stigma + school_support + health_education_quality +
        privacy_protection + menstrual_support + disability_accommodation +
        anti_harassment_climate + digital_safety + protective_context
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    (OUT / "python_puberty_embodiment_model_summary.txt").write_text(model.summary().as_text(), encoding="utf-8")

    trajectory = panel.groupby(["time", "chronic_stigma"], as_index=False).agg(
        average_adjustment=("adjustment_score", "mean"),
        average_protective_context=("protective_context", "mean"),
        average_peer_comparison=("current_peer_comparison", "mean"),
        average_stigma=("current_stigma", "mean"),
        average_body_concern=("current_body_concern", "mean"),
        average_digital_visibility_stress=("digital_visibility_stress", "mean"),
        standard_error=("adjustment_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["group_label"] = trajectory["chronic_stigma"].map({0: "Lower stigma risk", 1: "Higher stigma risk"})
    trajectory.to_csv(OUT / "python_stigma_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for label, group in trajectory.groupby("group_label"):
        plt.plot(group["time"], group["average_adjustment"], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average adjustment score")
    plt.title("Synthetic Puberty, Embodiment, and Adolescent Transition")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "python_stigma_trajectory.png", dpi=160)
    plt.close()

    support = panel.groupby("time", as_index=False).agg(
        average_family_support=("current_family_support", "mean"),
        average_peer_comparison=("current_peer_comparison", "mean"),
        average_body_concern=("current_body_concern", "mean"),
        average_stigma=("current_stigma", "mean"),
        average_digital_visibility_stress=("digital_visibility_stress", "mean"),
        average_protective_context=("protective_context", "mean"),
        average_adjustment=("adjustment_score", "mean"),
    )
    support.to_csv(OUT / "python_protective_context_trajectory.csv", index=False)

    profiles = panel.groupby("puberty_profile", as_index=False).agg(
        adolescents=("adolescent_id", "nunique"),
        average_adjustment=("adjustment_score", "mean"),
        average_protective_context=("protective_context", "mean"),
        average_stigma=("current_stigma", "mean"),
        average_body_concern=("current_body_concern", "mean"),
        average_digital_visibility_stress=("digital_visibility_stress", "mean"),
        chronic_stigma_rate=("chronic_stigma", "mean"),
        average_abs_timing_deviation=("timing_deviation", lambda x: x.abs().mean()),
    )
    profiles.to_csv(OUT / "python_puberty_profiles.csv", index=False)

    schools = panel.groupby("school_id", as_index=False).agg(
        school_support=("school_support", "mean"),
        health_education_quality=("health_education_quality", "mean"),
        privacy_protection=("privacy_protection", "mean"),
        menstrual_support=("menstrual_support", "mean"),
        disability_accommodation=("disability_accommodation", "mean"),
        anti_harassment_climate=("anti_harassment_climate", "mean"),
        digital_safety=("digital_safety", "mean"),
        average_adjustment=("adjustment_score", "mean"),
        average_protective_context=("protective_context", "mean"),
        average_stigma=("current_stigma", "mean"),
    )
    schools.to_csv(OUT / "python_school_puberty_context_summary.csv", index=False)

    print("Wrote Python puberty embodiment model outputs.")

if __name__ == "__main__":
    main()
