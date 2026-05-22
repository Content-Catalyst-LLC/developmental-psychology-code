using Random
Random.seed!(2026)
n = 920
waves = 10
conscience = zeros(waves)
action = zeros(waves)
context = zeros(waves)
for i in 1:n
    baseline = 50 + 8 * randn()
    guidance_base, empathy_base, fairness_base, regulation_base, harm_base = randn(5)
    chronic = rand() < 0.22 ? 1.0 : 0.0
    school_climate, restorative, punitive, bullying, digital = 0.6*randn(), 0.6*randn(), 0.6*randn(), 0.6*randn(), 0.5*randn()
    prev = baseline
    for t in 1:waves
        time = t - 1
        guidance = guidance_base + 0.7 * randn()
        empathy = empathy_base + 0.7 * randn()
        fairness = fairness_base + 0.7 * randn()
        regulation = regulation_base + 0.5 * randn()
        harm = harm_base + 0.6 * randn()
        repair = 0.35 * restorative + 0.25 * guidance + 0.20 * school_climate - 0.20 * punitive + 0.65 * randn()
        excl = 0.42 * chronic - 0.22 * bullying + 0.18 * punitive + 0.70 * randn()
        pressure = 0.25 * excl - 0.18 * fairness - 0.15 * bullying + 0.65 * randn()
        moral_context = guidance + empathy + fairness + regulation + harm + repair + school_climate + restorative + bullying + digital - punitive
        cons = 0.70 * prev + 0.80 * time + 1.05 * guidance + 1.00 * empathy + 0.95 * fairness + 0.90 * regulation + 1.00 * harm + 0.95 * repair + 0.80 * school_climate + 0.90 * restorative + 0.80 * bullying + 0.55 * digital - 1.00 * punitive - 1.20 * excl - 0.85 * chronic + 0.25 * moral_context + 2.5 * randn()
        act = 0.55 * cons + 1.10 * regulation + 0.85 * fairness + 0.80 * empathy + 0.75 * harm + 0.70 * repair - 1.10 * pressure - 0.95 * excl + 2.4 * randn()
        conscience[t] += cons
        action[t] += act
        context[t] += moral_context
        prev = cons
    end
end
mkpath(joinpath(@__DIR__, "..", "outputs"))
open(joinpath(@__DIR__, "..", "outputs", "julia_moral_development.csv"), "w") do io
    println(io, "time,average_conscience,average_moral_action,average_moral_context")
    for t in 1:waves
        println(io, "$(t-1),$(conscience[t]/n),$(action[t]/n),$(context[t]/n)")
    end
end
println("Wrote outputs/julia_moral_development.csv")
