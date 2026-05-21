# Rust

The Rust utility validates that the generated CSV contains the expected aging adaptation schema.

Run:

```bash
rustc rust/validate_aging_adaptation_panel.rs -o outputs/validate_aging_adaptation_panel_rust
./outputs/validate_aging_adaptation_panel_rust data/aging_adaptation_later_life_panel.csv
```
