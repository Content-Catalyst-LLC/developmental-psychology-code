using Random
Random.seed!(2026)

n = 900
waves = 10

development = zeros(waves)
protective = zeros(waves)
support = zeros(waves)
stress = zeros(waves)
intervention_rate = zeros(waves)

for i in 1:n
    baseline = 50 + 8 * randn()
    caregiver = randn()
    family = randn()
    school_support = randn()
    support_need = rand() < 0.18 ? 1.0 : 0.0
    structural_risk = rand() < 0.35 ? 1.0 : 0.0
    school_climate = 0.6 * randn()
    accommodation = 0.6 * randn()
    counseling = 0.5 * randn()
    language = 0.5 * randn()
    community = 0.7 * randn()
    prev = baseline

    for t in 1:waves
        time = t - 1
        acute = 0.35 * structural_risk - 0.15 * caregiver + 0.90 * randn()
        current = caregiver + family + school_support + school_climate + counseling + 0.65 * randn()
        intervention = (time >= 5 && rand() < 0.32) ? 1.0 : 0.0
        context = caregiver + family + school_support + school_climate + counseling + language + community + accommodation * (1.0 + support_need)

        score =
            0.72 * prev +
            0.90 * time +
            1.10 * caregiver +
            0.90 * family +
            0.85 * school_support +
            0.75 * school_climate +
            0.65 * counseling +
            0.55 * language +
            0.55 * community +
            0.95 * accommodation * support_need -
            2.30 * structural_risk -
            1.45 * acute +
            1.80 * intervention +
            0.70 * current +
            0.28 * context +
            2.5 * randn()

        development[t] += score
        protective[t] += context
        support[t] += current
        stress[t] += acute
        intervention_rate[t] += intervention
        prev = score
    end
end

mkpath(joinpath(@__DIR__, "..", "outputs"))

open(joinpath(@__DIR__, "..", "outputs", "julia_developmental_lifespan.csv"), "w") do io
    println(io, "time,average_development,average_protective_context,average_support,average_stress,intervention_rate")
    for t in 1:waves
        println(io, "$(t-1),$(development[t]/n),$(protective[t]/n),$(support[t]/n),$(stress[t]/n),$(intervention_rate[t]/n)")
    end
end

println("Wrote outputs/julia_developmental_lifespan.csv")
