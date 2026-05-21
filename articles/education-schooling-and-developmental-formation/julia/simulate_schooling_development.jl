using Random
using Statistics

Random.seed!(2026)

n_students = 850
n_periods = 10

development_trajectory = zeros(Float64, n_periods)
connectedness_trajectory = zeros(Float64, n_periods)

for student in 1:n_students
    teacher = randn()
    peer = randn()
    stress = randn()
    climate = 0.6 * randn()
    curriculum = 0.6 * randn()
    resources = 0.5 * randn()
    intervention = rand() < 0.35 ? 1.0 : 0.0
    previous_development = 50 + 3 * randn()

    for t in 1:n_periods
        current_teacher = teacher + 0.6 * randn()
        current_peer = peer + 0.6 * randn()
        current_stress = stress + 0.7 * randn()

        connectedness =
            45 +
            0.45 * (t - 1) +
            1.20 * current_teacher +
            1.05 * current_peer +
            0.80 * climate -
            1.10 * current_stress +
            2.2 * randn()

        development =
            0.70 * previous_development +
            0.22 * (t - 1) +
            1.10 * current_teacher +
            1.00 * current_peer +
            0.95 * climate +
            0.90 * curriculum +
            0.65 * resources +
            0.85 * intervention +
            0.55 * connectedness / 10 -
            1.05 * current_stress +
            0.50 * current_teacher * current_peer +
            2.3 * randn()

        development_trajectory[t] += development
        connectedness_trajectory[t] += connectedness
        previous_development = development
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_schooling_development.csv"), "w") do io
    println(io, "time,average_development,average_connectedness")
    for t in 1:n_periods
        println(io, "$(t - 1),$(development_trajectory[t] / n_students),$(connectedness_trajectory[t] / n_students)")
    end
end

println("Wrote outputs/julia_schooling_development.csv")
