.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_continuity_discontinuity_panel.py

python: data
>python3 python/model_continuity_discontinuity.py

scenarios: data
>python3 python/developmental_turning_point_scenarios.py

r: data
>Rscript r/model_continuity_discontinuity.R

c: data
>gcc c/continuity_discontinuity_summary.c -o outputs/continuity_discontinuity_summary_c
>./outputs/continuity_discontinuity_summary_c data/continuity_discontinuity_panel.csv

cpp: data
>g++ -std=c++17 cpp/continuity_discontinuity_summary.cpp -o outputs/continuity_discontinuity_summary_cpp
>./outputs/continuity_discontinuity_summary_cpp data/continuity_discontinuity_panel.csv

go: data
>go run go/continuity_discontinuity_summary.go data/continuity_discontinuity_panel.csv

rust: data
>rustc rust/validate_continuity_discontinuity_panel.rs -o outputs/validate_continuity_discontinuity_panel_rust
>./outputs/validate_continuity_discontinuity_panel_rust data/continuity_discontinuity_panel.csv

julia:
>julia julia/simulate_continuity_discontinuity.jl

fortran:
>gfortran fortran/continuity_discontinuity_simulation.f90 -o outputs/continuity_discontinuity_fortran
>./outputs/continuity_discontinuity_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png
>rm -f outputs/continuity_discontinuity_summary_c
>rm -f outputs/continuity_discontinuity_summary_cpp
>rm -f outputs/validate_continuity_discontinuity_panel_rust
>rm -f outputs/continuity_discontinuity_fortran
