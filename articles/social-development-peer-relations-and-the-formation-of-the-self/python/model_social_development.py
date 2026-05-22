#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "social_development_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA).sort_values(["child_id", "time"])
    panel["lag_score"] = panel.groupby("child_id")["social_self_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    model = smf.ols(
        """
        social_self_score ~ lag_score + time + current_peer_support +
        current_friendship_quality + current_family_support +
        current_social_interpretation + school_connectedness +
        teacher_support + anti_bullying_climate + inclusion_climate +
        restorative_practice_access + current_exclusion +
        bullying_exposure + digital_comparison_stress +
        chronic_exclusion + social_support_context
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    profile_model = smf.ols(
        """
        social_self_score ~ time + chronic_exclusion + current_exclusion +
        bullying_exposure + digital_comparison_stress + social_support_context +
        C(social_profile)
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUT / "python_social_development_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC SOCIAL DEVELOPMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(model.summary().as_text())
        f.write("\n\nSOCIAL PROFILE MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(profile_model.summary().as_text())

    trajectory = panel.groupby(["time", "chronic_exclusion"], as_index=False).agg(
        average_social_self=("social_self_score", "mean"),
        average_social_context=("social_support_context", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_bullying=("bullying_exposure", "mean"),
        average_digital_comparison=("digital_comparison_stress", "mean"),
        standard_error=("social_self_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["exclusion_group"] = trajectory["chronic_exclusion"].map({
        0: "Lower exclusion risk",
        1: "Higher exclusion risk",
    })
    trajectory.to_csv(OUT / "python_exclusion_social_self_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for label, group in trajectory.groupby("exclusion_group"):
        plt.plot(group["time"], group["average_social_self"], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average social-self score")
    plt.title("Synthetic Social Development and Self Formation")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "python_exclusion_social_self_trajectory.png", dpi=160)
    plt.close()

    context = panel.groupby("time", as_index=False).agg(
        average_peer_support=("current_peer_support", "mean"),
        average_friendship_quality=("current_friendship_quality", "mean"),
        average_family_support=("current_family_support", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_bullying=("bullying_exposure", "mean"),
        average_digital_comparison=("digital_comparison_stress", "mean"),
        average_social_context=("social_support_context", "mean"),
        average_social_self=("social_self_score", "mean"),
    )
    context.to_csv(OUT / "python_social_context_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for col, label in [
        ("average_peer_support", "peer support"),
        ("average_friendship_quality", "friendship quality"),
        ("average_family_support", "family support"),
        ("average_exclusion", "exclusion"),
        ("average_bullying", "bullying"),
        ("average_digital_comparison", "digital comparison"),
        ("average_social_context", "social context"),
    ]:
        plt.plot(context["time"], context[col], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average index")
    plt.title("Synthetic Social Development Context Across Time")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_social_context_trajectory.png", dpi=160)
    plt.close()

    panel.groupby("social_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_social_self=("social_self_score", "mean"),
        average_social_support_context=("social_support_context", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_bullying=("bullying_exposure", "mean"),
        average_digital_comparison=("digital_comparison_stress", "mean"),
        chronic_exclusion_rate=("chronic_exclusion", "mean"),
    ).to_csv(OUT / "python_social_development_profiles.csv", index=False)

    panel.groupby("school_id", as_index=False).agg(
        school_connectedness=("school_connectedness", "mean"),
        teacher_support=("teacher_support", "mean"),
        anti_bullying_climate=("anti_bullying_climate", "mean"),
        inclusion_climate=("inclusion_climate", "mean"),
        restorative_practice_access=("restorative_practice_access", "mean"),
        average_social_self=("social_self_score", "mean"),
        average_social_context=("social_support_context", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_bullying=("bullying_exposure", "mean"),
    ).to_csv(OUT / "python_school_social_context_summary.csv", index=False)

    print("Wrote Python social development model outputs.")

if __name__ == "__main__":
    main()
