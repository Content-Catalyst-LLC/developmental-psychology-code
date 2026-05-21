# Rust

The Rust utility validates that the generated CSV contains the expected temperament schema.

Run:

```bash
rustc rust/validate_temperament_panel.rs -o outputs/validate_temperament_panel_rust
./outputs/validate_temperament_panel_rust data/temperament_individual_differences_panel.csv
```
