.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_moral_development_panel.py

python: data
>python3 python/model_moral_development.py

scenarios: data
>python3 python/moral_development_scenarios.py

r: data
>Rscript r/model_moral_development.R

c: data
>gcc c/moral_development_summary.c -o outputs/moral_development_summary_c
>./outputs/moral_development_summary_c data/moral_development_panel.csv

cpp: data
>g++ -std=c++17 cpp/moral_development_summary.cpp -o outputs/moral_development_summary_cpp
>./outputs/moral_development_summary_cpp data/moral_development_panel.csv

go: data
>go run go/moral_development_summary.go data/moral_development_panel.csv

rust: data
>rustc rust/validate_moral_development_panel.rs -o outputs/validate_moral_development_panel_rust
>./outputs/validate_moral_development_panel_rust data/moral_development_panel.csv

julia:
>julia julia/simulate_moral_development.jl

fortran:
>gfortran fortran/moral_development_simulation.f90 -o outputs/moral_development_fortran
>./outputs/moral_development_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/*_c outputs/*_cpp outputs/*_rust outputs/*_fortran
