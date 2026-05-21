use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: rustc validate_prenatal_development_panel.rs -o validate && ./validate data/prenatal_development_foundations_panel.csv");
        std::process::exit(1);
    }

    let content = fs::read_to_string(&args[1]).expect("Unable to read CSV file");
    let mut lines = content.lines();
    let header = lines.next().expect("Missing header");
    let columns: Vec<&str> = header.split(',').collect();

    let required = [
        "case_id",
        "neighborhood_context",
        "gestational_weeks",
        "maternal_health",
        "prenatal_care",
        "chronic_stress",
        "toxic_exposure",
        "nutrition_support",
        "social_support",
        "healthcare_access",
        "environmental_burden",
        "economic_security",
        "effective_care",
        "developmental_risk",
        "early_outcome",
        "prenatal_profile",
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
