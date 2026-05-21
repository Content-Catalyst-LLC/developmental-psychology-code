#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "adolescence_identity_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA).sort_values(["adolescent_id", "time"])
    panel["lag_score"] = panel.groupby("adolescent_id")["identity_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"])

    model = smf.ols(
        """
        identity_score ~ lag_score + time + current_peer_support +
        current_family_support + current_connectedness +
        current_future_orientation + school_climate + counseling_access +
        extracurricular_access + identity_safety + digital_safety +
        current_exclusion + digital_stress + chronic_exclusion
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    (OUT / "python_adolescence_identity_model_summary.txt").write_text(model.summary().as_text(), encoding="utf-8")

    trajectory = panel.groupby(["time", "chronic_exclusion"], as_index=False).agg(
        average_identity=("identity_score", "mean"),
        average_support_context=("support_context", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_digital_stress=("digital_stress", "mean"),
        standard_error=("identity_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["group_label"] = trajectory["chronic_exclusion"].map({0: "Lower exclusion risk", 1: "Higher exclusion risk"})
    trajectory.to_csv(OUT / "python_exclusion_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for label, group in trajectory.groupby("group_label"):
        plt.plot(group["time"], group["average_identity"], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average identity score")
    plt.title("Synthetic Adolescence, Identity, and Psychological Transition")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "python_exclusion_trajectory.png", dpi=160)
    plt.close()

    support = panel.groupby("time", as_index=False).agg(
        average_peer_support=("current_peer_support", "mean"),
        average_family_support=("current_family_support", "mean"),
        average_connectedness=("current_connectedness", "mean"),
        average_future_orientation=("current_future_orientation", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_digital_stress=("digital_stress", "mean"),
        average_identity=("identity_score", "mean"),
    )
    support.to_csv(OUT / "python_support_context_trajectory.csv", index=False)

    profiles = panel.groupby("identity_profile", as_index=False).agg(
        adolescents=("adolescent_id", "nunique"),
        average_identity=("identity_score", "mean"),
        average_support_context=("support_context", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_digital_stress=("digital_stress", "mean"),
        chronic_exclusion_rate=("chronic_exclusion", "mean"),
    )
    profiles.to_csv(OUT / "python_identity_profiles.csv", index=False)

    schools = panel.groupby("school_id", as_index=False).agg(
        school_climate=("school_climate", "mean"),
        counseling_access=("counseling_access", "mean"),
        extracurricular_access=("extracurricular_access", "mean"),
        identity_safety=("identity_safety", "mean"),
        digital_safety=("digital_safety", "mean"),
        average_identity=("identity_score", "mean"),
        average_support_context=("support_context", "mean"),
        average_exclusion=("current_exclusion", "mean"),
    )
    schools.to_csv(OUT / "python_school_context_summary.csv", index=False)
    print("Wrote Python adolescent identity model outputs.")

if __name__ == "__main__":
    main()
