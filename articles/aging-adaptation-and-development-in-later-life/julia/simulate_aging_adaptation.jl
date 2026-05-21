using Random
using Statistics

Random.seed!(2026)

n_older_adults = 900
n_periods = 10

adjustment_trajectory = zeros(Float64, n_periods)
fit_trajectory = zeros(Float64, n_periods)
support_trajectory = zeros(Float64, n_periods)
health_trajectory = zeros(Float64, n_periods)

for person in 1:n_older_adults
    baseline_adjustment = 50 + 8 * randn()
    function_base = randn()
    support_base = randn()
    health_base = randn()
    adaptation_base = randn()
    meaning_base = 0.8 * randn()
    accessibility = 0.6 * randn()
    dignity = 0.6 * randn()
    services = 0.5 * randn()
    previous_adjustment = baseline_adjustment + 2 * randn()

    for t in 1:n_periods
        current_function = function_base - 0.04 * (t - 1) + 0.70 * randn()
        current_support = support_base + 0.70 * randn()
        current_health = health_base + 0.05 * (t - 1) + 0.70 * randn()
        current_adaptation = adaptation_base + 0.03 * (t - 1) + 0.70 * randn()
        current_meaning = meaning_base + 0.55 * randn()

        functional_fit =
            current_function +
            accessibility +
            0.35 * current_function * accessibility

        adjustment =
            0.70 * previous_adjustment +
            0.35 * (t - 1) +
            1.15 * functional_fit +
            1.05 * current_support +
            0.95 * current_adaptation +
            0.80 * current_meaning +
            0.75 * dignity +
            0.60 * services -
            1.30 * current_health +
            2.5 * randn()

        adjustment_trajectory[t] += adjustment
        fit_trajectory[t] += functional_fit
        support_trajectory[t] += current_support
        health_trajectory[t] += current_health
        previous_adjustment = adjustment
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_aging_adaptation.csv"), "w") do io
    println(io, "time,average_adjustment,average_functional_fit,average_support,average_health")
    for t in 1:n_periods
        println(io, "$(t - 1),$(adjustment_trajectory[t] / n_older_adults),$(fit_trajectory[t] / n_older_adults),$(support_trajectory[t] / n_older_adults),$(health_trajectory[t] / n_older_adults)")
    end
end

println("Wrote outputs/julia_aging_adaptation.csv")
