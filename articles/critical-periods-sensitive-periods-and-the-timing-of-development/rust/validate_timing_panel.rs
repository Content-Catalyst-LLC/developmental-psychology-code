use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: rustc validate_timing_panel.rs -o validate && ./validate data/developmental_timing_panel.csv");
        std::process::exit(1);
    }

    let content = fs::read_to_string(&args[1]).expect("Unable to read CSV file");
    let mut lines = content.lines();

    let header = lines.next().expect("Missing header");
    let columns: Vec<&str> = header.split(',').collect();

    let required = [
        "person_id",
        "context_id",
        "time",
        "experience",
        "critical_weight",
        "early_sensitive_weight",
        "adolescent_sensitive_weight",
        "critical_outcome",
        "sensitive_outcome",
        "multi_window_outcome",
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
