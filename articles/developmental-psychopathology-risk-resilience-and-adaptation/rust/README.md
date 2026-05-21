# Rust

The Rust utility validates that the generated CSV contains the expected developmental psychopathology schema.

Run:

```bash
rustc rust/validate_psychopathology_panel.rs -o outputs/validate_psychopathology_panel_rust
./outputs/validate_psychopathology_panel_rust data/developmental_psychopathology_panel.csv
```
