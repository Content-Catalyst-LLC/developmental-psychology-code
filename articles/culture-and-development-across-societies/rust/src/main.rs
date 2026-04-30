fn developmental_score(care: f64, opportunity: f64, regulation: f64, resilience: f64, risk: f64) -> f64 {
    0.22 * care + 0.20 * opportunity + 0.20 * regulation + 0.18 * resilience - 0.20 * risk
}

fn main() {
    let score = developmental_score(0.8, 0.7, 0.65, 0.75, 0.25);
    println!("Developmental score: {:.3}", score);
}
