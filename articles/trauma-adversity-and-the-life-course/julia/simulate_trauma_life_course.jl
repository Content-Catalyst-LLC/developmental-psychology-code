# Synthetic trauma/adversity life-course simulation in Julia.
# Run with: julia julia/simulate_trauma_life_course.jl

using Random
using Statistics

Random.seed!(2026)

n_children = 850
n_periods = 10

trajectory = zeros(Float64, n_periods)

profile_scores = Dict(
    "lower_adversity_higher_support" => Float64[],
    "higher_adversity_higher_support" => Float64[],
    "lower_adversity_lower_support" => Float64[],
    "higher_adversity_lower_support" => Float64[]
)

for child in 1:n_children
    adversity = randn()
    support = randn()
    stability = randn()
    previous = 50 + 3 * randn()
    cumulative_adversity = 0.0

    profile =
        adversity < 0 && support >= 0 ? "lower_adversity_higher_support" :
        adversity >= 0 && support >= 0 ? "higher_adversity_higher_support" :
        adversity < 0 && support < 0 ? "lower_adversity_lower_support" :
        "higher_adversity_lower_support"

    final_score = previous

    for t in 1:n_periods
        early_weight = exp(-0.18 * (t - 1))
        transition_weight = exp(-(((t - 1) - 6.0)^2) / (2 * 1.8^2))

        current_adversity = adversity + 0.7 * randn()
        current_support = support + 0.6 * randn()
        current_stability = stability + 0.6 * randn()

        cumulative_adversity += current_adversity * early_weight

        score =
            0.70 * previous +
            0.18 * (t - 1) -
            0.70 * cumulative_adversity -
            1.05 * current_adversity * early_weight +
            1.05 * current_support +
            0.95 * current_stability +
            0.70 * current_support * transition_weight +
            0.75 * current_support * current_stability +
            2.3 * randn()

        trajectory[t] += score
        previous = score
        final_score = score
    end

    push!(profile_scores[profile], final_score)
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_trauma_life_course.csv"), "w") do io
    println(io, "time,average_adaptation")
    for t in 1:n_periods
        println(io, "$(t - 1),$(trajectory[t] / n_children)")
    end
end

open(joinpath(outputs_dir, "julia_adversity_support_profiles.csv"), "w") do io
    println(io, "adversity_support_profile,children,average_final_score")
    for (profile, values) in profile_scores
        println(io, "$profile,$(length(values)),$(mean(values))")
    end
end

println("Wrote outputs/julia_trauma_life_course.csv")
println("Wrote outputs/julia_adversity_support_profiles.csv")
