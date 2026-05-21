# Rust

The Rust utility validates that the generated CSV contains the expected parenting and family-systems schema.

Run:

```bash
rustc rust/validate_family_systems_panel.rs -o outputs/validate_family_systems_panel_rust
./outputs/validate_family_systems_panel_rust data/family_systems_panel.csv
```
