# Synthetic critical-period and sensitive-period simulation in Julia.
# Run with: julia julia/simulate_timing_windows.jl

using Random
using Statistics

Random.seed!(2026)

n_people = 900
n_periods = 14

function gaussian_weight(t, center, sd)
    return exp(-((t - center)^2) / (2 * sd^2))
end

critical_means = zeros(Float64, n_periods)
sensitive_means = zeros(Float64, n_periods)
multi_window_means = zeros(Float64, n_periods)

for i in 1:n_people
    baseline = randn()
    support = randn()
    adversity = randn()

    for t in 1:n_periods
        experience = baseline + 0.7 * randn()
        critical_weight = (t >= 3 && t <= 5) ? 1.0 : 0.0
        early_sensitive = gaussian_weight(t, 4.0, 2.0)
        adolescent_sensitive = gaussian_weight(t, 10.0, 2.2)

        critical_outcome =
            50 + 0.3 * t + 2.2 * experience * critical_weight +
            0.6 * support - 0.7 * adversity + 2.0 * randn()

        sensitive_outcome =
            50 + 0.3 * t + 2.0 * experience * early_sensitive +
            0.6 * support - 0.7 * adversity + 2.0 * randn()

        multi_window_outcome =
            50 + 0.3 * t +
            1.4 * experience * early_sensitive +
            1.2 * experience * adolescent_sensitive +
            0.6 * support - 0.7 * adversity + 2.0 * randn()

        critical_means[t] += critical_outcome
        sensitive_means[t] += sensitive_outcome
        multi_window_means[t] += multi_window_outcome
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_timing_windows.csv"), "w") do io
    println(io, "time,critical_outcome,sensitive_outcome,multi_window_outcome")
    for t in 1:n_periods
        println(io, "$(t),$(critical_means[t] / n_people),$(sensitive_means[t] / n_people),$(multi_window_means[t] / n_people)")
    end
end

println("Wrote outputs/julia_timing_windows.csv")
