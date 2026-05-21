using Random
using Statistics

Random.seed!(2026)

n_adolescents = 900
n_periods = 10

adjustment_trajectory = zeros(Float64, n_periods)
protective_trajectory = zeros(Float64, n_periods)
stigma_trajectory = zeros(Float64, n_periods)
family_trajectory = zeros(Float64, n_periods)
consent_trajectory = zeros(Float64, n_periods)

for adolescent in 1:n_adolescents
    baseline_adjustment = 50 + 8 * randn()
    family_support = randn()
    social_recognition = randn()
    consent_knowledge = randn()
    school_connectedness = randn()
    chronic_stigma = rand() < 0.24 ? 1.0 : 0.0
    school_climate = 0.6 * randn()
    health_education_quality = 0.6 * randn()
    anti_harassment_support = 0.5 * randn()
    previous_adjustment = baseline_adjustment + 2 * randn()

    for t in 1:n_periods
        pubertal_progress = (t - 1) + 0.40 * randn()
        current_family = family_support + 0.70 * randn()
        current_recognition = social_recognition + 0.70 * randn()
        current_consent = consent_knowledge + 0.70 * randn()
        current_connectedness = school_connectedness + 0.70 * randn()
        current_stigma = 0.40 * chronic_stigma + 0.70 * randn()

        protective_context =
            current_family +
            current_recognition +
            current_consent +
            current_connectedness +
            school_climate +
            health_education_quality +
            anti_harassment_support

        adjustment =
            0.70 * previous_adjustment +
            0.75 * pubertal_progress +
            1.15 * current_family +
            1.05 * current_recognition +
            1.00 * current_consent +
            0.95 * current_connectedness +
            0.70 * school_climate +
            0.70 * health_education_quality +
            0.65 * anti_harassment_support -
            1.40 * current_stigma -
            0.90 * chronic_stigma -
            0.35 * current_stigma * protective_context +
            2.5 * randn()

        adjustment_trajectory[t] += adjustment
        protective_trajectory[t] += protective_context
        stigma_trajectory[t] += current_stigma
        family_trajectory[t] += current_family
        consent_trajectory[t] += current_consent
        previous_adjustment = adjustment
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_gender_sexual_development.csv"), "w") do io
    println(io, "time,average_adjustment,average_protective_context,average_stigma,average_family_support,average_consent_knowledge")
    for t in 1:n_periods
        println(io, "$(t - 1),$(adjustment_trajectory[t] / n_adolescents),$(protective_trajectory[t] / n_adolescents),$(stigma_trajectory[t] / n_adolescents),$(family_trajectory[t] / n_adolescents),$(consent_trajectory[t] / n_adolescents)")
    end
end

println("Wrote outputs/julia_gender_sexual_development.csv")
