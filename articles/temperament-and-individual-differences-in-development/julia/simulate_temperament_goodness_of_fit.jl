using Random
using Statistics

Random.seed!(2026)

n_children = 900
n_periods = 10

adjustment_trajectory = zeros(Float64, n_periods)
fit_trajectory = zeros(Float64, n_periods)
support_trajectory = zeros(Float64, n_periods)
stress_trajectory = zeros(Float64, n_periods)

for child in 1:n_children
    reactivity = randn()
    inhibition = randn()
    activity = randn()
    baseline_adjustment = 50 + 8 * randn()
    family_support = randn()
    school_fit = randn()
    chronic_stress = rand() < 0.30 ? 1.0 : 0.0
    classroom_structure = 0.6 * randn()
    teacher = 0.6 * randn()
    movement = 0.5 * randn()
    previous_adjustment = baseline_adjustment + 2 * randn()

    for t in 1:n_periods
        support = family_support + 0.70 * randn()
        current_school_fit = school_fit + 0.70 * randn()
        stress = 0.3 * chronic_stress + 0.80 * randn()
        accommodation = 0.40 + 0.50 * randn()

        goodness_of_fit =
            current_school_fit +
            teacher +
            movement -
            abs(reactivity - classroom_structure) +
            accommodation

        adjustment =
            0.70 * previous_adjustment +
            0.90 * (t - 1) +
            1.30 * support +
            1.20 * goodness_of_fit +
            0.50 * teacher -
            1.50 * stress -
            1.10 * chronic_stress -
            0.25 * inhibition -
            0.20 * activity +
            0.95 * reactivity * support +
            0.85 * reactivity * goodness_of_fit -
            0.90 * reactivity * stress +
            2.5 * randn()

        adjustment_trajectory[t] += adjustment
        fit_trajectory[t] += goodness_of_fit
        support_trajectory[t] += support
        stress_trajectory[t] += stress
        previous_adjustment = adjustment
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_temperament_goodness_of_fit.csv"), "w") do io
    println(io, "time,average_adjustment,average_goodness_of_fit,average_support,average_stress")
    for t in 1:n_periods
        println(io, "$(t - 1),$(adjustment_trajectory[t] / n_children),$(fit_trajectory[t] / n_children),$(support_trajectory[t] / n_children),$(stress_trajectory[t] / n_children)")
    end
end

println("Wrote outputs/julia_temperament_goodness_of_fit.csv")
