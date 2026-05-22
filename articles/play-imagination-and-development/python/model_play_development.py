#!/usr/bin/env python3
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "play_development_panel.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main() -> None:
    panel = pd.read_csv(DATA).sort_values(["child_id", "time"])
    panel["lag_score"] = panel.groupby("child_id")["development_score"].shift(1)
    model_data = panel.dropna(subset=["lag_score"]).copy()

    model = smf.ols(
        """
        development_score ~ lag_score + time + current_pretend +
        current_social_play + current_constructive + current_outdoor +
        current_support + peer_inclusion + current_stress + chronic_stress +
        play_restriction + play_space_quality + adult_responsiveness +
        inclusion_climate + outdoor_safety + play_material_access +
        play_support_context
        """,
        data=model_data,
    ).fit(cov_type="HC3")

    profile_model = smf.ols(
        """
        development_score ~ time + chronic_stress + current_stress +
        play_restriction + peer_inclusion + play_support_context +
        C(play_profile)
        """,
        data=panel,
    ).fit(cov_type="HC3")

    with open(OUT / "python_play_development_model_summary.txt", "w", encoding="utf-8") as f:
        f.write("DYNAMIC PLAY DEVELOPMENT MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(model.summary().as_text())
        f.write("\n\nPLAY PROFILE MODEL\n")
        f.write("=" * 80 + "\n")
        f.write(profile_model.summary().as_text())

    trajectory = panel.groupby(["time", "chronic_stress"], as_index=False).agg(
        average_development=("development_score", "mean"),
        average_pretend=("current_pretend", "mean"),
        average_social_play=("current_social_play", "mean"),
        average_constructive=("current_constructive", "mean"),
        average_outdoor=("current_outdoor", "mean"),
        average_stress=("current_stress", "mean"),
        average_restriction=("play_restriction", "mean"),
        average_peer_inclusion=("peer_inclusion", "mean"),
        average_play_support_context=("play_support_context", "mean"),
        standard_error=("development_score", lambda x: x.std() / (len(x) ** 0.5)),
    )
    trajectory["stress_group"] = trajectory["chronic_stress"].map({
        0: "Lower chronic stress",
        1: "Higher chronic stress",
    })
    trajectory.to_csv(OUT / "python_stress_play_development_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for label, group in trajectory.groupby("stress_group"):
        plt.plot(group["time"], group["average_development"], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average development score")
    plt.title("Synthetic Play, Imagination, and Development Across Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "python_stress_play_development_trajectory.png", dpi=160)
    plt.close()

    context = panel.groupby("time", as_index=False).agg(
        average_pretend=("current_pretend", "mean"),
        average_social_play=("current_social_play", "mean"),
        average_constructive=("current_constructive", "mean"),
        average_outdoor=("current_outdoor", "mean"),
        average_support=("current_support", "mean"),
        average_peer_inclusion=("peer_inclusion", "mean"),
        average_restriction=("play_restriction", "mean"),
        average_stress=("current_stress", "mean"),
        average_play_context=("play_support_context", "mean"),
        average_development=("development_score", "mean"),
    )
    context.to_csv(OUT / "python_play_context_trajectory.csv", index=False)

    plt.figure(figsize=(8, 5))
    for col, label in [
        ("average_pretend", "pretend play"),
        ("average_social_play", "social play"),
        ("average_constructive", "constructive play"),
        ("average_outdoor", "outdoor play"),
        ("average_restriction", "play restriction"),
        ("average_play_context", "play context"),
    ]:
        plt.plot(context["time"], context[col], marker="o", label=label)
    plt.xlabel("Time")
    plt.ylabel("Average index")
    plt.title("Synthetic Play Context Across Time")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "python_play_context_trajectory.png", dpi=160)
    plt.close()

    panel.groupby("play_profile", as_index=False).agg(
        children=("child_id", "nunique"),
        average_development=("development_score", "mean"),
        average_play_support_context=("play_support_context", "mean"),
        average_play_restriction=("play_restriction", "mean"),
        average_stress=("current_stress", "mean"),
        average_peer_inclusion=("peer_inclusion", "mean"),
        chronic_stress_rate=("chronic_stress", "mean"),
    ).to_csv(OUT / "python_play_development_profiles.csv", index=False)

    panel.groupby("context_id", as_index=False).agg(
        play_space_quality=("play_space_quality", "mean"),
        adult_responsiveness=("adult_responsiveness", "mean"),
        inclusion_climate=("inclusion_climate", "mean"),
        outdoor_safety=("outdoor_safety", "mean"),
        play_material_access=("play_material_access", "mean"),
        average_development=("development_score", "mean"),
        average_play_support_context=("play_support_context", "mean"),
        average_play_restriction=("play_restriction", "mean"),
        average_peer_inclusion=("peer_inclusion", "mean"),
    ).to_csv(OUT / "python_play_context_summary.csv", index=False)

    print("Wrote Python play development model outputs.")

if __name__ == "__main__":
    main()
