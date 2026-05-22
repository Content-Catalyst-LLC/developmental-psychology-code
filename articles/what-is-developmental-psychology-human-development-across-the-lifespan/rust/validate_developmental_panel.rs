use std::{env, fs};

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("usage: validate_developmental_panel data/developmental_lifespan_panel.csv");
        std::process::exit(1);
    }

    let txt = fs::read_to_string(&args[1]).expect("read csv");
    let mut lines = txt.lines();
    let header = lines.next().expect("header");
    let cols: Vec<&str> = header.split(',').collect();

    let required = [
        "child_id",
        "school_id",
        "time",
        "baseline_regulation",
        "caregiver_support",
        "family_support",
        "school_support",
        "disability_support_need",
        "structural_risk",
        "school_climate",
        "disability_accommodation",
        "counseling_access",
        "language_access",
        "community_resource_index",
        "acute_stress",
        "current_support",
        "intervention",
        "protective_context",
        "development_score",
        "development_profile",
    ];

    for r in required {
        if !cols.contains(&r) {
            eprintln!("missing column: {}", r);
            std::process::exit(1);
        }
    }

    println!("CSV validation passed. Rows: {} Columns: {}", lines.count(), cols.len());
}
