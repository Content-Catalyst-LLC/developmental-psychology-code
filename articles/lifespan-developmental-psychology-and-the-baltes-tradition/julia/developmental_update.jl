# Toy recursive developmental update model.

development = 0.45
caregiving = 0.75
opportunity = 0.70
risk = 0.30
learning_rate = 0.10

for t in 1:10
    development = development + learning_rate * (0.30 * caregiving + 0.30 * opportunity - 0.25 * risk)
    development = clamp(development, 0.0, 1.0)
    println("Time ", t, ": developmental functioning = ", round(development, digits=3))
end
