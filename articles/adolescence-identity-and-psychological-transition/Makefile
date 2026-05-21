.RECIPEPREFIX := >
.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
>python3 python/generate_adolescence_identity_panel.py

python: data
>python3 python/model_adolescence_identity.py

scenarios: data
>python3 python/adolescent_transition_scenarios.py

r: data
>Rscript r/model_adolescence_identity.R

c: data
>gcc c/adolescence_identity_summary.c -o outputs/adolescence_identity_summary_c
>./outputs/adolescence_identity_summary_c data/adolescence_identity_panel.csv

cpp: data
>g++ -std=c++17 cpp/adolescence_identity_summary.cpp -o outputs/adolescence_identity_summary_cpp
>./outputs/adolescence_identity_summary_cpp data/adolescence_identity_panel.csv

go: data
>go run go/adolescence_identity_summary.go data/adolescence_identity_panel.csv

rust: data
>rustc rust/validate_adolescence_identity_panel.rs -o outputs/validate_adolescence_identity_panel_rust
>./outputs/validate_adolescence_identity_panel_rust data/adolescence_identity_panel.csv

julia:
>julia julia/simulate_adolescence_identity.jl

fortran:
>gfortran fortran/adolescence_identity_simulation.f90 -o outputs/adolescence_identity_fortran
>./outputs/adolescence_identity_fortran

all: python scenarios

clean:
>rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/*_c outputs/*_cpp outputs/*_rust outputs/*_fortran
