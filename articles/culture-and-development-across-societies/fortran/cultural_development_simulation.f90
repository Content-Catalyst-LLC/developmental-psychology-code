program cultural_development_simulation
  implicit none

  integer, parameter :: n_children = 850
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: family, fit, mismatch, support, flexibility, previous_score, score
  real :: random_value
  real :: trajectory(n_periods)

  call random_seed()
  trajectory = 0.0

  do i = 1, n_children
     call random_number(random_value)
     family = 2.0 * random_value - 1.0

     call random_number(random_value)
     fit = 2.0 * random_value - 1.0

     call random_number(random_value)
     mismatch = 2.0 * random_value - 1.0

     call random_number(random_value)
     support = 2.0 * random_value - 1.0

     call random_number(random_value)
     flexibility = 2.0 * random_value - 1.0

     call random_number(random_value)
     previous_score = 47.0 + 6.0 * random_value

     do t = 1, n_periods
        call random_number(random_value)

        score = 0.70 * previous_score + &
                0.18 * real(t - 1) + &
                1.00 * family + &
                0.95 * fit + &
                0.90 * support + &
                0.80 * flexibility - &
                1.00 * mismatch + &
                2.3 * (random_value - 0.5)

        trajectory(t) = trajectory(t) + score
        previous_score = score
     end do
  end do

  open(unit=10, file="outputs/fortran_cultural_development.csv", status="replace")
  write(10, '(A)') "time,average_development"

  do t = 1, n_periods
     write(10, '(I0,A,F10.4)') t - 1, ",", trajectory(t) / real(n_children)
  end do

  close(10)

  print *, "Wrote outputs/fortran_cultural_development.csv"
end program cultural_development_simulation
