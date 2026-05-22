.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_language_development_panel.py

python: data
>python3 python/model_language_development.py

scenarios: data
>python3 python/language_support_scenarios.py

r: data
>Rscript r/model_language_development.R

c: data
>gcc c/language_development_summary.c -o outputs/language_development_summary_c
>./outputs/language_development_summary_c data/language_development_panel.csv

cpp: data
>g++ -std=c++17 cpp/language_development_summary.cpp -o outputs/language_development_summary_cpp
>./outputs/language_development_summary_cpp data/language_development_panel.csv

go: data
>go run go/language_development_summary.go data/language_development_panel.csv

rust: data
>rustc rust/validate_language_development_panel.rs -o outputs/validate_language_development_panel_rust
>./outputs/validate_language_development_panel_rust data/language_development_panel.csv

julia:
>julia julia/simulate_language_development.jl

fortran:
>gfortran fortran/language_development_simulation.f90 -o outputs/language_development_fortran
>./outputs/language_development_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/*_c outputs/*_cpp outputs/*_rust outputs/*_fortran
