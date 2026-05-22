use std::{env, fs};
fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 { eprintln!("usage: validate_language_development_panel data/language_development_panel.csv"); std::process::exit(1); }
    let txt = fs::read_to_string(&args[1]).expect("read csv");
    let mut lines = txt.lines();
    let header = lines.next().expect("header");
    let cols: Vec<&str> = header.split(',').collect();
    let required = ["child_id","context_id","time","baseline_language","responsive_interaction","shared_reading","joint_attention","conversational_turns","hearing_support","multilingual_exposure","chronic_stress","language_ecology_support","book_access","early_education_quality","home_language_recognition","current_interaction","current_reading","current_joint_attention","current_turn_taking","current_stress","language_support_context","language_score","language_profile"];
    for r in required { if !cols.contains(&r) { eprintln!("missing column: {}", r); std::process::exit(1); } }
    println!("CSV validation passed. Rows: {} Columns: {}", lines.count(), cols.len());
}
