.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_developmental_history_panel.py

python: data
>python3 python/model_developmental_history.py

scenarios: data
>python3 python/paradigm_shift_scenarios.py

r: data
>Rscript r/model_developmental_history.R

c: data
>gcc c/history_summary.c -o outputs/history_summary_c
>./outputs/history_summary_c data/developmental_psychology_history_panel.csv

cpp: data
>g++ -std=c++17 cpp/history_summary.cpp -o outputs/history_summary_cpp
>./outputs/history_summary_cpp data/developmental_psychology_history_panel.csv

go: data
>go run go/history_summary.go data/developmental_psychology_history_panel.csv

rust: data
>rustc rust/validate_history_panel.rs -o outputs/validate_history_panel_rust
>./outputs/validate_history_panel_rust data/developmental_psychology_history_panel.csv

julia:
>julia julia/simulate_developmental_history.jl

fortran:
>gfortran fortran/developmental_history_simulation.f90 -o outputs/developmental_history_fortran
>./outputs/developmental_history_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/*_c outputs/*_cpp outputs/*_rust outputs/*_fortran
