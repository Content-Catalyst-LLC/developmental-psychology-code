.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
	python3 python/generate_family_systems_panel.py

python: data
	python3 python/model_family_systems.py

scenarios: data
	python3 python/family_support_scenario_analysis.py

r: data
	Rscript r/model_family_systems.R

c: data
	gcc c/family_systems_summary.c -o outputs/family_systems_summary_c
	./outputs/family_systems_summary_c data/family_systems_panel.csv

cpp: data
	g++ -std=c++17 cpp/family_systems_summary.cpp -o outputs/family_systems_summary_cpp
	./outputs/family_systems_summary_cpp data/family_systems_panel.csv

go: data
	go run go/family_systems_summary.go data/family_systems_panel.csv

rust: data
	rustc rust/validate_family_systems_panel.rs -o outputs/validate_family_systems_panel_rust
	./outputs/validate_family_systems_panel_rust data/family_systems_panel.csv

julia:
	julia julia/simulate_family_systems.jl

fortran:
	gfortran fortran/family_systems_simulation.f90 -o outputs/family_systems_fortran
	./outputs/family_systems_fortran

all: python scenarios

clean:
	rm -f outputs/*.txt outputs/*.csv outputs/*.png
	rm -f outputs/family_systems_summary_c
	rm -f outputs/family_systems_summary_cpp
	rm -f outputs/validate_family_systems_panel_rust
	rm -f outputs/family_systems_fortran
