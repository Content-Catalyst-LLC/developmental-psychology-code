.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_developmental_lifespan_panel.py

python: data
>python3 python/model_developmental_lifespan.py

scenarios: data
>python3 python/developmental_support_scenarios.py

r: data
>Rscript r/model_developmental_lifespan.R

c: data
>gcc c/developmental_summary.c -o outputs/developmental_summary_c
>./outputs/developmental_summary_c data/developmental_lifespan_panel.csv

cpp: data
>g++ -std=c++17 cpp/developmental_summary.cpp -o outputs/developmental_summary_cpp
>./outputs/developmental_summary_cpp data/developmental_lifespan_panel.csv

go: data
>go run go/developmental_summary.go data/developmental_lifespan_panel.csv

rust: data
>rustc rust/validate_developmental_panel.rs -o outputs/validate_developmental_panel_rust
>./outputs/validate_developmental_panel_rust data/developmental_lifespan_panel.csv

julia:
>julia julia/simulate_developmental_lifespan.jl

fortran:
>gfortran fortran/developmental_lifespan_simulation.f90 -o outputs/developmental_lifespan_fortran
>./outputs/developmental_lifespan_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/*_c outputs/*_cpp outputs/*_rust outputs/*_fortran
