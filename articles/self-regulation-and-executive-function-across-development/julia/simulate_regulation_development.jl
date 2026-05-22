using Random
Random.seed!(2026)

n = 920
waves = 10
regulation = zeros(waves)
context = zeros(waves)
stress = zeros(waves)
sleep = zeros(waves)

for i in 1:n
    baseline = 50 + 8 * randn()
    support_base, structure_base, sleep_base, temperament = randn(4)
    chronic = rand() < 0.30 ? 1.0 : 0.0
    support_need = rand() < 0.18 ? 1.0 : 0.0
    school, scaffolding, accommodation, transition = 0.6*randn(), 0.6*randn(), 0.6*randn(), 0.5*randn()
    prev = baseline

    for t in 1:waves
        time = t - 1
        support = support_base + 0.7 * randn()
        structure = structure_base + 0.7 * randn()
        slp = sleep_base + 0.5 * randn()
        acute = 0.35 * chronic + 0.8 * randn()
        intervention = (time >= 5 && rand() < 0.35) ? 1.0 : 0.0
        reg_context = support + structure + slp + school + scaffolding + transition + accommodation * support_need
        score =
            0.70 * prev +
            0.90 * time +
            1.15 * support +
            1.05 * structure +
            0.90 * slp +
            0.80 * school +
            0.95 * scaffolding +
            0.80 * transition +
            0.90 * accommodation * support_need +
            1.10 * intervention -
            1.25 * acute -
            0.90 * chronic +
            0.75 * temperament * support -
            0.80 * temperament * acute +
            0.25 * reg_context +
            2.5 * randn()
        regulation[t] += score
        context[t] += reg_context
        stress[t] += acute
        sleep[t] += slp
        prev = score
    end
end

mkpath(joinpath(@__DIR__, "..", "outputs"))
open(joinpath(@__DIR__, "..", "outputs", "julia_regulation_development.csv"), "w") do io
    println(io, "time,average_regulation,average_regulatory_context,average_stress,average_sleep")
    for t in 1:waves
        println(io, "$(t-1),$(regulation[t]/n),$(context[t]/n),$(stress[t]/n),$(sleep[t]/n)")
    end
end
println("Wrote outputs/julia_regulation_development.csv")
