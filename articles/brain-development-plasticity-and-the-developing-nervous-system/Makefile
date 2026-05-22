.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_brain_development_panel.py

python: data
>python3 python/model_brain_development.py

scenarios: data
>python3 python/neurodevelopment_support_scenarios.py

r: data
>Rscript r/model_brain_development.R

c: data
>gcc c/brain_development_summary.c -o outputs/brain_development_summary_c
>./outputs/brain_development_summary_c data/brain_development_panel.csv

cpp: data
>g++ -std=c++17 cpp/brain_development_summary.cpp -o outputs/brain_development_summary_cpp
>./outputs/brain_development_summary_cpp data/brain_development_panel.csv

go: data
>go run go/brain_development_summary.go data/brain_development_panel.csv

rust: data
>rustc rust/validate_brain_development_panel.rs -o outputs/validate_brain_development_panel_rust
>./outputs/validate_brain_development_panel_rust data/brain_development_panel.csv

julia:
>julia julia/simulate_brain_development.jl

fortran:
>gfortran fortran/brain_development_simulation.f90 -o outputs/brain_development_fortran
>./outputs/brain_development_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/*_c outputs/*_cpp outputs/*_rust outputs/*_fortran
