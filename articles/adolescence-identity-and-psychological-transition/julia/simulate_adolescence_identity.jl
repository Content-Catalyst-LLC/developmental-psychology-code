using Random
Random.seed!(2026)
n=900; waves=10
identity=zeros(waves); support=zeros(waves); exclusion=zeros(waves); digital=zeros(waves)
for i in 1:n
    baseline=50+8*randn(); peer=randn(); family=randn(); connected=randn(); future=randn()
    chronic=rand() < 0.24 ? 1.0 : 0.0
    climate=0.6*randn(); counseling=0.5*randn(); extra=0.5*randn(); safety=0.6*randn(); dsafe=0.5*randn()
    prev=baseline
    for t in 1:waves
        time=t-1
        p=peer+0.7*randn(); f=family+0.7*randn(); s=connected+0.7*randn(); a=future+0.7*randn()
        x=0.45*chronic-0.20*safety+0.70*randn()
        d=0.30*chronic-0.25*dsafe+0.65*randn()
        ctx=p+f+s+a+climate+counseling+extra+safety+dsafe
        score=0.70*prev+0.85*time+1.10*p+1.00*f+0.95*s+0.90*a+0.80*climate+0.70*counseling+0.65*extra+0.85*safety+0.55*dsafe-1.25*x-0.75*d-0.90*chronic+2.5*randn()
        identity[t]+=score; support[t]+=ctx; exclusion[t]+=x; digital[t]+=d; prev=score
    end
end
mkpath(joinpath(@__DIR__,"..","outputs"))
open(joinpath(@__DIR__,"..","outputs","julia_adolescence_identity.csv"),"w") do io
    println(io,"time,average_identity_score,average_support_context,average_exclusion,average_digital_stress")
    for t in 1:waves
        println(io,"$(t-1),$(identity[t]/n),$(support[t]/n),$(exclusion[t]/n),$(digital[t]/n)")
    end
end
println("Wrote outputs/julia_adolescence_identity.csv")
