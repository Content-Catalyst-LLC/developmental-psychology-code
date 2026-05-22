program moral_development_simulation
  implicit none
  integer, parameter :: n=920, waves=10
  integer :: i,t
  real :: r, baseline, guidance, empathy, fairness, regulation, harm, chronic
  real :: school, repair, exclusion, pressure, context, conscience, action, prev
  real :: avg_conscience(waves), avg_action(waves), avg_context(waves)
  call random_seed()
  avg_conscience=0.0; avg_action=0.0; avg_context=0.0
  do i=1,n
    call random_number(r); baseline=42.0+16.0*r
    call random_number(r); chronic=merge(1.0,0.0,r<0.22)
    prev=baseline
    do t=1,waves
      call random_number(r); guidance=2.0*r-1.0
      call random_number(r); empathy=2.0*r-1.0
      call random_number(r); fairness=2.0*r-1.0
      call random_number(r); regulation=2.0*r-1.0
      call random_number(r); harm=2.0*r-1.0
      call random_number(r); school=1.2*r-0.6
      call random_number(r); repair=1.2*r-0.6
      call random_number(r); exclusion=0.42*chronic+0.70*(r-0.5)
      call random_number(r); pressure=0.25*exclusion-0.18*fairness+0.65*(r-0.5)
      context=guidance+empathy+fairness+regulation+harm+repair+school-exclusion-pressure
      conscience=0.70*prev+0.80*real(t-1)+guidance+empathy+fairness+regulation+harm+repair+school-exclusion+0.25*context
      action=0.55*conscience+regulation+fairness+empathy+harm+repair-pressure-exclusion
      avg_conscience(t)=avg_conscience(t)+conscience
      avg_action(t)=avg_action(t)+action
      avg_context(t)=avg_context(t)+context
      prev=conscience
    end do
  end do
  open(unit=10,file="outputs/fortran_moral_development.csv",status="replace")
  write(10,'(A)') "time,average_conscience,average_moral_action,average_moral_context"
  do t=1,waves
    write(10,'(I0,A,F10.4,A,F10.4,A,F10.4)') t-1,",",avg_conscience(t)/real(n),",",avg_action(t)/real(n),",",avg_context(t)/real(n)
  end do
  close(10)
  print *, "Wrote outputs/fortran_moral_development.csv"
end program moral_development_simulation
