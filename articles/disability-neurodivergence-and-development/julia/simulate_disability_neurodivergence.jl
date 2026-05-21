using Random
using Statistics

Random.seed!(2026)

n_children = 820
n_periods = 10

development_trajectory = zeros(Float64, n_periods)
participation_trajectory = zeros(Float64, n_periods)

for child in 1:n_children
    neuro_profile = randn()
    support = randn()
    access = randn()
    barrier = randn()
    communication = 0.8 * randn()
    previous_development = 50 + 3 * randn()

    for t in 1:n_periods
        current_support = support + 0.6 * randn()
        current_access = access + 0.6 * randn()
        current_barrier = barrier + 0.7 * randn()
        current_communication = communication + 0.55 * randn()

        participation =
            45 +
            0.50 * (t - 1) +
            1.15 * current_support +
            1.10 * current_access +
            0.95 * current_communication -
            1.25 * current_barrier +
            2.2 * randn()

        development =
            0.70 * previous_development +
            0.20 * (t - 1) +
            0.45 * neuro_profile +
            1.10 * current_support +
            1.05 * current_access +
            0.90 * current_communication +
            0.80 * participation / 10 -
            1.15 * current_barrier +
            0.50 * current_support * current_access -
            0.40 * current_barrier * abs(neuro_profile) +
            2.3 * randn()

        development_trajectory[t] += development
        participation_trajectory[t] += participation
        previous_development = development
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_disability_neurodivergence.csv"), "w") do io
    println(io, "time,average_development,average_participation")
    for t in 1:n_periods
        println(io, "$(t - 1),$(development_trajectory[t] / n_children),$(participation_trajectory[t] / n_children)")
    end
end

println("Wrote outputs/julia_disability_neurodivergence.csv")
