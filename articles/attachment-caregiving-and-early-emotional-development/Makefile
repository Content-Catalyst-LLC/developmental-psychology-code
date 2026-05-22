.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_attachment_development_panel.py

python: data
>python3 python/model_attachment_development.py

scenarios: data
>python3 python/attachment_support_scenarios.py

r: data
>Rscript r/model_attachment_development.R

c: data
>gcc c/attachment_development_summary.c -o outputs/attachment_development_summary_c
>./outputs/attachment_development_summary_c data/attachment_development_panel.csv

cpp: data
>g++ -std=c++17 cpp/attachment_development_summary.cpp -o outputs/attachment_development_summary_cpp
>./outputs/attachment_development_summary_cpp data/attachment_development_panel.csv

go: data
>go run go/attachment_development_summary.go data/attachment_development_panel.csv

rust: data
>rustc rust/validate_attachment_development_panel.rs -o outputs/validate_attachment_development_panel_rust
>./outputs/validate_attachment_development_panel_rust data/attachment_development_panel.csv

julia:
>julia julia/simulate_attachment_development.jl

fortran:
>gfortran fortran/attachment_development_simulation.f90 -o outputs/attachment_development_fortran
>./outputs/attachment_development_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/*_c outputs/*_cpp outputs/*_rust outputs/*_fortran
