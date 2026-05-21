.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_lifespan_baltes_panel.py

python: data
>python3 python/model_lifespan_baltes.py

scenarios: data
>python3 python/lifespan_scenario_analysis.py

r: data
>Rscript r/model_lifespan_baltes.R

c: data
>gcc c/lifespan_baltes_summary.c -o outputs/lifespan_baltes_summary_c
>./outputs/lifespan_baltes_summary_c data/lifespan_baltes_panel.csv

cpp: data
>g++ -std=c++17 cpp/lifespan_baltes_summary.cpp -o outputs/lifespan_baltes_summary_cpp
>./outputs/lifespan_baltes_summary_cpp data/lifespan_baltes_panel.csv

go: data
>go run go/lifespan_baltes_summary.go data/lifespan_baltes_panel.csv

rust: data
>rustc rust/validate_lifespan_baltes_panel.rs -o outputs/validate_lifespan_baltes_panel_rust
>./outputs/validate_lifespan_baltes_panel_rust data/lifespan_baltes_panel.csv

julia:
>julia julia/simulate_lifespan_baltes.jl

fortran:
>gfortran fortran/lifespan_baltes_simulation.f90 -o outputs/lifespan_baltes_fortran
>./outputs/lifespan_baltes_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png
>rm -f outputs/lifespan_baltes_summary_c
>rm -f outputs/lifespan_baltes_summary_cpp
>rm -f outputs/validate_lifespan_baltes_panel_rust
>rm -f outputs/lifespan_baltes_fortran
