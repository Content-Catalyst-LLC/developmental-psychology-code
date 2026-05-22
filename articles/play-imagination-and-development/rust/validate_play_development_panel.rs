use std::{env, fs};
fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 { eprintln!("usage: validate_play_development_panel data/play_development_panel.csv"); std::process::exit(1); }
    let txt = fs::read_to_string(&args[1]).expect("read csv");
    let mut lines = txt.lines();
    let header = lines.next().expect("header");
    let cols: Vec<&str> = header.split(',').collect();
    let required = ["child_id","context_id","time","baseline_development","pretend_play_base","social_play_base","constructive_play_base","outdoor_play_base","caregiver_support_base","chronic_stress","play_space_quality","adult_responsiveness","inclusion_climate","outdoor_safety","play_material_access","current_pretend","current_social_play","current_constructive","current_outdoor","current_support","current_stress","play_restriction","peer_inclusion","play_support_context","development_score","play_profile"];
    for r in required { if !cols.contains(&r) { eprintln!("missing column: {}", r); std::process::exit(1); } }
    println!("CSV validation passed. Rows: {} Columns: {}", lines.count(), cols.len());
}
