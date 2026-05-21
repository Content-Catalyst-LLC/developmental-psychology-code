use std::{env, fs};

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("usage: validate_history_panel data/developmental_psychology_history_panel.csv");
        std::process::exit(1);
    }

    let txt = fs::read_to_string(&args[1]).expect("read csv");
    let mut lines = txt.lines();
    let header = lines.next().expect("header");
    let cols: Vec<&str> = header.split(',').collect();

    let required = [
        "year",
        "child_study",
        "cognitive_developmental",
        "ecological",
        "lifespan",
        "developmental_systems",
        "institutional_support",
        "methodological_advantage",
        "social_relevance",
        "critique_index",
        "broadening_index",
    ];

    for r in required {
        if !cols.contains(&r) {
            eprintln!("missing column: {}", r);
            std::process::exit(1);
        }
    }

    println!("CSV validation passed. Rows: {} Columns: {}", lines.count(), cols.len());
}
