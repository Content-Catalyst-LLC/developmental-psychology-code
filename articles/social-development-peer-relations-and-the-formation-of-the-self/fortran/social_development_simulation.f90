program social_development_simulation
  implicit none
  integer, parameter :: n=950, waves=10
  integer :: i,t
  real :: r, baseline, peer, friendship, family, interpretation, chronic
  real :: connectedness, teacher, antibullying, inclusion, restorative
  real :: prev, exclusion, bullying, digital, context, score
  real :: avg_score(waves), avg_context(waves), avg_exclusion(waves)
  call random_seed()
  avg_score=0.0; avg_context=0.0; avg_exclusion=0.0

  do i=1,n
    call random_number(r); baseline=42.0+16.0*r
    call random_number(r); chronic=merge(1.0,0.0,r<0.22)
    prev=baseline
    do t=1,waves
      call random_number(r); peer=2.0*r-1.0
      call random_number(r); friendship=2.0*r-1.0
      call random_number(r); family=2.0*r-1.0
      call random_number(r); interpretation=2.0*r-1.0
      call random_number(r); connectedness=1.2*r-0.6
      call random_number(r); teacher=1.2*r-0.6
      call random_number(r); antibullying=1.2*r-0.6
      call random_number(r); inclusion=1.2*r-0.6
      call random_number(r); restorative=1.0*r-0.5
      exclusion=0.45*chronic-0.25*antibullying-0.20*inclusion
      bullying=0.35*chronic+0.25*exclusion-0.30*antibullying
      digital=0.25*exclusion-0.15*friendship
      context=peer+friendship+family+interpretation+connectedness+teacher+antibullying+inclusion+restorative
      score=0.70*prev+0.85*real(t-1)+1.10*peer+1.00*friendship+0.95*family+0.85*interpretation+0.90*connectedness+0.75*teacher+0.80*antibullying+0.80*inclusion+0.60*restorative-1.20*exclusion-1.10*bullying-0.75*digital-0.90*chronic+0.25*context
      avg_score(t)=avg_score(t)+score
      avg_context(t)=avg_context(t)+context
      avg_exclusion(t)=avg_exclusion(t)+exclusion
      prev=score
    end do
  end do

  open(unit=10,file="outputs/fortran_social_development.csv",status="replace")
  write(10,'(A)') "time,average_social_self,average_social_context,average_exclusion"
  do t=1,waves
    write(10,'(I0,A,F10.4,A,F10.4,A,F10.4)') t-1,",",avg_score(t)/real(n),",",avg_context(t)/real(n),",",avg_exclusion(t)/real(n)
  end do
  close(10)
  print *, "Wrote outputs/fortran_social_development.csv"
end program social_development_simulation
