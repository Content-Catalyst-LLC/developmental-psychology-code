using Random
Random.seed!(2026)

years = collect(1900:2025)
n = length(years)

function logistic(x)
    return 1.0 / (1.0 + exp(-x))
end

child = [1.0 / (1.0 + exp(0.060 * (y - 1925))) for y in years]
lifespan = [logistic(0.095 * (y - 1970)) for y in years]
ecological = [logistic(0.080 * (y - 1975)) for y in years]
systems = [logistic(0.090 * (y - 1995)) for y in years]
critique = [logistic(0.060 * (y - 1970)) + 0.25 * logistic(0.090 * (y - 2000)) for y in years]

broadening = ecological .+ lifespan .+ systems .+ 0.30 .* critique
mkpath(joinpath(@__DIR__, "..", "outputs"))

open(joinpath(@__DIR__, "..", "outputs", "julia_developmental_history.csv"), "w") do io
    println(io, "year,child_centered_index,lifespan_index,ecological_index,systems_index,critique_index,broadening_index")
    for i in eachindex(years)
        println(io, "$(years[i]),$(child[i]),$(lifespan[i]),$(ecological[i]),$(systems[i]),$(critique[i]),$(broadening[i])")
    end
end

println("Wrote outputs/julia_developmental_history.csv")
