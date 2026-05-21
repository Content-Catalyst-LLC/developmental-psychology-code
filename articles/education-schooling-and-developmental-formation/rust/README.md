# Rust

The Rust utility validates that the generated CSV contains the expected schooling-development schema.

Run:

```bash
rustc rust/validate_schooling_panel.rs -o outputs/validate_schooling_panel_rust
./outputs/validate_schooling_panel_rust data/schooling_development_panel.csv
```
