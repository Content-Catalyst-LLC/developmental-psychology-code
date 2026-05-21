# Rust

The Rust utility validates that the generated CSV contains the expected lifespan Baltes schema.

Run:

```bash
rustc rust/validate_lifespan_baltes_panel.rs -o outputs/validate_lifespan_baltes_panel_rust
./outputs/validate_lifespan_baltes_panel_rust data/lifespan_baltes_panel.csv
```
