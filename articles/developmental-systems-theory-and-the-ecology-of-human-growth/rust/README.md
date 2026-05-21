# Rust

The Rust utility validates that the generated CSV contains the expected developmental-systems schema.

Run:

```bash
rustc rust/validate_developmental_systems_panel.rs -o outputs/validate_developmental_systems_panel_rust
./outputs/validate_developmental_systems_panel_rust data/developmental_systems_panel.csv
```
