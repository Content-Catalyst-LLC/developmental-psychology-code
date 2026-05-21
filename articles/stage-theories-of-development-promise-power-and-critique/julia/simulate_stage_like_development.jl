using Random
using Statistics

Random.seed!(2026)

logistic(x, k=1.35) = 1.0 / (1.0 + exp(-k * x))

n_children = 950
n_periods = 10

score_trajectory = zeros(Float64, n_periods)
readiness_trajectory = zeros(Float64, n_periods)
support_trajectory = zeros(Float64, n_periods)
stress_trajectory = zeros(Float64, n_periods)
logistic_trajectory = zeros(Float64, n_periods)

for child in 1:n_children
    baseline = 46 + 7 * randn()
    growth_rate = 1.70 + 0.50 * randn()
    support_context = randn()
    chronic_stress = rand() < 0.32 ? 1.0 : 0.0
    threshold_time = rand(4:7)
    stage_pattern = rand() < 0.50 ? 1.0 : 0.0
    school_support = 0.6 * randn()
    resource_stability = 0.5 * randn()
    previous_score = baseline

    for t in 1:n_periods
        time = t - 1
        current_support = support_context + 0.70 * randn()
        threshold_on = time >= threshold_time ? 1.0 : 0.0
        smooth_transition = logistic(time - threshold_time)
        readiness = current_support + school_support + resource_stability - 0.75 * chronic_stress

        score =
            0.58 * previous_score +
            0.42 * (baseline + growth_rate * time) +
            1.15 * current_support +
            0.90 * school_support +
            0.70 * resource_stability -
            2.00 * chronic_stress +
            3.00 * threshold_on * stage_pattern +
            2.20 * smooth_transition * stage_pattern +
            0.75 * threshold_on * stage_pattern * readiness +
            2.5 * randn()

        score_trajectory[t] += score
        readiness_trajectory[t] += readiness
        support_trajectory[t] += current_support
        stress_trajectory[t] += chronic_stress
        logistic_trajectory[t] += smooth_transition
        previous_score = score
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_stage_like_development.csv"), "w") do io
    println(io, "time,average_development_score,average_transition_readiness,average_support,average_stress,average_logistic_transition")
    for t in 1:n_periods
        println(io, "$(t - 1),$(score_trajectory[t] / n_children),$(readiness_trajectory[t] / n_children),$(support_trajectory[t] / n_children),$(stress_trajectory[t] / n_children),$(logistic_trajectory[t] / n_children)")
    end
end

println("Wrote outputs/julia_stage_like_development.csv")
