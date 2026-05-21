# Synthetic cohort-sequential design simulation in Julia.
# Run with: julia julia/simulate_cohort_sequential_design.jl

using Random
using Statistics

Random.seed!(2026)

n_people = 1200
n_waves = 6
cohorts = [2006, 2009, 2012, 2015]
start_age = Dict(2006 => 14, 2009 => 11, 2012 => 8, 2015 => 5)

scores_by_cohort_age = Dict{Tuple{Int64, Int64}, Vector{Float64}}()

for i in 1:n_people
    cohort = cohorts[rand(1:length(cohorts))]
    baseline = randn()
    support = randn()
    risk = randn()

    for wave in 0:(n_waves - 1)
        age = start_age[cohort] + wave
        centered_age = age - 11.5
        curve = 0.95 * centered_age - 0.035 * centered_age^2
        score = 50 + curve + 1.0 * baseline + 1.1 * support - 1.2 * risk + 2.0 * randn()

        key = (cohort, age)
        if !haskey(scores_by_cohort_age, key)
            scores_by_cohort_age[key] = Float64[]
        end
        push!(scores_by_cohort_age[key], score)
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_cohort_sequential_summary.csv"), "w") do io
    println(io, "birth_cohort,age,average_development_score,observations")
    for key in sort(collect(keys(scores_by_cohort_age)))
        values = scores_by_cohort_age[key]
        println(io, "$(key[1]),$(key[2]),$(mean(values)),$(length(values))")
    end
end

println("Wrote outputs/julia_cohort_sequential_summary.csv")
