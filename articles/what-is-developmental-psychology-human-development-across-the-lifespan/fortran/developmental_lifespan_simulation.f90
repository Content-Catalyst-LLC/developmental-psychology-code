program developmental_lifespan_simulation
  implicit none
  integer, parameter :: n=900, waves=10
  integer :: i,t
  real :: r, baseline, caregiver, family, school_support, support_need, structural_risk
  real :: climate, accommodation, counseling, language_access, community
  real :: prev, time, acute, current, intervention, context, score
  real :: development(waves), protective(waves), support(waves), stress(waves), intervention_rate(waves)

  call random_seed()
  development=0.0
  protective=0.0
  support=0.0
  stress=0.0
  intervention_rate=0.0

  do i=1,n
    call random_number(r); baseline=42.0+16.0*r
    call random_number(r); caregiver=2.0*r-1.0
    call random_number(r); family=2.0*r-1.0
    call random_number(r); school_support=2.0*r-1.0
    call random_number(r); support_need=merge(1.0,0.0,r<0.18)
    call random_number(r); structural_risk=merge(1.0,0.0,r<0.35)
    call random_number(r); climate=1.2*r-0.6
    call random_number(r); accommodation=1.2*r-0.6
    call random_number(r); counseling=1.0*r-0.5
    call random_number(r); language_access=1.0*r-0.5
    call random_number(r); community=1.4*r-0.7
    prev=baseline

    do t=1,waves
      time=real(t-1)
      call random_number(r); acute=0.35*structural_risk-0.15*caregiver+0.90*(r-0.5)
      call random_number(r); current=caregiver+family+school_support+climate+counseling+0.65*(r-0.5)
      call random_number(r); intervention=merge(1.0,0.0,time>=5.0 .and. r<0.32)
      context=caregiver+family+school_support+climate+counseling+language_access+community+accommodation*(1.0+support_need)

      score=0.72*prev+0.90*time+1.10*caregiver+0.90*family+0.85*school_support+0.75*climate+0.65*counseling+0.55*language_access+0.55*community+0.95*accommodation*support_need-2.30*structural_risk-1.45*acute+1.80*intervention+0.70*current+0.28*context

      development(t)=development(t)+score
      protective(t)=protective(t)+context
      support(t)=support(t)+current
      stress(t)=stress(t)+acute
      intervention_rate(t)=intervention_rate(t)+intervention
      prev=score
    end do
  end do

  open(unit=10,file="outputs/fortran_developmental_lifespan.csv",status="replace")
  write(10,'(A)') "time,average_development,average_protective_context,average_support,average_stress,intervention_rate"
  do t=1,waves
    write(10,'(I0,A,F10.4,A,F10.4,A,F10.4,A,F10.4,A,F10.4)') t-1,",",development(t)/real(n),",",protective(t)/real(n),",",support(t)/real(n),",",stress(t)/real(n),",",intervention_rate(t)/real(n)
  end do
  close(10)

  print *, "Wrote outputs/fortran_developmental_lifespan.csv"
end program developmental_lifespan_simulation
