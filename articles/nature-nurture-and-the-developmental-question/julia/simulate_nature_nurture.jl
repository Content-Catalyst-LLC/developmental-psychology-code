using Random
using Statistics

Random.seed!(2026)

n_children = 900
n_periods = 10

development_trajectory = zeros(Float64, n_periods)
protective_trajectory = zeros(Float64, n_periods)
support_trajectory = zeros(Float64, n_periods)
stress_trajectory = zeros(Float64, n_periods)
risk_trajectory = zeros(Float64, n_periods)
sensitivity_trajectory = zeros(Float64, n_periods)

for child in 1:n_children
    biological_sensitivity = randn()
    baseline_functioning = 50 + 7 * randn()
    structural_risk = rand() < 0.35 ? 1.0 : 0.0
    chronic_adversity = rand() < 0.32 ? 1.0 : 0.0
    family_support_context = randn()
    institutional_support = 0.7 * randn()
    disability_support = 0.6 * randn()
    resource_stability = 0.5 * randn()
    previous_score = baseline_functioning

    for t in 1:n_periods
        time = t - 1
        caregiver_support = 0.4 + family_support_context - 0.5 * structural_risk + 0.9 * randn()
        acute_stress = 0.3 * structural_risk + 0.35 * chronic_adversity + 0.8 * randn()
        intervention = (time >= 5 && rand() < 0.28) ? 1.0 : 0.0

        protective_context =
            caregiver_support +
            institutional_support +
            disability_support +
            resource_stability +
            intervention

        development_score =
            0.70 * previous_score +
            0.90 * time +
            1.20 * caregiver_support -
            1.40 * acute_stress -
            2.20 * structural_risk -
            1.80 * chronic_adversity +
            0.95 * institutional_support +
            0.85 * disability_support +
            0.70 * resource_stability +
            1.60 * intervention +
            1.00 * biological_sensitivity * caregiver_support -
            0.90 * biological_sensitivity * acute_stress +
            0.65 * biological_sensitivity * protective_context +
            2.6 * randn()

        development_trajectory[t] += development_score
        protective_trajectory[t] += protective_context
        support_trajectory[t] += caregiver_support
        stress_trajectory[t] += acute_stress
        risk_trajectory[t] += structural_risk
        sensitivity_trajectory[t] += biological_sensitivity
        previous_score = development_score
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_nature_nurture.csv"), "w") do io
    println(io, "time,average_development_score,average_protective_context,average_caregiver_support,average_acute_stress,average_structural_risk,average_biological_sensitivity")
    for t in 1:n_periods
        println(io, "$(t - 1),$(development_trajectory[t] / n_children),$(protective_trajectory[t] / n_children),$(support_trajectory[t] / n_children),$(stress_trajectory[t] / n_children),$(risk_trajectory[t] / n_children),$(sensitivity_trajectory[t] / n_children)")
    end
end

println("Wrote outputs/julia_nature_nurture.csv")
