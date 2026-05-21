.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_prenatal_development_panel.py

python: data
>python3 python/model_prenatal_development.py

scenarios: data
>python3 python/prenatal_scenario_analysis.py

r: data
>Rscript r/model_prenatal_development.R

c: data
>gcc c/prenatal_development_summary.c -o outputs/prenatal_development_summary_c
>./outputs/prenatal_development_summary_c data/prenatal_development_foundations_panel.csv

cpp: data
>g++ -std=c++17 cpp/prenatal_development_summary.cpp -o outputs/prenatal_development_summary_cpp
>./outputs/prenatal_development_summary_cpp data/prenatal_development_foundations_panel.csv

go: data
>go run go/prenatal_development_summary.go data/prenatal_development_foundations_panel.csv

rust: data
>rustc rust/validate_prenatal_development_panel.rs -o outputs/validate_prenatal_development_panel_rust
>./outputs/validate_prenatal_development_panel_rust data/prenatal_development_foundations_panel.csv

julia:
>julia julia/simulate_prenatal_development.jl

fortran:
>gfortran fortran/prenatal_development_simulation.f90 -o outputs/prenatal_development_fortran
>./outputs/prenatal_development_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png
>rm -f outputs/prenatal_development_summary_c
>rm -f outputs/prenatal_development_summary_cpp
>rm -f outputs/validate_prenatal_development_panel_rust
>rm -f outputs/prenatal_development_fortran
