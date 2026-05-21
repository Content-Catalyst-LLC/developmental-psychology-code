.PHONY: data python r julia go rust c cpp fortran all clean

data:
	python3 python/generate_life_course_inequality.py

python: data
	python3 python/model_life_course_inequality.py

r: data
	Rscript r/model_life_course_inequality.R

julia:
	julia julia/simulate_cumulative_inequality.jl

go: data
	go run go/inequality_summary.go data/life_course_inequality_panel.csv

rust: data
	rustc rust/validate_inequality_panel.rs -o outputs/validate_inequality_panel_rust
	./outputs/validate_inequality_panel_rust data/life_course_inequality_panel.csv

c: data
	gcc c/inequality_summary.c -o outputs/inequality_summary_c
	./outputs/inequality_summary_c data/life_course_inequality_panel.csv

cpp: data
	g++ -std=c++17 cpp/inequality_summary.cpp -o outputs/inequality_summary_cpp
	./outputs/inequality_summary_cpp data/life_course_inequality_panel.csv

fortran:
	gfortran fortran/life_course_inequality_simulation.f90 -o outputs/life_course_inequality_fortran
	./outputs/life_course_inequality_fortran

all: python r

clean:
	rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/inequality_summary_c outputs/inequality_summary_cpp outputs/validate_inequality_panel_rust outputs/life_course_inequality_fortran
