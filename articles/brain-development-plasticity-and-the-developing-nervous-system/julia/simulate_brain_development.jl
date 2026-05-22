using Random
Random.seed!(2026)

n = 900
waves = 10
neural = zeros(waves)
outcome = zeros(waves)
context = zeros(waves)
stress = zeros(waves)

for i in 1:n
    baseline = 50 + 7 * randn()
    family_base, learning_base, sleep_base, sensory_base = randn(4)
    chronic = rand() < 0.30 ? 1.0 : 0.0
    school, safety, health, envrisk = 0.6*randn(), 0.6*randn(), 0.6*randn(), 0.6*randn()
    prev = baseline
    for t in 1:waves
        time = t - 1
        family = family_base + 0.7 * randn()
        learning = learning_base + 0.7 * randn()
        sleep = sleep_base + 0.5 * randn()
        sensory = sensory_base + 0.5 * randn()
        acute = 0.35 * chronic + 0.8 * randn()
        support_context = family + learning + sleep + sensory + school + safety + health - envrisk
        nstate = 0.70*prev + 0.85*time - 0.010*time^2 + 1.15*family + 1.20*learning + 0.90*sleep + 0.75*sensory + 0.80*school + 0.70*safety + 0.75*health - 1.30*acute - 0.90*chronic - 0.70*envrisk + 0.25*support_context + 2.5*randn()
        dev = 0.72*nstate + 0.85*family + 0.80*learning + 0.70*sleep + 0.65*sensory - 0.95*acute - 0.65*envrisk + 2.4*randn()
        neural[t] += nstate; outcome[t] += dev; context[t] += support_context; stress[t] += acute
        prev = nstate
    end
end

mkpath(joinpath(@__DIR__, "..", "outputs"))
open(joinpath(@__DIR__, "..", "outputs", "julia_brain_development.csv"), "w") do io
    println(io, "time,average_neural_state,average_developmental_outcome,average_stress,average_support_context")
    for t in 1:waves
        println(io, "$(t-1),$(neural[t]/n),$(outcome[t]/n),$(stress[t]/n),$(context[t]/n)")
    end
end
println("Wrote outputs/julia_brain_development.csv")
