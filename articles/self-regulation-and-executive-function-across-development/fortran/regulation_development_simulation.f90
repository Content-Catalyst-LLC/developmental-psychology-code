program regulation_development_simulation
  implicit none
  integer, parameter :: n=920, waves=10
  integer :: i,t
  real :: r, baseline, support, structure, sleepq, chronic, temperament, support_need
  real :: school, scaffolding, accommodation, transition, prev, acute, intervention, context, score
  real :: avg_score(waves), avg_context(waves), avg_stress(waves)
  call random_seed()
  avg_score=0.0; avg_context=0.0; avg_stress=0.0

  do i=1,n
    call random_number(r); baseline=42.0+16.0*r
    call random_number(r); chronic=merge(1.0,0.0,r<0.30)
    call random_number(r); support_need=merge(1.0,0.0,r<0.18)
    call random_number(r); temperament=2.0*r-1.0
    prev=baseline
    do t=1,waves
      call random_number(r); support=2.0*r-1.0
      call random_number(r); structure=2.0*r-1.0
      call random_number(r); sleepq=2.0*r-1.0
      call random_number(r); school=1.2*r-0.6
      call random_number(r); scaffolding=1.2*r-0.6
      call random_number(r); accommodation=1.2*r-0.6
      call random_number(r); transition=1.0*r-0.5
      call random_number(r); acute=0.35*chronic+0.8*(r-0.5)
      call random_number(r); intervention=merge(1.0,0.0,real(t-1)>=5.0 .and. r<0.35)
      context=support+structure+sleepq+school+scaffolding+transition+accommodation*support_need
      score=0.70*prev+0.90*real(t-1)+1.15*support+1.05*structure+0.90*sleepq+0.80*school+0.95*scaffolding+0.80*transition+0.90*accommodation*support_need+1.10*intervention-1.25*acute-0.90*chronic+0.75*temperament*support-0.80*temperament*acute+0.25*context
      avg_score(t)=avg_score(t)+score
      avg_context(t)=avg_context(t)+context
      avg_stress(t)=avg_stress(t)+acute
      prev=score
    end do
  end do

  open(unit=10,file="outputs/fortran_regulation_development.csv",status="replace")
  write(10,'(A)') "time,average_regulation,average_regulatory_context,average_stress"
  do t=1,waves
    write(10,'(I0,A,F10.4,A,F10.4,A,F10.4)') t-1,",",avg_score(t)/real(n),",",avg_context(t)/real(n),",",avg_stress(t)/real(n)
  end do
  close(10)
  print *, "Wrote outputs/fortran_regulation_development.csv"
end program regulation_development_simulation
