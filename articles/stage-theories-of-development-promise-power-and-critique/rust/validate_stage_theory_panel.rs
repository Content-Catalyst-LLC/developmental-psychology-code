use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: rustc validate_stage_theory_panel.rs -o validate && ./validate data/stage_theory_development_panel.csv");
        std::process::exit(1);
    }

    let content = fs::read_to_string(&args[1]).expect("Unable to read CSV file");
    let mut lines = content.lines();
    let header = lines.next().expect("Missing header");
    let columns: Vec<&str> = header.split(',').collect();

    let required = [
        "child_id",
        "context_id",
        "time",
        "baseline_functioning",
        "growth_rate",
        "support_context",
        "chronic_stress",
        "threshold_time",
        "stage_pattern",
        "school_support",
        "resource_stability",
        "current_support",
        "threshold_on",
        "logistic_transition",
        "transition_readiness",
        "development_score",
        "stage_profile",
    ];

    for required_column in required {
        if !columns.contains(&required_column) {
            eprintln!("Missing required column: {}", required_column);
            std::process::exit(1);
        }
    }

    println!("CSV validation passed.");
    println!("Rows: {}", lines.count());
    println!("Columns: {}", columns.len());
}
