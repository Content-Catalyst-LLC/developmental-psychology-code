use std::{env, fs};
fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 { eprintln!("usage: validate_attachment_development_panel data/attachment_development_panel.csv"); std::process::exit(1); }
    let txt = fs::read_to_string(&args[1]).expect("read csv");
    let mut lines = txt.lines();
    let header = lines.next().expect("header");
    let cols: Vec<&str> = header.split(',').collect();
    let required = ["child_id","context_id","time","baseline_regulation","caregiving_quality","repair_capacity","caregiver_support","temperament_reactivity","disability_support_need","chronic_stress","childcare_continuity","neighborhood_safety","family_service_access","caregiving_ecology_support","current_care","current_repair","current_caregiver_support","current_stress","caregiving_support_context","regulation_score","attachment_profile"];
    for r in required { if !cols.contains(&r) { eprintln!("missing column: {}", r); std::process::exit(1); } }
    println!("CSV validation passed. Rows: {} Columns: {}", lines.count(), cols.len());
}
