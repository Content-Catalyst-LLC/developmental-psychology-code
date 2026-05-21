using Random
using Statistics

Random.seed!(2026)

n_people = 900
n_periods = 10
trajectory = zeros(Float64, n_periods)

for i in 1:n_people
    resources = randn()
    burden = randn()
    support = randn()
    previous = 50 + 3 * randn()

    for t in 1:n_periods
        early_weight = exp(-0.16 * (t - 1))
        transition_weight = exp(-(((t - 1) - 6.0)^2) / (2 * 1.8^2))
        score = 0.68 * previous + 0.20 * (t - 1) +
                1.00 * resources * early_weight -
                1.15 * burden * early_weight +
                0.95 * support +
                0.85 * support * transition_weight +
                2.2 * randn()
        trajectory[t] += score
        previous = score
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_cumulative_inequality.csv"), "w") do io
    println(io, "time,average_development")
    for t in 1:n_periods
        println(io, "$(t - 1),$(trajectory[t] / n_people)")
    end
end

println("Wrote outputs/julia_cumulative_inequality.csv")
