#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "moral_development_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA).sort_values(["child_id", "time"])
    panel["lag_conscience"] = panel.groupby("child_id")["conscience_score"].shift(1)
    panel["lag_action"] = panel.groupby("child_id")["moral_action_score"].shift(1)
    model_data = panel.dropna(subset=["lag_conscience", "lag_action"]).copy()

    conscience_model = smf.ols(
        """
        conscience_score ~ lag_conscience + time + current_guidance +
        current_empathy + current_peer_fairness + current_self_regulation +
        current_harm_recognition + current_repair_opportunity +
        school_moral_climate + restorative_practice_access +
        punitive_inconsistency + anti_bullying_climate + digital_moral_safety +
        current_exclusion + digital_cruelty_exposure + chronic_exclusion +
        moral_support_context
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    action_model = smf.ols(
        """
        moral_action_score ~ lag_action + conscience_score + current_self_regulation +
        current_peer_fairness + current_empathy + current_harm_recognition +
        current_repair_opportunity + peer_pressure + current_exclusion +
        digital_cruelty_exposure + moral_support_context
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    with open(OUT / "python_moral_development_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC CONSCIENCE MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(conscience_model.summary().as_text())
        f.write("\n\nMORAL ACTION MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(action_model.summary().as_text())

    trajectory = panel.groupby(["time", "chronic_exclusion"], as_index=False).agg(
        average_conscience=("conscience_score", "mean"),
        average_moral_action=("moral_action_score", "mean"),
        average_moral_context=("moral_support_context", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_peer_pressure=("peer_pressure", "mean"),
    )
    trajectory["exclusion_group"] = trajectory["chronic_exclusion"].map({
        0: "Lower exclusion risk",
        1: "Higher exclusion risk",
    })
    trajectory.to_csv(OUT / "python_exclusion_conscience_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for label, group in trajectory.groupby("exclusion_group"):
        plt.plot(group["time"], group["average_conscience"], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average conscience score")
    plt.title("Synthetic Moral Development and Growth of Conscience")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "python_exclusion_conscience_trajectory.png", dpi=160)
    plt.close()

    context = panel.groupby("time", as_index=False).agg(
        average_guidance=("current_guidance", "mean"),
        average_empathy=("current_empathy", "mean"),
        average_peer_fairness=("current_peer_fairness", "mean"),
        average_repair=("current_repair_opportunity", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_moral_context=("moral_support_context", "mean"),
        average_conscience=("conscience_score", "mean"),
        average_moral_action=("moral_action_score", "mean"),
    )
    context.to_csv(OUT / "python_moral_context_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for col, label in [
        ("average_guidance", "guidance"),
        ("average_empathy", "empathy"),
        ("average_peer_fairness", "peer fairness"),
        ("average_repair", "repair"),
        ("average_exclusion", "exclusion"),
        ("average_moral_context", "moral context"),
    ]:
        plt.plot(context["time"], context[col], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average index")
    plt.title("Synthetic Moral Development Context Across Time")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_moral_context_trajectory.png", dpi=160)
    plt.close()

    panel.groupby("moral_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_conscience=("conscience_score", "mean"),
        average_moral_action=("moral_action_score", "mean"),
        average_moral_support_context=("moral_support_context", "mean"),
        average_exclusion=("current_exclusion", "mean"),
        average_peer_pressure=("peer_pressure", "mean"),
        chronic_exclusion_rate=("chronic_exclusion", "mean"),
    ).to_csv(OUT / "python_moral_development_profiles.csv", index=False)

    panel.groupby("school_id", as_index=False).agg(
        school_moral_climate=("school_moral_climate", "mean"),
        restorative_practice_access=("restorative_practice_access", "mean"),
        punitive_inconsistency=("punitive_inconsistency", "mean"),
        anti_bullying_climate=("anti_bullying_climate", "mean"),
        digital_moral_safety=("digital_moral_safety", "mean"),
        average_conscience=("conscience_score", "mean"),
        average_moral_action=("moral_action_score", "mean"),
        average_moral_context=("moral_support_context", "mean"),
        average_exclusion=("current_exclusion", "mean"),
    ).to_csv(OUT / "python_school_moral_context_summary.csv", index=False)

    print("Wrote Python moral development model outputs.")

if __name__ == "__main__":
    main()
