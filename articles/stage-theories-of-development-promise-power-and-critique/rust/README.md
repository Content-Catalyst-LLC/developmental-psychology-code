# Rust

The Rust utility validates that the generated CSV contains the expected stage-theory schema.

Run:

```bash
rustc rust/validate_stage_theory_panel.rs -o outputs/validate_stage_theory_panel_rust
./outputs/validate_stage_theory_panel_rust data/stage_theory_development_panel.csv
```
