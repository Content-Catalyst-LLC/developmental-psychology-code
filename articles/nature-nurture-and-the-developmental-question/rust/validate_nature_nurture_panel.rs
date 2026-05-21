use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: rustc validate_nature_nurture_panel.rs -o validate && ./validate data/nature_nurture_development_panel.csv");
        std::process::exit(1);
    }

    let content = fs::read_to_string(&args[1]).expect("Unable to read CSV file");
    let mut lines = content.lines();
    let header = lines.next().expect("Missing header");
    let columns: Vec<&str> = header.split(',').collect();

    let required = [
        "child_id",
        "school_id",
        "time",
        "biological_sensitivity",
        "baseline_functioning",
        "structural_risk",
        "chronic_adversity",
        "family_support_context",
        "institutional_support",
        "disability_support",
        "resource_stability",
        "caregiver_support",
        "acute_stress",
        "intervention",
        "protective_context",
        "development_score",
        "sensitivity_profile",
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
