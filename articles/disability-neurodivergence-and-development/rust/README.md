# Rust

The Rust utility validates that the generated CSV contains the expected disability/neurodivergence accessibility schema.

Run:

```bash
rustc rust/validate_accessibility_panel.rs -o outputs/validate_accessibility_panel_rust
./outputs/validate_accessibility_panel_rust data/disability_neurodivergence_panel.csv
```
