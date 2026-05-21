.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_aging_adaptation_panel.py

python: data
>python3 python/model_aging_adaptation.py

scenarios: data
>python3 python/aging_adaptation_scenario_analysis.py

r: data
>Rscript r/model_aging_adaptation.R

c: data
>gcc c/aging_adaptation_summary.c -o outputs/aging_adaptation_summary_c
>./outputs/aging_adaptation_summary_c data/aging_adaptation_later_life_panel.csv

cpp: data
>g++ -std=c++17 cpp/aging_adaptation_summary.cpp -o outputs/aging_adaptation_summary_cpp
>./outputs/aging_adaptation_summary_cpp data/aging_adaptation_later_life_panel.csv

go: data
>go run go/aging_adaptation_summary.go data/aging_adaptation_later_life_panel.csv

rust: data
>rustc rust/validate_aging_adaptation_panel.rs -o outputs/validate_aging_adaptation_panel_rust
>./outputs/validate_aging_adaptation_panel_rust data/aging_adaptation_later_life_panel.csv

julia:
>julia julia/simulate_aging_adaptation.jl

fortran:
>gfortran fortran/aging_adaptation_simulation.f90 -o outputs/aging_adaptation_fortran
>./outputs/aging_adaptation_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png
>rm -f outputs/aging_adaptation_summary_c
>rm -f outputs/aging_adaptation_summary_cpp
>rm -f outputs/validate_aging_adaptation_panel_rust
>rm -f outputs/aging_adaptation_fortran
