using Random
using Statistics

Random.seed!(2026)

n_children = 850
n_periods = 10

adaptation_trajectory = zeros(Float64, n_periods)
internalizing_trajectory = zeros(Float64, n_periods)
externalizing_trajectory = zeros(Float64, n_periods)

for child in 1:n_children
    risk = randn()
    support = randn()
    stability = randn()
    regulation = randn()
    sensitivity = 0.7 * randn()

    previous_adaptation = 50 + 3 * randn()
    previous_internalizing = 45 + 3 * randn()
    previous_externalizing = 45 + 3 * randn()
    cumulative_risk = 0.0

    for t in 1:n_periods
        timing_weight = exp(-0.16 * (t - 1))
        transition_weight = exp(-(((t - 1) - 6.0)^2) / (2 * 1.8^2))

        current_risk = risk + 0.7 * randn()
        current_support = support + 0.6 * randn()
        current_stability = stability + 0.6 * randn()
        current_regulation = regulation + 0.55 * randn()

        cumulative_risk += current_risk * timing_weight

        adaptation =
            0.70 * previous_adaptation +
            0.20 * (t - 1) +
            0.75 * current_regulation +
            1.10 * current_support +
            1.00 * current_stability +
            0.70 * current_support * transition_weight -
            0.85 * cumulative_risk -
            1.10 * current_risk * timing_weight +
            0.60 * sensitivity * current_support +
            0.75 * current_support * current_stability +
            2.3 * randn()

        internalizing =
            0.64 * previous_internalizing +
            0.95 * current_risk * timing_weight +
            0.55 * cumulative_risk -
            0.70 * current_support -
            0.55 * current_stability -
            0.45 * current_regulation +
            0.40 * sensitivity +
            2.1 * randn() + 30

        externalizing =
            0.62 * previous_externalizing +
            0.85 * current_risk * timing_weight +
            0.45 * cumulative_risk -
            0.65 * current_support -
            0.70 * current_stability -
            0.60 * current_regulation +
            0.35 * sensitivity +
            2.2 * randn() + 30

        adaptation_trajectory[t] += adaptation
        internalizing_trajectory[t] += internalizing
        externalizing_trajectory[t] += externalizing

        previous_adaptation = adaptation
        previous_internalizing = internalizing
        previous_externalizing = externalizing
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_developmental_psychopathology.csv"), "w") do io
    println(io, "time,average_adaptation,average_internalizing,average_externalizing")
    for t in 1:n_periods
        println(io, "$(t - 1),$(adaptation_trajectory[t] / n_children),$(internalizing_trajectory[t] / n_children),$(externalizing_trajectory[t] / n_children)")
    end
end

println("Wrote outputs/julia_developmental_psychopathology.csv")
