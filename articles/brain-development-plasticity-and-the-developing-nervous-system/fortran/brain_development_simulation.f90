program brain_development_simulation
  implicit none
  integer, parameter :: n=900, waves=10
  integer :: i,t
  real :: r, baseline, family, learning, sleepq, sensory, chronic, school, safety, health, envrisk
  real :: prev, acute, support_context, nstate, dev, time
  real :: avg_neural(waves), avg_outcome(waves), avg_context(waves), avg_stress(waves)
  call random_seed()
  avg_neural=0.0; avg_outcome=0.0; avg_context=0.0; avg_stress=0.0
  do i=1,n
    call random_number(r); baseline=43.0+14.0*r
    call random_number(r); chronic=merge(1.0,0.0,r<0.30)
    prev=baseline
    do t=1,waves
      time=real(t-1)
      call random_number(r); family=2.0*r-1.0
      call random_number(r); learning=2.0*r-1.0
      call random_number(r); sleepq=2.0*r-1.0
      call random_number(r); sensory=2.0*r-1.0
      call random_number(r); school=1.2*r-0.6
      call random_number(r); safety=1.2*r-0.6
      call random_number(r); health=1.2*r-0.6
      call random_number(r); envrisk=1.2*r-0.6
      call random_number(r); acute=0.35*chronic+0.8*(r-0.5)
      support_context=family+learning+sleepq+sensory+school+safety+health-envrisk
      nstate=0.70*prev+0.85*time-0.010*time*time+1.15*family+1.20*learning+0.90*sleepq+0.75*sensory+0.80*school+0.70*safety+0.75*health-1.30*acute-0.90*chronic-0.70*envrisk+0.25*support_context
      dev=0.72*nstate+0.85*family+0.80*learning+0.70*sleepq+0.65*sensory-0.95*acute-0.65*envrisk
      avg_neural(t)=avg_neural(t)+nstate; avg_outcome(t)=avg_outcome(t)+dev; avg_context(t)=avg_context(t)+support_context; avg_stress(t)=avg_stress(t)+acute
      prev=nstate
    end do
  end do
  open(unit=10,file="outputs/fortran_brain_development.csv",status="replace")
  write(10,'(A)') "time,average_neural_state,average_developmental_outcome,average_support_context,average_stress"
  do t=1,waves
    write(10,'(I0,A,F10.4,A,F10.4,A,F10.4,A,F10.4)') t-1,",",avg_neural(t)/real(n),",",avg_outcome(t)/real(n),",",avg_context(t)/real(n),",",avg_stress(t)/real(n)
  end do
  close(10)
  print *, "Wrote outputs/fortran_brain_development.csv"
end program brain_development_simulation
