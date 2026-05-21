# Synthetic cultural-development simulation in Julia.
# Run with: julia julia/simulate_cultural_development.jl

using Random
using Statistics

Random.seed!(2026)

n_children = 850
n_periods = 10

trajectory = zeros(Float64, n_periods)

condition_scores = Dict(
    "lower_mismatch_higher_support" => Float64[],
    "higher_mismatch_higher_support" => Float64[],
    "lower_mismatch_lower_support" => Float64[],
    "higher_mismatch_lower_support" => Float64[]
)

for child in 1:n_children
    family = randn()
    fit = randn()
    mismatch = randn()
    support = randn()
    flexibility = 0.7 * randn()
    previous = 50 + 3 * randn()

    condition =
        mismatch < 0 && support >= 0 ? "lower_mismatch_higher_support" :
        mismatch >= 0 && support >= 0 ? "higher_mismatch_higher_support" :
        mismatch < 0 && support < 0 ? "lower_mismatch_lower_support" :
        "higher_mismatch_lower_support"

    final_score = previous

    for t in 1:n_periods
        current_family = family + 0.6 * randn()
        current_fit = fit + 0.6 * randn()
        current_mismatch = mismatch + 0.7 * randn()
        current_support = support + 0.6 * randn()
        current_flexibility = flexibility + 0.5 * randn()

        score =
            0.70 * previous +
            0.18 * (t - 1) +
            1.00 * current_family +
            0.95 * current_fit +
            0.90 * current_support +
            0.80 * current_flexibility -
            1.00 * current_mismatch +
            2.3 * randn()

        trajectory[t] += score
        previous = score
        final_score = score
    end

    push!(condition_scores[condition], final_score)
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_cultural_development.csv"), "w") do io
    println(io, "time,average_development")
    for t in 1:n_periods
        println(io, "$(t - 1),$(trajectory[t] / n_children)")
    end
end

open(joinpath(outputs_dir, "julia_cultural_conditions.csv"), "w") do io
    println(io, "cultural_condition,children,average_final_score")
    for (condition, values) in condition_scores
        println(io, "$condition,$(length(values)),$(mean(values))")
    end
end

println("Wrote outputs/julia_cultural_development.csv")
println("Wrote outputs/julia_cultural_conditions.csv")
