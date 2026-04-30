program developmental_growth
  implicit none

  integer :: t
  real :: functioning
  real, parameter :: support = 0.72
  real, parameter :: risk = 0.25
  real, parameter :: rate = 0.08

  functioning = 0.40

  print *, "Time", "Functioning"

  do t = 1, 12
     functioning = functioning + rate * (support - risk)
     if (functioning > 1.0) functioning = 1.0
     if (functioning < 0.0) functioning = 0.0
     print *, t, functioning
  end do

end program developmental_growth
