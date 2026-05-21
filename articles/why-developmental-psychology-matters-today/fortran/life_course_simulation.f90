program life_course_simulation
  implicit none

  integer, parameter :: n_people = 1000
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: score, previous_score, support, risk, policy, random_value
  real :: trajectory(n_periods)

  call random_seed()
  trajectory = 0.0

  do i = 1, n_people
     call random_number(random_value)
     previous_score = 47.0 + 6.0 * random_value

     call random_number(support)
     call random_number(risk)
     call random_number(policy)

     support = 2.0 * support - 1.0
     risk = 2.0 * risk - 1.0
     policy = 2.0 * policy - 1.0

     do t = 1, n_periods
        call random_number(random_value)

        score = 0.68 * previous_score + &
                0.22 * real(t - 1) + &
                1.10 * support - &
                1.15 * risk + &
                0.90 * policy + &
                2.0 * (random_value - 0.5)

        trajectory(t) = trajectory(t) + score
        previous_score = score
     end do
  end do

  open(unit=10, file="outputs/fortran_average_trajectory.csv", status="replace")
  write(10, '(A)') "time,average_development"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4)') t - 1, ",", trajectory(t) / real(n_people)
  end do
  close(10)

  print *, "Wrote outputs/fortran_average_trajectory.csv"
end program life_course_simulation
