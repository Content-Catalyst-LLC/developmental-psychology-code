.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
	python3 python/generate_disability_neurodivergence_panel.py

python: data
	python3 python/model_disability_neurodivergence.py

scenarios: data
	python3 python/access_scenario_analysis.py

r: data
	Rscript r/model_disability_neurodivergence.R

c: data
	gcc c/accessibility_summary.c -o outputs/accessibility_summary_c
	./outputs/accessibility_summary_c data/disability_neurodivergence_panel.csv

cpp: data
	g++ -std=c++17 cpp/accessibility_summary.cpp -o outputs/accessibility_summary_cpp
	./outputs/accessibility_summary_cpp data/disability_neurodivergence_panel.csv

go: data
	go run go/accessibility_summary.go data/disability_neurodivergence_panel.csv

rust: data
	rustc rust/validate_accessibility_panel.rs -o outputs/validate_accessibility_panel_rust
	./outputs/validate_accessibility_panel_rust data/disability_neurodivergence_panel.csv

julia:
	julia julia/simulate_disability_neurodivergence.jl

fortran:
	gfortran fortran/disability_neurodivergence_simulation.f90 -o outputs/disability_neurodivergence_fortran
	./outputs/disability_neurodivergence_fortran

all: python scenarios

clean:
	rm -f outputs/*.txt outputs/*.csv outputs/*.png
	rm -f outputs/accessibility_summary_c
	rm -f outputs/accessibility_summary_cpp
	rm -f outputs/validate_accessibility_panel_rust
	rm -f outputs/disability_neurodivergence_fortran
