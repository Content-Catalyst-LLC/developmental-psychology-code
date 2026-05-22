program puberty_embodiment_simulation
  implicit none
  integer, parameter :: n=920, waves=10
  integer :: i,t
  real :: r, baseline, timing, family_base, peer_base, body_vulnerability, chronic
  real :: school, health, privacy, menstrual, disability, harassment, digital_safety
  real :: prev, time, progress, family, peer, body, stig, digital, context, score
  real :: adjustment(waves), protective(waves), stigma(waves), body_concern(waves), peer_comparison(waves)
  call random_seed()
  adjustment=0.0; protective=0.0; stigma=0.0; body_concern=0.0; peer_comparison=0.0
  do i=1,n
    call random_number(r); baseline=42.0+16.0*r
    call random_number(r); timing=2.0*r-1.0
    call random_number(r); family_base=2.0*r-1.0
    call random_number(r); peer_base=2.0*r-1.0
    call random_number(r); body_vulnerability=2.0*r-1.0
    call random_number(r); chronic=merge(1.0,0.0,r<0.22)
    call random_number(r); school=1.2*r-0.6
    call random_number(r); health=1.2*r-0.6
    call random_number(r); privacy=1.0*r-0.5
    call random_number(r); menstrual=1.0*r-0.5
    call random_number(r); disability=1.2*r-0.6
    call random_number(r); harassment=1.2*r-0.6
    call random_number(r); digital_safety=1.0*r-0.5
    prev=baseline
    do t=1,waves
      time=real(t-1)
      call random_number(r); progress=time+0.4*(r-0.5)
      call random_number(r); family=family_base+0.7*(r-0.5)
      call random_number(r); peer=peer_base+0.7*(r-0.5)
      call random_number(r); body=body_vulnerability+0.25*abs(timing)+0.6*(r-0.5)
      call random_number(r); stig=0.42*chronic+0.20*peer-0.20*harassment+0.7*(r-0.5)
      call random_number(r); digital=0.25*body+0.20*chronic-0.25*digital_safety+0.65*(r-0.5)
      context=family+school+health+privacy+menstrual+disability+harassment+digital_safety
      score=0.70*prev+0.90*progress-0.95*abs(timing)+1.05*family-1.10*peer-0.85*body-1.20*stig-0.75*digital-0.80*chronic+0.80*school+0.75*health+0.70*privacy+0.65*menstrual+0.75*disability+0.80*harassment+0.55*digital_safety+0.25*context
      adjustment(t)=adjustment(t)+score; protective(t)=protective(t)+context; stigma(t)=stigma(t)+stig; body_concern(t)=body_concern(t)+body; peer_comparison(t)=peer_comparison(t)+peer; prev=score
    end do
  end do
  open(unit=10,file="outputs/fortran_puberty_embodiment.csv",status="replace")
  write(10,'(A)') "time,average_adjustment,average_protective_context,average_stigma,average_body_concern,average_peer_comparison"
  do t=1,waves
    write(10,'(I0,A,F10.4,A,F10.4,A,F10.4,A,F10.4,A,F10.4)') t-1,",",adjustment(t)/real(n),",",protective(t)/real(n),",",stigma(t)/real(n),",",body_concern(t)/real(n),",",peer_comparison(t)/real(n)
  end do
  close(10)
  print *, "Wrote outputs/fortran_puberty_embodiment.csv"
end program puberty_embodiment_simulation
