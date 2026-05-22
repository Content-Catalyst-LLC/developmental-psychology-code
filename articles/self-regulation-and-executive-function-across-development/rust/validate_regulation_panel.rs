use std::{env, fs};
fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 { eprintln!("usage: validate_regulation_panel data/regulation_development_panel.csv"); std::process::exit(1); }
    let txt = fs::read_to_string(&args[1]).expect("read csv");
    let mut lines = txt.lines();
    let header = lines.next().expect("header");
    let cols: Vec<&str> = header.split(',').collect();
    let required = ["child_id","school_id","time","baseline_ef","caregiving_support","classroom_structure","sleep_quality","chronic_stress","temperament_reactivity","disability_support_need","school_climate","regulation_scaffolding","disability_accommodation","transition_predictability","current_support","current_structure","current_sleep","acute_stress","intervention_exposure","regulatory_support_context","regulation_score","regulation_profile"];
    for r in required { if !cols.contains(&r) { eprintln!("missing column: {}", r); std::process::exit(1); } }
    println!("CSV validation passed. Rows: {} Columns: {}", lines.count(), cols.len());
}
