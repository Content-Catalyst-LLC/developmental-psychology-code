.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_adult_development_panel.py

python: data
>python3 python/model_adult_development.py

scenarios: data
>python3 python/adult_development_scenario_analysis.py

r: data
>Rscript r/model_adult_development.R

c: data
>gcc c/adult_development_summary.c -o outputs/adult_development_summary_c
>./outputs/adult_development_summary_c data/adult_development_life_stages_panel.csv

cpp: data
>g++ -std=c++17 cpp/adult_development_summary.cpp -o outputs/adult_development_summary_cpp
>./outputs/adult_development_summary_cpp data/adult_development_life_stages_panel.csv

go: data
>go run go/adult_development_summary.go data/adult_development_life_stages_panel.csv

rust: data
>rustc rust/validate_adult_development_panel.rs -o outputs/validate_adult_development_panel_rust
>./outputs/validate_adult_development_panel_rust data/adult_development_life_stages_panel.csv

julia:
>julia julia/simulate_adult_development.jl

fortran:
>gfortran fortran/adult_development_simulation.f90 -o outputs/adult_development_fortran
>./outputs/adult_development_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png
>rm -f outputs/adult_development_summary_c
>rm -f outputs/adult_development_summary_cpp
>rm -f outputs/validate_adult_development_panel_rust
>rm -f outputs/adult_development_fortran
