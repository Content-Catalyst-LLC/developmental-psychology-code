.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_developmental_systems_panel.py

python: data
>python3 python/model_developmental_systems.py

scenarios: data
>python3 python/systems_scenario_analysis.py

r: data
>Rscript r/model_developmental_systems.R

c: data
>gcc c/developmental_systems_summary.c -o outputs/developmental_systems_summary_c
>./outputs/developmental_systems_summary_c data/developmental_systems_panel.csv

cpp: data
>g++ -std=c++17 cpp/developmental_systems_summary.cpp -o outputs/developmental_systems_summary_cpp
>./outputs/developmental_systems_summary_cpp data/developmental_systems_panel.csv

go: data
>go run go/developmental_systems_summary.go data/developmental_systems_panel.csv

rust: data
>rustc rust/validate_developmental_systems_panel.rs -o outputs/validate_developmental_systems_panel_rust
>./outputs/validate_developmental_systems_panel_rust data/developmental_systems_panel.csv

julia:
>julia julia/simulate_developmental_systems.jl

fortran:
>gfortran fortran/developmental_systems_simulation.f90 -o outputs/developmental_systems_fortran
>./outputs/developmental_systems_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png
>rm -f outputs/developmental_systems_summary_c
>rm -f outputs/developmental_systems_summary_cpp
>rm -f outputs/validate_developmental_systems_panel_rust
>rm -f outputs/developmental_systems_fortran
