# Synthetic life-course developmental simulation in Julia.
# Run with: julia julia/simulate_life_course.jl

using Random
using Statistics
using DelimitedFiles

Random.seed!(2026)

n_people = 1000
n_periods = 10

scores = zeros(Float64, n_people, n_periods)

for i in 1:n_people
    support = randn()
    risk = randn()
    policy = randn()
    resilience = 0.7 * randn()
    previous_score = 50 + 3 * randn()

    for t in 1:n_periods
        current_support = support + 0.5 * randn()
        current_risk = risk + 0.6 * randn()
        current_policy = policy + 0.5 * randn()

        scores[i, t] =
            0.68 * previous_score +
            0.22 * (t - 1) +
            1.10 * current_support -
            1.15 * current_risk +
            0.90 * current_policy +
            resilience +
            2.0 * randn()

        previous_score = scores[i, t]
    end
end

trajectory = [mean(scores[:, t]) for t in 1:n_periods]

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_average_trajectory.csv"), "w") do io
    println(io, "time,average_development")
    for t in 1:n_periods
        println(io, "$(t - 1),$(trajectory[t])")
    end
end

println("Wrote outputs/julia_average_trajectory.csv")
