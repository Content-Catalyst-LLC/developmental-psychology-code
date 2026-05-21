using Random
using Statistics

Random.seed!(2026)

n_children = 850
n_periods = 10

development_trajectory = zeros(Float64, n_periods)
family_support_trajectory = zeros(Float64, n_periods)

for child in 1:n_children
    parenting = randn()
    family = randn()
    stress = randn()
    sibling = 0.8 * randn()
    regulation = 0.8 * randn()
    stability = 0.6 * randn()
    kin = 0.5 * randn()
    security = 0.6 * randn()
    caregiver_support = rand() < 0.35 ? 1.0 : 0.0
    previous_development = 50 + 3 * randn()

    for t in 1:n_periods
        current_parenting = parenting + 0.6 * randn()
        current_family = family + 0.6 * randn()
        current_stress = stress + 0.7 * randn()
        current_sibling = sibling + 0.55 * randn()
        current_regulation = regulation + 0.55 * randn()

        family_support =
            current_parenting +
            current_family +
            stability +
            kin +
            security -
            current_stress

        development =
            0.70 * previous_development +
            0.24 * (t - 1) +
            1.15 * current_parenting +
            1.05 * current_family +
            0.90 * stability +
            0.80 * kin +
            0.75 * security +
            0.70 * current_sibling +
            0.65 * current_regulation +
            0.85 * caregiver_support -
            1.10 * current_stress +
            0.45 * current_parenting * current_family +
            2.3 * randn()

        development_trajectory[t] += development
        family_support_trajectory[t] += family_support
        previous_development = development
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_family_systems.csv"), "w") do io
    println(io, "time,average_development,average_family_support")
    for t in 1:n_periods
        println(io, "$(t - 1),$(development_trajectory[t] / n_children),$(family_support_trajectory[t] / n_children)")
    end
end

println("Wrote outputs/julia_family_systems.csv")
