using Random
Random.seed!(2026)

n = 900
waves = 10
language = zeros(waves)
context = zeros(waves)
stress = zeros(waves)
interaction = zeros(waves)

for i in 1:n
    baseline = 48 + 8 * randn()
    interaction_base, reading_base, joint_base, turns_base, hearing = randn(5)
    multilingual = rand() < 0.32 ? 1.0 : 0.0
    chronic = rand() < 0.28 ? 1.0 : 0.0
    ecology, books, education, home_language = 0.6*randn(), 0.6*randn(), 0.6*randn(), 0.6*randn()
    prev = baseline

    for t in 1:waves
        time = t - 1
        current_interaction = interaction_base + 0.7 * randn()
        current_reading = reading_base + 0.7 * randn()
        current_joint = joint_base + 0.7 * randn()
        current_turns = turns_base + 0.7 * randn()
        current_stress = 0.30 * chronic + 0.8 * randn()
        support_context = current_interaction + current_reading + current_joint + current_turns + hearing + ecology + books + education + home_language
        score =
            0.70 * prev +
            0.95 * time -
            0.015 * time^2 +
            1.30 * current_interaction +
            1.10 * current_reading +
            1.05 * current_joint +
            1.00 * current_turns +
            0.95 * hearing +
            0.70 * ecology +
            0.70 * books +
            0.75 * education +
            0.65 * home_language +
            0.50 * multilingual * home_language -
            1.20 * current_stress -
            0.90 * chronic +
            0.25 * support_context +
            2.5 * randn()
        language[t] += score
        context[t] += support_context
        stress[t] += current_stress
        interaction[t] += current_interaction
        prev = score
    end
end

mkpath(joinpath(@__DIR__, "..", "outputs"))
open(joinpath(@__DIR__, "..", "outputs", "julia_language_development.csv"), "w") do io
    println(io, "time,average_language,average_interaction,average_stress,average_language_support_context")
    for t in 1:waves
        println(io, "$(t-1),$(language[t]/n),$(interaction[t]/n),$(stress[t]/n),$(context[t]/n)")
    end
end
println("Wrote outputs/julia_language_development.csv")
