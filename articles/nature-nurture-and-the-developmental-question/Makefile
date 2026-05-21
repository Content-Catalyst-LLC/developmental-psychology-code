.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_nature_nurture_panel.py

python: data
>python3 python/model_nature_nurture_development.py

scenarios: data
>python3 python/nature_nurture_scenario_analysis.py

r: data
>Rscript r/model_nature_nurture_development.R

c: data
>gcc c/nature_nurture_summary.c -o outputs/nature_nurture_summary_c
>./outputs/nature_nurture_summary_c data/nature_nurture_development_panel.csv

cpp: data
>g++ -std=c++17 cpp/nature_nurture_summary.cpp -o outputs/nature_nurture_summary_cpp
>./outputs/nature_nurture_summary_cpp data/nature_nurture_development_panel.csv

go: data
>go run go/nature_nurture_summary.go data/nature_nurture_development_panel.csv

rust: data
>rustc rust/validate_nature_nurture_panel.rs -o outputs/validate_nature_nurture_panel_rust
>./outputs/validate_nature_nurture_panel_rust data/nature_nurture_development_panel.csv

julia:
>julia julia/simulate_nature_nurture.jl

fortran:
>gfortran fortran/nature_nurture_simulation.f90 -o outputs/nature_nurture_fortran
>./outputs/nature_nurture_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png
>rm -f outputs/nature_nurture_summary_c
>rm -f outputs/nature_nurture_summary_cpp
>rm -f outputs/validate_nature_nurture_panel_rust
>rm -f outputs/nature_nurture_fortran
