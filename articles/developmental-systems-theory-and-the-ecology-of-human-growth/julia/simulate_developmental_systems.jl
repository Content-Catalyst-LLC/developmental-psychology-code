using Random
using Statistics

Random.seed!(2026)

n_children = 850
n_periods = 10

development_trajectory = zeros(Float64, n_periods)
support_trajectory = zeros(Float64, n_periods)
stress_trajectory = zeros(Float64, n_periods)

for child in 1:n_children
    bio = randn()
    family_base = randn()
    peer_base = 0.8 * randn()
    school_climate = 0.6 * randn()
    curriculum = 0.5 * randn()
    neighborhood_safety = 0.6 * randn()
    service_access = 0.5 * randn()
    material_security = 0.5 * randn()
    intervention = rand() < 0.35 ? 1.0 : 0.0
    previous_development = 50 + 3 * randn()

    for t in 1:n_periods
        current_family = family_base + 0.60 * randn()
        current_peer = peer_base + 0.60 * randn()

        ecological_support =
            current_family +
            current_peer +
            school_climate +
            curriculum +
            neighborhood_safety +
            service_access +
            material_security

        ecological_stress =
            -0.25 * current_family -
            0.20 * school_climate -
            0.20 * neighborhood_safety -
            0.15 * material_security +
            0.70 * randn()

        development =
            0.70 * previous_development +
            0.24 * (t - 1) +
            0.85 * bio +
            1.15 * current_family +
            0.95 * current_peer +
            0.95 * school_climate +
            0.80 * curriculum +
            0.85 * neighborhood_safety +
            0.70 * service_access +
            0.65 * material_security +
            0.90 * intervention -
            1.10 * ecological_stress +
            0.45 * bio * current_family -
            0.35 * bio * ecological_stress +
            2.3 * randn()

        development_trajectory[t] += development
        support_trajectory[t] += ecological_support
        stress_trajectory[t] += ecological_stress
        previous_development = development
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_developmental_systems.csv"), "w") do io
    println(io, "time,average_development,average_ecological_support,average_ecological_stress")
    for t in 1:n_periods
        println(io, "$(t - 1),$(development_trajectory[t] / n_children),$(support_trajectory[t] / n_children),$(stress_trajectory[t] / n_children)")
    end
end

println("Wrote outputs/julia_developmental_systems.csv")
