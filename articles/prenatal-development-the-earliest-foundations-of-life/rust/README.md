# Rust

The Rust utility validates that the generated CSV contains the expected prenatal-development schema.

Run:

```bash
rustc rust/validate_prenatal_development_panel.rs -o outputs/validate_prenatal_development_panel_rust
./outputs/validate_prenatal_development_panel_rust data/prenatal_development_foundations_panel.csv
```
