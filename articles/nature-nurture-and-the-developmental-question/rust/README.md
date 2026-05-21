# Rust

The Rust utility validates that the generated CSV contains the expected nature-nurture schema.

Run:

```bash
rustc rust/validate_nature_nurture_panel.rs -o outputs/validate_nature_nurture_panel_rust
./outputs/validate_nature_nurture_panel_rust data/nature_nurture_development_panel.csv
```
