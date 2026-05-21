using Random
using Statistics

Random.seed!(2026)

n_people = 950
n_periods = 12

development_trajectory = zeros(Float64, n_periods)
gains_trajectory = zeros(Float64, n_periods)
losses_trajectory = zeros(Float64, n_periods)
soc_trajectory = zeros(Float64, n_periods)

for person in 1:n_people
    baseline = 50 + 8 * randn()
    plasticity = randn()
    support_base = randn()
    comp_base = randn()
    health = 0.8 * randn()
    historical = 0.6 * randn()
    institutional = 0.6 * randn()
    previous_development = baseline + 2 * randn()

    for t in 1:n_periods
        gains = 0.90 - 0.05 * (t - 1) + 0.50 * randn()
        losses = 0.20 + 0.07 * (t - 1) + 0.50 * randn()
        support = support_base + 0.70 * randn()
        current_comp = comp_base + 0.70 * randn()
        selection = 0.30 + 0.04 * (t - 1) + 0.50 * randn()
        optimization = 0.50 + 0.50 * randn()
        compensation = comp_base + 0.05 * (t - 1) + 0.50 * randn()
        soc = 0.35 * selection + 0.35 * optimization + 0.30 * compensation

        development =
            0.70 * previous_development +
            0.20 * (t - 1) +
            1.05 * gains -
            1.00 * losses +
            0.90 * plasticity +
            0.95 * support +
            0.80 * current_comp +
            0.65 * health +
            0.75 * historical +
            0.70 * institutional +
            0.90 * soc +
            0.35 * plasticity * support -
            0.30 * losses * compensation +
            2.5 * randn()

        development_trajectory[t] += development
        gains_trajectory[t] += gains
        losses_trajectory[t] += losses
        soc_trajectory[t] += soc
        previous_development = development
    end
end

root = joinpath(@__DIR__, "..")
outputs_dir = joinpath(root, "outputs")
mkpath(outputs_dir)

open(joinpath(outputs_dir, "julia_lifespan_baltes.csv"), "w") do io
    println(io, "time,average_development,average_gains,average_losses,average_soc")
    for t in 1:n_periods
        println(io, "$(t - 1),$(development_trajectory[t] / n_people),$(gains_trajectory[t] / n_people),$(losses_trajectory[t] / n_people),$(soc_trajectory[t] / n_people)")
    end
end

println("Wrote outputs/julia_lifespan_baltes.csv")
