using Random
Random.seed!(2026)

n = 950
waves = 10
social_self = zeros(waves)
context = zeros(waves)
exclusion = zeros(waves)
bullying = zeros(waves)
digital = zeros(waves)

for i in 1:n
    baseline = 50 + 8 * randn()
    peer_base, friend_base, family_base, interpretation_base = randn(4)
    chronic = rand() < 0.22 ? 1.0 : 0.0
    connectedness, teacher, antibullying, inclusion, restorative = 0.6*randn(), 0.6*randn(), 0.6*randn(), 0.6*randn(), 0.5*randn()
    prev = baseline

    for t in 1:waves
        time = t - 1
        peer = peer_base + 0.7 * randn()
        friendship = friend_base + 0.7 * randn()
        family = family_base + 0.7 * randn()
        interpretation = interpretation_base + 0.5 * randn()
        excl = 0.45 * chronic - 0.25 * antibullying - 0.20 * inclusion + 0.7 * randn()
        bully = 0.35 * chronic + 0.25 * excl - 0.30 * antibullying + 0.7 * randn()
        dig = 0.25 * excl - 0.15 * friendship + 0.7 * randn()
        support_context = peer + friendship + family + interpretation + connectedness + teacher + antibullying + inclusion + restorative
        score = 0.70 * prev + 0.85 * time + 1.10 * peer + 1.00 * friendship + 0.95 * family + 0.85 * interpretation + 0.90 * connectedness + 0.75 * teacher + 0.80 * antibullying + 0.80 * inclusion + 0.60 * restorative - 1.20 * excl - 1.10 * bully - 0.75 * dig - 0.90 * chronic + 0.25 * support_context + 2.5 * randn()
        social_self[t] += score
        context[t] += support_context
        exclusion[t] += excl
        bullying[t] += bully
        digital[t] += dig
        prev = score
    end
end

mkpath(joinpath(@__DIR__, "..", "outputs"))
open(joinpath(@__DIR__, "..", "outputs", "julia_social_development.csv"), "w") do io
    println(io, "time,average_social_self,average_social_context,average_exclusion,average_bullying,average_digital_comparison")
    for t in 1:waves
        println(io, "$(t-1),$(social_self[t]/n),$(context[t]/n),$(exclusion[t]/n),$(bullying[t]/n),$(digital[t]/n)")
    end
end
println("Wrote outputs/julia_social_development.csv")
