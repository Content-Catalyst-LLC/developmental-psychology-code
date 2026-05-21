using Random
using Statistics

Random.seed!(2026)

n_adults = 950
n_periods = 10

adjustment_trajectory = zeros(Float64, n_periods)
support_trajectory = zeros(Float64, n_periods)
work_trajectory = zeros(Float64, n_periods)
health_trajectory = zeros(Float64, n_periods)
burden_trajectory = zeros(Float64, n_periods)

for person in 1:n_adults
    baseline_adjustment = 50 + 8 * randn()
    support_base = randn()
    work_base = randn()
    health_base = randn()
    resources_base = randn()
    burden_base = randn()
    institutional = 0.6 * randn()
    community = 0.5 * randn()
    previous_adjustment = baseline_adjustment + 2 * randn()

    for t in 1:n_periods
        support = support_base + 0.70 * randn()
        work = work_base + 0.70 * randn()
        health = health_base + 0.03 * (t - 1) + 0.70 * randn()
        resources = resources_base + 0.70 * randn()
        burden = burden_base + 0.70 * randn()

        adjustment =
            0.70 * previous_adjustment +
            0.55 * (t - 1) +
            1.15 * support +
            1.05 * work +
            0.95 * resources +
            0.70 * institutional +
            0.55 * community -
            1.20 * health -
            0.80 * burden +
            0.25 * support * resources +
            2.5 * randn()

        adjustment_trajectory[t] += adjustment
        support_trajectory[t] += support
        work_trajectory[t] += work
        health_trajectory[t] += health
        burden_trajectory[t] += burden
        previous_adjustment = adjustment
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_adult_development.csv"), "w") do io
    println(io, "time,average_adjustment,average_support,average_work,average_health,average_role_burden")
    for t in 1:n_periods
        println(io, "$(t - 1),$(adjustment_trajectory[t] / n_adults),$(support_trajectory[t] / n_adults),$(work_trajectory[t] / n_adults),$(health_trajectory[t] / n_adults),$(burden_trajectory[t] / n_adults)")
    end
end

println("Wrote outputs/julia_adult_development.csv")
