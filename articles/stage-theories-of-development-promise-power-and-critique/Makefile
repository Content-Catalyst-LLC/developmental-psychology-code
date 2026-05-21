.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_stage_theory_panel.py

python: data
>python3 python/model_stage_like_development.py

scenarios: data
>python3 python/stage_transition_scenario_analysis.py

r: data
>Rscript r/model_stage_like_development.R

c: data
>gcc c/stage_theory_summary.c -o outputs/stage_theory_summary_c
>./outputs/stage_theory_summary_c data/stage_theory_development_panel.csv

cpp: data
>g++ -std=c++17 cpp/stage_theory_summary.cpp -o outputs/stage_theory_summary_cpp
>./outputs/stage_theory_summary_cpp data/stage_theory_development_panel.csv

go: data
>go run go/stage_theory_summary.go data/stage_theory_development_panel.csv

rust: data
>rustc rust/validate_stage_theory_panel.rs -o outputs/validate_stage_theory_panel_rust
>./outputs/validate_stage_theory_panel_rust data/stage_theory_development_panel.csv

julia:
>julia julia/simulate_stage_like_development.jl

fortran:
>gfortran fortran/stage_like_development_simulation.f90 -o outputs/stage_like_development_fortran
>./outputs/stage_like_development_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png
>rm -f outputs/stage_theory_summary_c
>rm -f outputs/stage_theory_summary_cpp
>rm -f outputs/validate_stage_theory_panel_rust
>rm -f outputs/stage_like_development_fortran
