.PHONY: data python r julia go rust c cpp fortran all clean

data:
	python3 python/generate_developmental_panel.py

python: data
	python3 python/model_developmental_trajectories.py

r: data
	Rscript r/model_developmental_conditions.R

julia:
	julia julia/simulate_life_course.jl

go: data
	go run go/development_summary.go data/developmental_panel.csv

rust: data
	rustc rust/validate_developmental_panel.rs -o outputs/validate_developmental_panel_rust
	./outputs/validate_developmental_panel_rust data/developmental_panel.csv

c: data
	gcc c/development_summary.c -o outputs/development_summary_c
	./outputs/development_summary_c data/developmental_panel.csv

cpp: data
	g++ -std=c++17 cpp/development_summary.cpp -o outputs/development_summary_cpp
	./outputs/development_summary_cpp data/developmental_panel.csv

fortran:
	gfortran fortran/life_course_simulation.f90 -o outputs/life_course_simulation_fortran
	./outputs/life_course_simulation_fortran

all: python r

clean:
	rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/development_summary_c outputs/development_summary_cpp outputs/validate_developmental_panel_rust outputs/life_course_simulation_fortran
