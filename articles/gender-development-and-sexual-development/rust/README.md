# Rust

The Rust utility validates that the generated CSV contains the expected gender/sexual-development schema.

Run:

```bash
rustc rust/validate_gender_sexual_development_panel.rs -o outputs/validate_gender_sexual_development_panel_rust
./outputs/validate_gender_sexual_development_panel_rust data/gender_sexual_development_panel.csv
```
