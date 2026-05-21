.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
	python3 python/generate_developmental_psychopathology.py

python: data
	python3 python/model_developmental_psychopathology.py

scenarios: data
	python3 python/scenario_analysis.py

r: data
	Rscript r/model_developmental_psychopathology.R

c: data
	gcc c/psychopathology_summary.c -o outputs/psychopathology_summary_c
	./outputs/psychopathology_summary_c data/developmental_psychopathology_panel.csv

cpp: data
	g++ -std=c++17 cpp/psychopathology_summary.cpp -o outputs/psychopathology_summary_cpp
	./outputs/psychopathology_summary_cpp data/developmental_psychopathology_panel.csv

go: data
	go run go/psychopathology_summary.go data/developmental_psychopathology_panel.csv

rust: data
	rustc rust/validate_psychopathology_panel.rs -o outputs/validate_psychopathology_panel_rust
	./outputs/validate_psychopathology_panel_rust data/developmental_psychopathology_panel.csv

julia:
	julia julia/simulate_developmental_psychopathology.jl

fortran:
	gfortran fortran/developmental_psychopathology_simulation.f90 -o outputs/developmental_psychopathology_fortran
	./outputs/developmental_psychopathology_fortran

all: python scenarios

clean:
	rm -f outputs/*.txt outputs/*.csv outputs/*.png
	rm -f outputs/psychopathology_summary_c
	rm -f outputs/psychopathology_summary_cpp
	rm -f outputs/validate_psychopathology_panel_rust
	rm -f outputs/developmental_psychopathology_fortran
