use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: rustc validate_aging_adaptation_panel.rs -o validate && ./validate data/aging_adaptation_later_life_panel.csv");
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
        "baseline_adjustment",
        "functional_ability",
        "social_support",
        "health_burden",
        "adaptive_strategy",
        "meaning_orientation",
        "environmental_accessibility",
        "dignity_support",
        "service_access",
        "current_function",
        "current_support",
        "current_health",
        "current_adaptation",
        "current_meaning",
        "functional_fit",
        "adjustment_score",
        "adaptation_profile",
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
