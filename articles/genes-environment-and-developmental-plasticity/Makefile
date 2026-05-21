.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
	python3 python/generate_genes_environment_panel.py

python: data
	python3 python/model_genes_environment_plasticity.py

scenarios: data
	python3 python/plasticity_scenario_analysis.py

r: data
	Rscript r/model_genes_environment_plasticity.R

c: data
	gcc c/plasticity_summary.c -o outputs/plasticity_summary_c
	./outputs/plasticity_summary_c data/genes_environment_plasticity_panel.csv

cpp: data
	g++ -std=c++17 cpp/plasticity_summary.cpp -o outputs/plasticity_summary_cpp
	./outputs/plasticity_summary_cpp data/genes_environment_plasticity_panel.csv

go: data
	go run go/plasticity_summary.go data/genes_environment_plasticity_panel.csv

rust: data
	rustc rust/validate_plasticity_panel.rs -o outputs/validate_plasticity_panel_rust
	./outputs/validate_plasticity_panel_rust data/genes_environment_plasticity_panel.csv

julia:
	julia julia/simulate_genes_environment_plasticity.jl

fortran:
	gfortran fortran/genes_environment_plasticity_simulation.f90 -o outputs/genes_environment_plasticity_fortran
	./outputs/genes_environment_plasticity_fortran

all: python scenarios

clean:
	rm -f outputs/*.txt outputs/*.csv outputs/*.png
	rm -f outputs/plasticity_summary_c
	rm -f outputs/plasticity_summary_cpp
	rm -f outputs/validate_plasticity_panel_rust
	rm -f outputs/genes_environment_plasticity_fortran
