use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: rustc validate_adult_development_panel.rs -o validate && ./validate data/adult_development_life_stages_panel.csv");
        std::process::exit(1);
    }

    let content = fs::read_to_string(&args[1]).expect("Unable to read CSV file");
    let mut lines = content.lines();
    let header = lines.next().expect("Missing header");
    let columns: Vec<&str> = header.split(',').collect();

    let required = [
        "id",
        "context_id",
        "time",
        "baseline_adjustment",
        "life_stage",
        "relational_support",
        "work_integration",
        "health_burden",
        "adaptive_resources",
        "role_burden",
        "institutional_support",
        "community_stability",
        "current_relational_support",
        "current_work_integration",
        "current_health_burden",
        "current_adaptive_resources",
        "current_role_burden",
        "young_stage",
        "midlife_stage",
        "later_stage",
        "adjustment_score",
        "adult_development_profile",
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
