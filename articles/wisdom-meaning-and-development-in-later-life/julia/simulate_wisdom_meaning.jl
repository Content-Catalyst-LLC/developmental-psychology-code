using Random
using Statistics

Random.seed!(2026)

n_older_adults = 900
n_periods = 10

meaning_trajectory = zeros(Float64, n_periods)
wisdom_trajectory = zeros(Float64, n_periods)
connection_trajectory = zeros(Float64, n_periods)
health_trajectory = zeros(Float64, n_periods)

for person in 1:n_older_adults
    baseline_meaning = 50 + 8 * randn()
    social_connection = randn()
    reflective_integration = randn()
    health_burden = randn()
    adaptive_support = randn()
    legacy_orientation = 0.8 * randn()
    dignity_support = 0.6 * randn()
    service_access = 0.5 * randn()
    community_participation = 0.5 * randn()
    previous_meaning = baseline_meaning + 2 * randn()

    for t in 1:n_periods
        connection = social_connection + 0.70 * randn()
        reflection = reflective_integration + 0.70 * randn()
        health = health_burden + 0.70 * randn()
        support = adaptive_support + 0.70 * randn()
        legacy = legacy_orientation + 0.55 * randn()

        wisdom =
            0.35 * reflection +
            0.25 * connection +
            0.20 * legacy +
            0.20 * dignity_support -
            0.20 * health

        meaning =
            0.70 * previous_meaning +
            0.35 * (t - 1) +
            1.10 * connection +
            1.05 * reflection +
            0.90 * support +
            0.75 * legacy +
            0.75 * dignity_support +
            0.60 * service_access +
            0.55 * community_participation -
            1.15 * health +
            0.85 * wisdom +
            2.5 * randn()

        meaning_trajectory[t] += meaning
        wisdom_trajectory[t] += wisdom
        connection_trajectory[t] += connection
        health_trajectory[t] += health
        previous_meaning = meaning
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_wisdom_meaning.csv"), "w") do io
    println(io, "time,average_meaning,average_wisdom,average_connection,average_health")
    for t in 1:n_periods
        println(io, "$(t - 1),$(meaning_trajectory[t] / n_older_adults),$(wisdom_trajectory[t] / n_older_adults),$(connection_trajectory[t] / n_older_adults),$(health_trajectory[t] / n_older_adults)")
    end
end

println("Wrote outputs/julia_wisdom_meaning.csv")
