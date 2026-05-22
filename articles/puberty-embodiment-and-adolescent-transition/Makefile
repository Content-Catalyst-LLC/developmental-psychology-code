.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_puberty_embodiment_panel.py

python: data
>python3 python/model_puberty_embodiment.py

scenarios: data
>python3 python/puberty_transition_scenarios.py

r: data
>Rscript r/model_puberty_embodiment.R

c: data
>gcc c/puberty_summary.c -o outputs/puberty_summary_c
>./outputs/puberty_summary_c data/puberty_embodiment_panel.csv

cpp: data
>g++ -std=c++17 cpp/puberty_summary.cpp -o outputs/puberty_summary_cpp
>./outputs/puberty_summary_cpp data/puberty_embodiment_panel.csv

go: data
>go run go/puberty_summary.go data/puberty_embodiment_panel.csv

rust: data
>rustc rust/validate_puberty_panel.rs -o outputs/validate_puberty_panel_rust
>./outputs/validate_puberty_panel_rust data/puberty_embodiment_panel.csv

julia:
>julia julia/simulate_puberty_embodiment.jl

fortran:
>gfortran fortran/puberty_embodiment_simulation.f90 -o outputs/puberty_embodiment_fortran
>./outputs/puberty_embodiment_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/*_c outputs/*_cpp outputs/*_rust outputs/*_fortran
