.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_social_development_panel.py

python: data
>python3 python/model_social_development.py

scenarios: data
>python3 python/social_development_scenarios.py

r: data
>Rscript r/model_social_development.R

c: data
>gcc c/social_development_summary.c -o outputs/social_development_summary_c
>./outputs/social_development_summary_c data/social_development_panel.csv

cpp: data
>g++ -std=c++17 cpp/social_development_summary.cpp -o outputs/social_development_summary_cpp
>./outputs/social_development_summary_cpp data/social_development_panel.csv

go: data
>go run go/social_development_summary.go data/social_development_panel.csv

rust: data
>rustc rust/validate_social_development_panel.rs -o outputs/validate_social_development_panel_rust
>./outputs/validate_social_development_panel_rust data/social_development_panel.csv

julia:
>julia julia/simulate_social_development.jl

fortran:
>gfortran fortran/social_development_simulation.f90 -o outputs/social_development_fortran
>./outputs/social_development_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/*_c outputs/*_cpp outputs/*_rust outputs/*_fortran
