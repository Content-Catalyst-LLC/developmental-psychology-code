using Random
using Statistics

Random.seed!(2026)

n_children = 900
n_periods = 10

development_trajectory = zeros(Float64, n_periods)
embedded_stress_trajectory = zeros(Float64, n_periods)
embedded_support_trajectory = zeros(Float64, n_periods)

for child in 1:n_children
    bio = randn()
    care_base = randn()
    stress_base = randn()
    nutrition_base = 0.8 * randn()
    school_support = 0.6 * randn()
    safety = 0.6 * randn()
    services = 0.5 * randn()
    early = rand() < 0.40 ? 1.0 : 0.0
    intervention = rand() < 0.35 ? 1.0 : 0.0
    previous_development = 50 + 3 * randn()
    stress_accum = 0.0
    support_accum = 0.0

    for t in 1:n_periods
        timing_weight = exp(-0.30 * (t - 1))
        care = care_base + 0.60 * randn()
        stress = stress_base + 0.65 * randn()
        nutrition = nutrition_base + 0.50 * randn()

        stress_accum += stress * timing_weight
        support_accum += (care + nutrition + school_support) * timing_weight

        embedded_stress = stress_accum / t
        embedded_support = support_accum / t

        development =
            0.70 * previous_development +
            0.22 * (t - 1) +
            0.90 * bio +
            1.10 * care -
            1.05 * stress +
            0.80 * nutrition +
            0.75 * school_support +
            0.65 * safety +
            0.60 * services +
            0.85 * early * timing_weight +
            0.85 * intervention +
            0.95 * bio * care -
            0.90 * bio * stress -
            0.70 * embedded_stress +
            0.60 * embedded_support +
            2.3 * randn()

        development_trajectory[t] += development
        embedded_stress_trajectory[t] += embedded_stress
        embedded_support_trajectory[t] += embedded_support
        previous_development = development
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_genes_environment_plasticity.csv"), "w") do io
    println(io, "time,average_development,average_embedded_stress,average_embedded_support")
    for t in 1:n_periods
        println(io, "$(t - 1),$(development_trajectory[t] / n_children),$(embedded_stress_trajectory[t] / n_children),$(embedded_support_trajectory[t] / n_children)")
    end
end

println("Wrote outputs/julia_genes_environment_plasticity.csv")
