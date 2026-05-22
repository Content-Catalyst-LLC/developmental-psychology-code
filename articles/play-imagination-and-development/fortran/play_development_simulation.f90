program play_development_simulation
  implicit none
  integer, parameter :: n=900, waves=10
  integer :: i,t
  real :: r, baseline, pretend, social, constructive, outdoor, support, chronic
  real :: space, adult, inclusion, safety, materials
  real :: prev, acute, restrict, peer, context, score
  real :: avg_score(waves), avg_context(waves), avg_restrict(waves)
  call random_seed()
  avg_score=0.0; avg_context=0.0; avg_restrict=0.0

  do i=1,n
    call random_number(r); baseline=42.0+16.0*r
    call random_number(r); chronic=merge(1.0,0.0,r<0.30)
    prev=baseline
    do t=1,waves
      call random_number(r); pretend=2.0*r-1.0
      call random_number(r); social=2.0*r-1.0
      call random_number(r); constructive=2.0*r-1.0
      call random_number(r); outdoor=2.0*r-1.0
      call random_number(r); support=2.0*r-1.0
      call random_number(r); space=1.2*r-0.6
      call random_number(r); adult=1.2*r-0.6
      call random_number(r); inclusion=1.2*r-0.6
      call random_number(r); safety=1.2*r-0.6
      call random_number(r); materials=1.0*r-0.5
      call random_number(r); acute=0.35*chronic+0.8*(r-0.5)
      restrict=0.35*chronic-0.20*space-0.20*safety
      peer=0.35*inclusion+0.25*social-0.20*restrict
      context=support+peer+space+adult+inclusion+safety+materials
      score=0.70*prev+0.85*real(t-1)+1.15*pretend+1.05*social+1.00*constructive+0.90*outdoor+1.00*support+0.90*peer+0.75*space+0.70*adult+0.65*safety+0.65*materials-1.15*acute-0.90*chronic-0.90*restrict+0.25*context
      avg_score(t)=avg_score(t)+score
      avg_context(t)=avg_context(t)+context
      avg_restrict(t)=avg_restrict(t)+restrict
      prev=score
    end do
  end do

  open(unit=10,file="outputs/fortran_play_development.csv",status="replace")
  write(10,'(A)') "time,average_development,average_play_context,average_restriction"
  do t=1,waves
    write(10,'(I0,A,F10.4,A,F10.4,A,F10.4)') t-1,",",avg_score(t)/real(n),",",avg_context(t)/real(n),",",avg_restrict(t)/real(n)
  end do
  close(10)
  print *, "Wrote outputs/fortran_play_development.csv"
end program play_development_simulation
