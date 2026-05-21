# Rust

The Rust utility validates that the generated CSV contains the expected continuity/discontinuity schema.

Run:

```bash
rustc rust/validate_continuity_discontinuity_panel.rs -o outputs/validate_continuity_discontinuity_panel_rust
./outputs/validate_continuity_discontinuity_panel_rust data/continuity_discontinuity_panel.csv
```
