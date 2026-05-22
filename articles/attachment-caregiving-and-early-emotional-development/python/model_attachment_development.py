#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "attachment_development_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA).sort_values(["child_id", "time"])
    panel["lag_score"] = panel.groupby("child_id")["regulation_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    model = smf.ols(
        """
        regulation_score ~ lag_score + time + current_care + current_repair +
        current_caregiver_support + current_stress + chronic_stress +
        temperament_reactivity + disability_support_need +
        childcare_continuity + neighborhood_safety +
        family_service_access + caregiving_ecology_support +
        temperament_reactivity:current_care +
        temperament_reactivity:current_stress +
        disability_support_need:family_service_access +
        caregiving_support_context
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    profile_model = smf.ols(
        """
        regulation_score ~ time + chronic_stress + current_stress +
        current_care + current_repair + caregiving_support_context +
        C(attachment_profile)
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUT / "python_attachment_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC ATTACHMENT AND EMOTIONAL DEVELOPMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(model.summary().as_text())
        f.write("\n\nATTACHMENT PROFILE MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(profile_model.summary().as_text())

    trajectory = panel.groupby(["time", "chronic_stress"], as_index=False).agg(
        average_regulation=("regulation_score", "mean"),
        average_care=("current_care", "mean"),
        average_repair=("current_repair", "mean"),
        average_caregiver_support=("current_caregiver_support", "mean"),
        average_stress=("current_stress", "mean"),
        average_support_context=("caregiving_support_context", "mean"),
        standard_error=("regulation_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["stress_group"] = trajectory["chronic_stress"].map({
        0: "Lower chronic stress",
        1: "Higher chronic stress",
    })
    trajectory.to_csv(OUT / "python_stress_attachment_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for label, group in trajectory.groupby("stress_group"):
        plt.plot(group["time"], group["average_regulation"], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average regulation score")
    plt.title("Synthetic Attachment, Caregiving, and Early Emotional Development")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "python_stress_attachment_trajectory.png", dpi=160)
    plt.close()

    context = panel.groupby("time", as_index=False).agg(
        average_care=("current_care", "mean"),
        average_repair=("current_repair", "mean"),
        average_caregiver_support=("current_caregiver_support", "mean"),
        average_stress=("current_stress", "mean"),
        average_support_context=("caregiving_support_context", "mean"),
        average_regulation=("regulation_score", "mean"),
    )
    context.to_csv(OUT / "python_attachment_context_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for col, label in [
        ("average_care", "caregiving responsiveness"),
        ("average_repair", "relational repair"),
        ("average_caregiver_support", "caregiver support"),
        ("average_stress", "stress"),
        ("average_support_context", "support context"),
    ]:
        plt.plot(context["time"], context[col], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average index")
    plt.title("Synthetic Caregiving Context Across Time")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_attachment_context_trajectory.png", dpi=160)
    plt.close()

    panel.groupby("attachment_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_regulation=("regulation_score", "mean"),
        average_caregiving_support_context=("caregiving_support_context", "mean"),
        average_care=("current_care", "mean"),
        average_repair=("current_repair", "mean"),
        average_stress=("current_stress", "mean"),
        chronic_stress_rate=("chronic_stress", "mean"),
        disability_support_need_rate=("disability_support_need", "mean"),
    ).to_csv(OUT / "python_attachment_development_profiles.csv", index=False)

    panel.groupby("context_id", as_index=False).agg(
        childcare_continuity=("childcare_continuity", "mean"),
        neighborhood_safety=("neighborhood_safety", "mean"),
        family_service_access=("family_service_access", "mean"),
        caregiving_ecology_support=("caregiving_ecology_support", "mean"),
        average_regulation=("regulation_score", "mean"),
        average_stress=("current_stress", "mean"),
        average_caregiving_support_context=("caregiving_support_context", "mean"),
    ).to_csv(OUT / "python_attachment_context_summary.csv", index=False)

    print("Wrote Python attachment model outputs.")

if __name__ == "__main__":
    main()
