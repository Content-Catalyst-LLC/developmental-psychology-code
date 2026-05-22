using Random
Random.seed!(2026)
n=920; waves=10
adjustment=zeros(waves); protective=zeros(waves); stigma=zeros(waves); body_concern=zeros(waves); peer_comparison=zeros(waves)
for i in 1:n
    baseline=50+8*randn(); timing=randn(); family_base=randn(); peer_base=randn(); body_vulnerability=randn(); chronic=rand()<0.22 ? 1.0 : 0.0
    school=0.6*randn(); health=0.6*randn(); privacy=0.5*randn(); menstrual=0.5*randn(); disability=0.6*randn(); harassment=0.6*randn(); digital_safety=0.5*randn()
    prev=baseline
    for t in 1:waves
        time=t-1; progress=time+0.4*randn(); family=family_base+0.7*randn(); peer=peer_base+0.7*randn()
        body=body_vulnerability+0.25*abs(timing)+0.6*randn()
        stig=0.42*chronic+0.20*peer-0.20*harassment+0.7*randn()
        digital=0.25*body+0.20*chronic-0.25*digital_safety+0.65*randn()
        context=family+school+health+privacy+menstrual+disability+harassment+digital_safety
        score=0.70*prev+0.90*progress-0.95*abs(timing)+1.05*family-1.10*peer-0.85*body-1.20*stig-0.75*digital-0.80*chronic+0.80*school+0.75*health+0.70*privacy+0.65*menstrual+0.75*disability+0.80*harassment+0.55*digital_safety+0.25*context+2.5*randn()
        adjustment[t]+=score; protective[t]+=context; stigma[t]+=stig; body_concern[t]+=body; peer_comparison[t]+=peer; prev=score
    end
end
mkpath(joinpath(@__DIR__,"..","outputs"))
open(joinpath(@__DIR__,"..","outputs","julia_puberty_embodiment.csv"),"w") do io
    println(io,"time,average_adjustment,average_protective_context,average_stigma,average_body_concern,average_peer_comparison")
    for t in 1:waves
        println(io,"$(t-1),$(adjustment[t]/n),$(protective[t]/n),$(stigma[t]/n),$(body_concern[t]/n),$(peer_comparison[t]/n)")
    end
end
println("Wrote outputs/julia_puberty_embodiment.csv")
