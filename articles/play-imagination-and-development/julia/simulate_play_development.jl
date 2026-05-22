using Random
Random.seed!(2026)

n = 900
waves = 10
development = zeros(waves)
context = zeros(waves)
restriction = zeros(waves)
stress = zeros(waves)

for i in 1:n
    baseline = 50 + 8 * randn()
    pretend_base, social_base, constructive_base, outdoor_base, support_base = randn(5)
    chronic = rand() < 0.30 ? 1.0 : 0.0
    space, adult, inclusion, safety, materials = 0.6*randn(), 0.6*randn(), 0.6*randn(), 0.6*randn(), 0.5*randn()
    prev = baseline

    for t in 1:waves
        time = t - 1
        pretend = pretend_base + 0.7 * randn()
        social = social_base + 0.7 * randn()
        constructive = constructive_base + 0.7 * randn()
        outdoor = outdoor_base + 0.7 * randn()
        support = support_base + 0.7 * randn()
        acute = 0.35 * chronic + 0.8 * randn()
        play_restriction = 0.35 * chronic - 0.20 * space - 0.20 * safety + 0.7 * randn()
        peer = 0.35 * inclusion + 0.25 * social - 0.20 * play_restriction + 0.7 * randn()
        play_context = support + peer + space + adult + inclusion + safety + materials
        score =
            0.70 * prev +
            0.85 * time +
            1.15 * pretend +
            1.05 * social +
            1.00 * constructive +
            0.90 * outdoor +
            1.00 * support +
            0.90 * peer +
            0.75 * space +
            0.70 * adult +
            0.65 * safety +
            0.65 * materials -
            1.15 * acute -
            0.90 * chronic -
            0.90 * play_restriction +
            0.25 * play_context +
            2.5 * randn()
        development[t] += score
        context[t] += play_context
        restriction[t] += play_restriction
        stress[t] += acute
        prev = score
    end
end

mkpath(joinpath(@__DIR__, "..", "outputs"))
open(joinpath(@__DIR__, "..", "outputs", "julia_play_development.csv"), "w") do io
    println(io, "time,average_development,average_play_context,average_restriction,average_stress")
    for t in 1:waves
        println(io, "$(t-1),$(development[t]/n),$(context[t]/n),$(restriction[t]/n),$(stress[t]/n)")
    end
end
println("Wrote outputs/julia_play_development.csv")
