use std::{env, fs};
fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 { eprintln!("usage: validate_moral_development_panel data/moral_development_panel.csv"); std::process::exit(1); }
    let txt = fs::read_to_string(&args[1]).expect("read csv");
    let mut lines = txt.lines();
    let header = lines.next().expect("header");
    let cols: Vec<&str> = header.split(',').collect();
    let required = ["child_id","school_id","time","baseline_morality","caregiving_guidance","empathic_sensitivity","peer_fairness_base","self_regulation","harm_recognition_base","chronic_exclusion","school_moral_climate","restorative_practice_access","punitive_inconsistency","anti_bullying_climate","digital_moral_safety","current_guidance","current_empathy","current_peer_fairness","current_self_regulation","current_harm_recognition","current_repair_opportunity","current_exclusion","digital_cruelty_exposure","peer_pressure","moral_support_context","conscience_score","moral_action_score","moral_profile"];
    for r in required { if !cols.contains(&r) { eprintln!("missing column: {}", r); std::process::exit(1); } }
    println!("CSV validation passed. Rows: {} Columns: {}", lines.count(), cols.len());
}
