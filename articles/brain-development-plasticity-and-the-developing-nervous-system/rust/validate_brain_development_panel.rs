use std::{env, fs};
fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 { eprintln!("usage: validate_brain_development_panel data/brain_development_panel.csv"); std::process::exit(1); }
    let txt = fs::read_to_string(&args[1]).expect("read csv");
    let mut lines = txt.lines();
    let header = lines.next().expect("header");
    let cols: Vec<&str> = header.split(',').collect();
    let required = ["child_id","context_id","time","baseline_neural_state","family_support","learning_context","sleep_quality","sensory_regulation_support","chronic_stress","school_support","neighborhood_safety","health_service_access","environmental_risk","current_family_support","current_learning","current_sleep","current_sensory_support","acute_stress","developmental_support_context","neural_state","developmental_outcome","neurodevelopment_profile"];
    for r in required { if !cols.contains(&r) { eprintln!("missing column: {}", r); std::process::exit(1); } }
    println!("CSV validation passed. Rows: {} Columns: {}", lines.count(), cols.len());
}
