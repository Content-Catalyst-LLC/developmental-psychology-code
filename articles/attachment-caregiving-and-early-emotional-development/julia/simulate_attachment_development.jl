using Random
Random.seed!(2026)

n = 900
waves = 10
regulation = zeros(waves)
context = zeros(waves)
stress = zeros(waves)
care = zeros(waves)

for i in 1:n
    baseline = 50 + 8 * randn()
    care_base, repair_base, caregiver_support_base, temperament = randn(4)
    chronic = rand() < 0.30 ? 1.0 : 0.0
    support_need = rand() < 0.16 ? 1.0 : 0.0
    childcare, safety, services, ecology = 0.6*randn(), 0.6*randn(), 0.6*randn(), 0.6*randn()
    prev = baseline

    for t in 1:waves
        time = t - 1
        current_care = care_base + 0.7 * randn()
        current_repair = repair_base + 0.7 * randn()
        current_support = caregiver_support_base + 0.7 * randn()
        current_stress = 0.35 * chronic + 0.8 * randn()
        support_context = current_care + current_repair + current_support + childcare + safety + services + ecology
        score =
            0.70 * prev +
            0.90 * time +
            1.35 * current_care +
            1.10 * current_repair +
            1.00 * current_support +
            0.80 * childcare +
            0.75 * safety +
            0.80 * services +
            0.75 * ecology -
            1.30 * current_stress -
            0.95 * chronic +
            0.75 * temperament * current_care -
            0.85 * temperament * current_stress +
            0.70 * support_need * services +
            0.25 * support_context +
            2.5 * randn()
        regulation[t] += score
        context[t] += support_context
        stress[t] += current_stress
        care[t] += current_care
        prev = score
    end
end

mkpath(joinpath(@__DIR__, "..", "outputs"))
open(joinpath(@__DIR__, "..", "outputs", "julia_attachment_development.csv"), "w") do io
    println(io, "time,average_regulation,average_care,average_stress,average_support_context")
    for t in 1:waves
        println(io, "$(t-1),$(regulation[t]/n),$(care[t]/n),$(stress[t]/n),$(context[t]/n)")
    end
end
println("Wrote outputs/julia_attachment_development.csv")
