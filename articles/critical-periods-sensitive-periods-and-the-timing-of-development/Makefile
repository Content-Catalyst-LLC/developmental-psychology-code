.PHONY: data python r julia go rust c cpp fortran all clean

data:
	python3 python/generate_timing_panel.py

python: data
	python3 python/model_timing_windows.py

r: data
	Rscript r/model_critical_sensitive_periods.R

julia:
	julia julia/simulate_timing_windows.jl

go: data
	go run go/timing_summary.go data/developmental_timing_panel.csv

rust: data
	rustc rust/validate_timing_panel.rs -o outputs/validate_timing_panel_rust
	./outputs/validate_timing_panel_rust data/developmental_timing_panel.csv

c: data
	gcc c/timing_summary.c -o outputs/timing_summary_c
	./outputs/timing_summary_c data/developmental_timing_panel.csv

cpp: data
	g++ -std=c++17 cpp/timing_summary.cpp -o outputs/timing_summary_cpp
	./outputs/timing_summary_cpp data/developmental_timing_panel.csv

fortran:
	gfortran fortran/timing_window_simulation.f90 -o outputs/timing_window_simulation_fortran
	./outputs/timing_window_simulation_fortran

all: python r

clean:
	rm -f outputs/*.txt outputs/*.csv outputs/*.png outputs/timing_summary_c outputs/timing_summary_cpp outputs/validate_timing_panel_rust outputs/timing_window_simulation_fortran
