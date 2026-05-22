use std::{env, fs};
fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 { eprintln!("usage: validate_social_development_panel data/social_development_panel.csv"); std::process::exit(1); }
    let txt = fs::read_to_string(&args[1]).expect("read csv");
    let mut lines = txt.lines();
    let header = lines.next().expect("header");
    let cols: Vec<&str> = header.split(',').collect();
    let required = ["child_id","school_id","time","baseline_social","peer_support_base","friendship_quality_base","family_support_base","social_interpretation_skill","chronic_exclusion","school_connectedness","teacher_support","anti_bullying_climate","inclusion_climate","restorative_practice_access","current_peer_support","current_friendship_quality","current_family_support","current_social_interpretation","current_exclusion","bullying_exposure","digital_comparison_stress","social_support_context","social_self_score","social_profile"];
    for r in required { if !cols.contains(&r) { eprintln!("missing column: {}", r); std::process::exit(1); } }
    println!("CSV validation passed. Rows: {} Columns: {}", lines.count(), cols.len());
}
