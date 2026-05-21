.PHONY: data python r julia go rust c cpp fortran all clean

data:
	python3 python/generate_trauma_life_course.py

python: data
	python3 python/model_trauma_life_course.py

r: data
	Rscript r/model_trauma_life_course.R

julia:
	julia julia/simulate_trauma_life_course.jl

go: data
	go run go/trauma_summary.go data/trauma_life_course_panel.csv

rust: data
	rustc rust/validate_trauma_panel.rs -o outputs/validate_trauma_panel_rust
	./outputs/validate_trauma_panel_rust data/trauma_life_course_panel.csv

c: data
	gcc c/trauma_summary.c -o outputs/trauma_summary_c
	./outputs/trauma_summary_c data/trauma_life_course_panel.csv

cpp: data
	g++ -std=c++17 cpp/trauma_summary.cpp -o outputs/trauma_summary_cpp
	./outputs/trauma_summary_cpp data/trauma_life_course_panel.csv

fortran:
	gfortran fortran/trauma_life_course_simulation.f90 -o outputs/trauma_life_course_fortran
	./outputs/trauma_life_course_fortran

all: python r

clean:
	rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/trauma_summary_c outputs/trauma_summary_cpp outputs/validate_trauma_panel_rust outputs/trauma_life_course_fortran
