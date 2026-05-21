use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: rustc validate_gender_sexual_development_panel.rs -o validate && ./validate data/gender_sexual_development_panel.csv");
        std::process::exit(1);
    }

    let content = fs::read_to_string(&args[1]).expect("Unable to read CSV file");
    let mut lines = content.lines();
    let header = lines.next().expect("Missing header");
    let columns: Vec<&str> = header.split(',').collect();

    let required = [
        "id",
        "school_id",
        "time",
        "baseline_adjustment",
        "family_support",
        "social_recognition",
        "consent_knowledge",
        "school_connectedness",
        "chronic_stigma",
        "school_climate",
        "health_education_quality",
        "anti_harassment_support",
        "pubertal_progress",
        "current_family_support",
        "current_recognition",
        "current_consent_knowledge",
        "current_connectedness",
        "current_stigma",
        "protective_context",
        "adjustment_score",
        "development_profile",
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
