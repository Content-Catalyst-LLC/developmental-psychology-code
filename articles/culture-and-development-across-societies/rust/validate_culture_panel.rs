use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: rustc validate_culture_panel.rs -o validate && ./validate data/cultural_development_panel.csv");
        std::process::exit(1);
    }

    let content = fs::read_to_string(&args[1]).expect("Unable to read CSV file");
    let mut lines = content.lines();

    let header = lines.next().expect("Missing header");
    let columns: Vec<&str> = header.split(',').collect();

    let required = [
        "child_id",
        "society_id",
        "time",
        "current_family",
        "current_fit",
        "current_mismatch",
        "current_support",
        "development_score",
        "cultural_condition",
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
