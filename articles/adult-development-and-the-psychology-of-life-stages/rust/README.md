# Rust

The Rust utility validates that the generated CSV contains the expected adult-development schema.

Run:

```bash
rustc rust/validate_adult_development_panel.rs -o outputs/validate_adult_development_panel_rust
./outputs/validate_adult_development_panel_rust data/adult_development_life_stages_panel.csv
```
