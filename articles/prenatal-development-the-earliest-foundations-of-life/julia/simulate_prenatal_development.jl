using Random
using Statistics

Random.seed!(2026)

n_cases = 1500

outcome_sum = 0.0
care_sum = 0.0
risk_sum = 0.0
gestation_sum = 0.0
maternal_health_sum = 0.0

for case_id in 1:n_cases
    gestational_weeks = 39 + 1.8 * randn()
    maternal_health = randn()
    prenatal_care = randn()
    chronic_stress = randn()
    toxic_exposure = randn()
    nutrition_support = randn()
    social_support = randn()
    healthcare_access = 0.6 * randn()
    environmental_burden = 0.6 * randn()
    economic_security = 0.5 * randn()

    effective_care = prenatal_care + healthcare_access + 0.30 * social_support
    developmental_risk = chronic_stress + toxic_exposure + environmental_burden - 0.40 * economic_security

    early_outcome =
        10 +
        0.85 * gestational_weeks +
        1.60 * maternal_health +
        1.35 * effective_care +
        1.10 * nutrition_support +
        0.85 * social_support -
        1.55 * chronic_stress -
        1.45 * toxic_exposure -
        1.10 * environmental_burden +
        0.70 * maternal_health * effective_care -
        0.60 * maternal_health * chronic_stress -
        0.55 * developmental_risk * effective_care +
        2.6 * randn()

    outcome_sum += early_outcome
    care_sum += effective_care
    risk_sum += developmental_risk
    gestation_sum += gestational_weeks
    maternal_health_sum += maternal_health
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_prenatal_development.csv"), "w") do io
    println(io, "measure,value")
    println(io, "average_early_outcome,$(outcome_sum / n_cases)")
    println(io, "average_effective_care,$(care_sum / n_cases)")
    println(io, "average_developmental_risk,$(risk_sum / n_cases)")
    println(io, "average_gestational_weeks,$(gestation_sum / n_cases)")
    println(io, "average_maternal_health,$(maternal_health_sum / n_cases)")
end

println("Wrote outputs/julia_prenatal_development.csv")
