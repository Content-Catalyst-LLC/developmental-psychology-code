.PHONY: data python r julia go rust c cpp fortran all clean

data:
	python3 python/generate_cultural_development_panel.py

python: data
	python3 python/model_cultural_development.py

r: data
	Rscript r/model_culture_development.R

julia:
	julia julia/simulate_cultural_development.jl

go: data
	go run go/culture_summary.go data/cultural_development_panel.csv

rust: data
	rustc rust/validate_culture_panel.rs -o outputs/validate_culture_panel_rust
	./outputs/validate_culture_panel_rust data/cultural_development_panel.csv

c: data
	gcc c/culture_summary.c -o outputs/culture_summary_c
	./outputs/culture_summary_c data/cultural_development_panel.csv

cpp: data
	g++ -std=c++17 cpp/culture_summary.cpp -o outputs/culture_summary_cpp
	./outputs/culture_summary_cpp data/cultural_development_panel.csv

fortran:
	gfortran fortran/cultural_development_simulation.f90 -o outputs/cultural_development_fortran
	./outputs/cultural_development_fortran

all: python r

clean:
	rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/culture_summary_c outputs/culture_summary_cpp outputs/validate_culture_panel_rust outputs/cultural_development_fortran
