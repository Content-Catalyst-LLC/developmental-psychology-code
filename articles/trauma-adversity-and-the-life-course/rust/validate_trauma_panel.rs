use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: rustc validate_trauma_panel.rs -o validate && ./validate data/trauma_life_course_panel.csv");
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
        "current_adversity",
        "current_support",
        "current_stability",
        "cumulative_adversity",
        "adaptation_score",
        "adversity_support_profile",
    ];

    for required_column in required {
        if !columns.contains(&required_column) {
            eprintln!("Missing required column: {}", required_column);
            std::process::exit(1);
        }
    }

    let row_count = lines.count();
    println!("CSV validation passed.");
    println!("Rows: {}", row_count);
    println!("Columns: {}", columns.len());
}
