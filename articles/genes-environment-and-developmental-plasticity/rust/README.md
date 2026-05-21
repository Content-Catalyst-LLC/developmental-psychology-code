# Rust

The Rust utility validates that the generated CSV contains the expected genes-environment-plasticity schema.

Run:

```bash
rustc rust/validate_plasticity_panel.rs -o outputs/validate_plasticity_panel_rust
./outputs/validate_plasticity_panel_rust data/genes_environment_plasticity_panel.csv
```
