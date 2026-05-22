.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_play_development_panel.py

python: data
>python3 python/model_play_development.py

scenarios: data
>python3 python/play_development_scenarios.py

r: data
>Rscript r/model_play_development.R

c: data
>gcc c/play_development_summary.c -o outputs/play_development_summary_c
>./outputs/play_development_summary_c data/play_development_panel.csv

cpp: data
>g++ -std=c++17 cpp/play_development_summary.cpp -o outputs/play_development_summary_cpp
>./outputs/play_development_summary_cpp data/play_development_panel.csv

go: data
>go run go/play_development_summary.go data/play_development_panel.csv

rust: data
>rustc rust/validate_play_development_panel.rs -o outputs/validate_play_development_panel_rust
>./outputs/validate_play_development_panel_rust data/play_development_panel.csv

julia:
>julia julia/simulate_play_development.jl

fortran:
>gfortran fortran/play_development_simulation.f90 -o outputs/play_development_fortran
>./outputs/play_development_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/*_c outputs/*_cpp outputs/*_rust outputs/*_fortran
