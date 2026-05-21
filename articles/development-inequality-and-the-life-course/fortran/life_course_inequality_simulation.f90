program life_course_inequality_simulation
  implicit none

  integer, parameter :: n_people = 900
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: resources, burden, support, previous_score, score
  real :: early_weight, transition_weight, random_value
  real :: trajectory(n_periods)

  call random_seed()
  trajectory = 0.0

  do i = 1, n_people
     call random_number(random_value)
     resources = 2.0 * random_value - 1.0
     call random_number(random_value)
     burden = 2.0 * random_value - 1.0
     call random_number(random_value)
     support = 2.0 * random_value - 1.0
     call random_number(random_value)
     previous_score = 47.0 + 6.0 * random_value

     do t = 1, n_periods
        early_weight = exp(-0.16 * real(t - 1))
        transition_weight = exp(-((real(t - 1) - 6.0)**2) / (2.0 * 1.8**2))
        call random_number(random_value)

        score = 0.68 * previous_score + &
                0.20 * real(t - 1) + &
                1.00 * resources * early_weight - &
                1.15 * burden * early_weight + &
                0.95 * support + &
                0.85 * support * transition_weight + &
                2.2 * (random_value - 0.5)

        trajectory(t) = trajectory(t) + score
        previous_score = score
     end do
  end do

  open(unit=10, file="outputs/fortran_life_course_inequality.csv", status="replace")
  write(10, '(A)') "time,average_development"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4)') t - 1, ",", trajectory(t) / real(n_people)
  end do
  close(10)

  print *, "Wrote outputs/fortran_life_course_inequality.csv"
end program life_course_inequality_simulation
