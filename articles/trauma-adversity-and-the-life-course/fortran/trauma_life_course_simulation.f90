program trauma_life_course_simulation
  implicit none

  integer, parameter :: n_children = 850
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: adversity, support, stability, previous_score, score
  real :: early_weight, transition_weight, cumulative_adversity, random_value
  real :: trajectory(n_periods)

  call random_seed()
  trajectory = 0.0

  do i = 1, n_children
     call random_number(random_value)
     adversity = 2.0 * random_value - 1.0

     call random_number(random_value)
     support = 2.0 * random_value - 1.0

     call random_number(random_value)
     stability = 2.0 * random_value - 1.0

     call random_number(random_value)
     previous_score = 47.0 + 6.0 * random_value

     cumulative_adversity = 0.0

     do t = 1, n_periods
        early_weight = exp(-0.18 * real(t - 1))
        transition_weight = exp(-((real(t - 1) - 6.0)**2) / (2.0 * 1.8**2))
        cumulative_adversity = cumulative_adversity + adversity * early_weight

        call random_number(random_value)

        score = 0.70 * previous_score + &
                0.18 * real(t - 1) - &
                0.70 * cumulative_adversity - &
                1.05 * adversity * early_weight + &
                1.05 * support + &
                0.95 * stability + &
                0.70 * support * transition_weight + &
                0.75 * support * stability + &
                2.3 * (random_value - 0.5)

        trajectory(t) = trajectory(t) + score
        previous_score = score
     end do
  end do

  open(unit=10, file="outputs/fortran_trauma_life_course.csv", status="replace")
  write(10, '(A)') "time,average_adaptation"

  do t = 1, n_periods
     write(10, '(I0,A,F10.4)') t - 1, ",", trajectory(t) / real(n_children)
  end do

  close(10)

  print *, "Wrote outputs/fortran_trauma_life_course.csv"
end program trauma_life_course_simulation
