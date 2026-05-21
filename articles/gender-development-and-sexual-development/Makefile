.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_gender_sexual_development_panel.py

python: data
>python3 python/model_gender_sexual_development.py

scenarios: data
>python3 python/gender_sexual_development_scenario_analysis.py

r: data
>Rscript r/model_gender_sexual_development.R

c: data
>gcc c/gender_sexual_development_summary.c -o outputs/gender_sexual_development_summary_c
>./outputs/gender_sexual_development_summary_c data/gender_sexual_development_panel.csv

cpp: data
>g++ -std=c++17 cpp/gender_sexual_development_summary.cpp -o outputs/gender_sexual_development_summary_cpp
>./outputs/gender_sexual_development_summary_cpp data/gender_sexual_development_panel.csv

go: data
>go run go/gender_sexual_development_summary.go data/gender_sexual_development_panel.csv

rust: data
>rustc rust/validate_gender_sexual_development_panel.rs -o outputs/validate_gender_sexual_development_panel_rust
>./outputs/validate_gender_sexual_development_panel_rust data/gender_sexual_development_panel.csv

julia:
>julia julia/simulate_gender_sexual_development.jl

fortran:
>gfortran fortran/gender_sexual_development_simulation.f90 -o outputs/gender_sexual_development_fortran
>./outputs/gender_sexual_development_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png
>rm -f outputs/gender_sexual_development_summary_c
>rm -f outputs/gender_sexual_development_summary_cpp
>rm -f outputs/validate_gender_sexual_development_panel_rust
>rm -f outputs/gender_sexual_development_fortran
