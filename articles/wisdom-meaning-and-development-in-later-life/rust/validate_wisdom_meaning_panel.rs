use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: rustc validate_wisdom_meaning_panel.rs -o validate && ./validate data/wisdom_meaning_later_life_panel.csv");
        std::process::exit(1);
    }

    let content = fs::read_to_string(&args[1]).expect("Unable to read CSV file");
    let mut lines = content.lines();
    let header = lines.next().expect("Missing header");
    let columns: Vec<&str> = header.split(',').collect();

    let required = [
        "id",
        "care_context_id",
        "time",
        "baseline_meaning",
        "social_connection",
        "reflective_integration",
        "health_burden",
        "adaptive_support",
        "legacy_orientation",
        "dignity_support",
        "service_access",
        "community_participation",
        "current_connection",
        "current_reflection",
        "current_health",
        "current_support",
        "current_legacy",
        "wisdom_index",
        "meaning_score",
        "meaning_profile",
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
