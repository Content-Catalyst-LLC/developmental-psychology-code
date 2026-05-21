.PHONY: data python r julia go rust c cpp fortran all clean

data:
	python3 python/generate_developmental_designs.py

python: data
	python3 python/analyze_developmental_designs.py

r: data
	Rscript r/analyze_research_designs.R

julia:
	julia julia/simulate_cohort_sequential_design.jl

go: data
	go run go/design_summary.go data/developmental_design_panel.csv

rust: data
	rustc rust/validate_design_panel.rs -o outputs/validate_design_panel_rust
	./outputs/validate_design_panel_rust data/developmental_design_panel.csv

c: data
	gcc c/design_summary.c -o outputs/design_summary_c
	./outputs/design_summary_c data/developmental_design_panel.csv

cpp: data
	g++ -std=c++17 cpp/design_summary.cpp -o outputs/design_summary_cpp
	./outputs/design_summary_cpp data/developmental_design_panel.csv

fortran:
	gfortran fortran/growth_curve_simulation.f90 -o outputs/growth_curve_simulation_fortran
	./outputs/growth_curve_simulation_fortran

all: python r

clean:
	rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/design_summary_c outputs/design_summary_cpp outputs/validate_design_panel_rust outputs/growth_curve_simulation_fortran
