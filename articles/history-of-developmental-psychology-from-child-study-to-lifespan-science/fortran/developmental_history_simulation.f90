program developmental_history_simulation
  implicit none
  integer, parameter :: start_year=1900, end_year=2025
  integer :: y
  real :: child, lifespan, ecological, systems, critique, broadening

  open(unit=10,file="outputs/fortran_developmental_history.csv",status="replace")
  write(10,'(A)') "year,child_centered_index,lifespan_index,ecological_index,systems_index,critique_index,broadening_index"

  do y=start_year,end_year
     child = 1.0 / (1.0 + exp(0.060 * real(y - 1925)))
     lifespan = 1.0 / (1.0 + exp(-0.095 * real(y - 1970)))
     ecological = 1.0 / (1.0 + exp(-0.080 * real(y - 1975)))
     systems = 1.0 / (1.0 + exp(-0.090 * real(y - 1995)))
     critique = 1.0 / (1.0 + exp(-0.060 * real(y - 1970))) + 0.25 / (1.0 + exp(-0.090 * real(y - 2000)))
     broadening = ecological + lifespan + systems + 0.30 * critique

     write(10,'(I0,A,F10.4,A,F10.4,A,F10.4,A,F10.4,A,F10.4,A,F10.4)') y,",",child,",",lifespan,",",ecological,",",systems,",",critique,",",broadening
  end do

  close(10)
  print *, "Wrote outputs/fortran_developmental_history.csv"
end program developmental_history_simulation
