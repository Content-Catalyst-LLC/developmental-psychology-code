.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_temperament_panel.py

python: data
>python3 python/model_temperament_goodness_of_fit.py

scenarios: data
>python3 python/temperament_scenario_analysis.py

r: data
>Rscript r/model_temperament_goodness_of_fit.R

c: data
>gcc c/temperament_summary.c -o outputs/temperament_summary_c
>./outputs/temperament_summary_c data/temperament_individual_differences_panel.csv

cpp: data
>g++ -std=c++17 cpp/temperament_summary.cpp -o outputs/temperament_summary_cpp
>./outputs/temperament_summary_cpp data/temperament_individual_differences_panel.csv

go: data
>go run go/temperament_summary.go data/temperament_individual_differences_panel.csv

rust: data
>rustc rust/validate_temperament_panel.rs -o outputs/validate_temperament_panel_rust
>./outputs/validate_temperament_panel_rust data/temperament_individual_differences_panel.csv

julia:
>julia julia/simulate_temperament_goodness_of_fit.jl

fortran:
>gfortran fortran/temperament_goodness_of_fit_simulation.f90 -o outputs/temperament_fortran
>./outputs/temperament_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png
>rm -f outputs/temperament_summary_c
>rm -f outputs/temperament_summary_cpp
>rm -f outputs/validate_temperament_panel_rust
>rm -f outputs/temperament_fortran
