use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: rustc validate_temperament_panel.rs -o validate && ./validate data/temperament_individual_differences_panel.csv");
        std::process::exit(1);
    }

    let content = fs::read_to_string(&args[1]).expect("Unable to read CSV file");
    let mut lines = content.lines();
    let header = lines.next().expect("Missing header");
    let columns: Vec<&str> = header.split(',').collect();

    let required = [
        "child_id",
        "classroom_id",
        "time",
        "temperament_reactivity",
        "inhibition",
        "activity_level",
        "baseline_adjustment",
        "chronic_stress",
        "family_support",
        "school_fit",
        "classroom_structure",
        "teacher_responsiveness",
        "movement_flexibility",
        "current_support",
        "current_school_fit",
        "acute_stress",
        "current_accommodation",
        "goodness_of_fit",
        "adjustment_score",
        "temperament_profile",
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
