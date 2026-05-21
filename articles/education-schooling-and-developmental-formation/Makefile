.PHONY: data python scenarios r c cpp go rust julia fortran all clean

data:
	python3 python/generate_schooling_development_panel.py

python: data
	python3 python/model_schooling_development.py

scenarios: data
	python3 python/schooling_scenario_analysis.py

r: data
	Rscript r/model_schooling_development.R

c: data
	gcc c/schooling_summary.c -o outputs/schooling_summary_c
	./outputs/schooling_summary_c data/schooling_development_panel.csv

cpp: data
	g++ -std=c++17 cpp/schooling_summary.cpp -o outputs/schooling_summary_cpp
	./outputs/schooling_summary_cpp data/schooling_development_panel.csv

go: data
	go run go/schooling_summary.go data/schooling_development_panel.csv

rust: data
	rustc rust/validate_schooling_panel.rs -o outputs/validate_schooling_panel_rust
	./outputs/validate_schooling_panel_rust data/schooling_development_panel.csv

julia:
	julia julia/simulate_schooling_development.jl

fortran:
	gfortran fortran/schooling_development_simulation.f90 -o outputs/schooling_development_fortran
	./outputs/schooling_development_fortran

all: python scenarios

clean:
	rm -f outputs/*.txt outputs/*.csv outputs/*.png
	rm -f outputs/schooling_summary_c
	rm -f outputs/schooling_summary_cpp
	rm -f outputs/validate_schooling_panel_rust
	rm -f outputs/schooling_development_fortran
