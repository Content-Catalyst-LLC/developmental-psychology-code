.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_wisdom_meaning_panel.py

python: data
>python3 python/model_wisdom_meaning.py

scenarios: data
>python3 python/wisdom_meaning_scenario_analysis.py

r: data
>Rscript r/model_wisdom_meaning.R

c: data
>gcc c/wisdom_meaning_summary.c -o outputs/wisdom_meaning_summary_c
>./outputs/wisdom_meaning_summary_c data/wisdom_meaning_later_life_panel.csv

cpp: data
>g++ -std=c++17 cpp/wisdom_meaning_summary.cpp -o outputs/wisdom_meaning_summary_cpp
>./outputs/wisdom_meaning_summary_cpp data/wisdom_meaning_later_life_panel.csv

go: data
>go run go/wisdom_meaning_summary.go data/wisdom_meaning_later_life_panel.csv

rust: data
>rustc rust/validate_wisdom_meaning_panel.rs -o outputs/validate_wisdom_meaning_panel_rust
>./outputs/validate_wisdom_meaning_panel_rust data/wisdom_meaning_later_life_panel.csv

julia:
>julia julia/simulate_wisdom_meaning.jl

fortran:
>gfortran fortran/wisdom_meaning_simulation.f90 -o outputs/wisdom_meaning_fortran
>./outputs/wisdom_meaning_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png
>rm -f outputs/wisdom_meaning_summary_c
>rm -f outputs/wisdom_meaning_summary_cpp
>rm -f outputs/validate_wisdom_meaning_panel_rust
>rm -f outputs/wisdom_meaning_fortran
