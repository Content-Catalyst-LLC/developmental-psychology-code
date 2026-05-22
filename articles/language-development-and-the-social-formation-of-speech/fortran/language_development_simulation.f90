program language_development_simulation
  implicit none
  integer, parameter :: n=900, waves=10
  integer :: i,t
  real :: r, baseline, interaction, reading, joint, turns, hearing, multilingual, chronic
  real :: ecology, books, education, home_language
  real :: prev, stress, support_context, score, time
  real :: avg_score(waves), avg_context(waves), avg_stress(waves)
  call random_seed()
  avg_score=0.0; avg_context=0.0; avg_stress=0.0

  do i=1,n
    call random_number(r); baseline=40.0+16.0*r
    call random_number(r); multilingual=merge(1.0,0.0,r<0.32)
    call random_number(r); chronic=merge(1.0,0.0,r<0.28)
    prev=baseline
    do t=1,waves
      time=real(t-1)
      call random_number(r); interaction=2.0*r-1.0
      call random_number(r); reading=2.0*r-1.0
      call random_number(r); joint=2.0*r-1.0
      call random_number(r); turns=2.0*r-1.0
      call random_number(r); hearing=2.0*r-1.0
      call random_number(r); ecology=1.2*r-0.6
      call random_number(r); books=1.2*r-0.6
      call random_number(r); education=1.2*r-0.6
      call random_number(r); home_language=1.2*r-0.6
      call random_number(r); stress=0.30*chronic+0.8*(r-0.5)
      support_context=interaction+reading+joint+turns+hearing+ecology+books+education+home_language
      score=0.70*prev+0.95*time-0.015*time*time+1.30*interaction+1.10*reading+1.05*joint+1.00*turns+0.95*hearing+0.70*ecology+0.70*books+0.75*education+0.65*home_language+0.50*multilingual*home_language-1.20*stress-0.90*chronic+0.25*support_context
      avg_score(t)=avg_score(t)+score
      avg_context(t)=avg_context(t)+support_context
      avg_stress(t)=avg_stress(t)+stress
      prev=score
    end do
  end do

  open(unit=10,file="outputs/fortran_language_development.csv",status="replace")
  write(10,'(A)') "time,average_language,average_language_support_context,average_stress"
  do t=1,waves
    write(10,'(I0,A,F10.4,A,F10.4,A,F10.4)') t-1,",",avg_score(t)/real(n),",",avg_context(t)/real(n),",",avg_stress(t)/real(n)
  end do
  close(10)
  print *, "Wrote outputs/fortran_language_development.csv"
end program language_development_simulation
