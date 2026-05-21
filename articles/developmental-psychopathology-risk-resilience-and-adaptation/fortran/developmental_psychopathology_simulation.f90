program developmental_psychopathology_simulation
  implicit none

  integer, parameter :: n_children = 850
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: risk, support, stability, regulation, sensitivity
  real :: previous_adaptation, adaptation, cumulative_risk
  real :: timing_weight, transition_weight, random_value
  real :: trajectory(n_periods)

  call random_seed()
  trajectory = 0.0

  do i = 1, n_children
     call random_number(random_value)
     risk = 2.0 * random_value - 1.0
     call random_number(random_value)
     support = 2.0 * random_value - 1.0
     call random_number(random_value)
     stability = 2.0 * random_value - 1.0
     call random_number(random_value)
     regulation = 2.0 * random_value - 1.0
     call random_number(random_value)
     sensitivity = 2.0 * random_value - 1.0
     call random_number(random_value)
     previous_adaptation = 47.0 + 6.0 * random_value

     cumulative_risk = 0.0

     do t = 1, n_periods
        timing_weight = exp(-0.16 * real(t - 1))
        transition_weight = exp(-((real(t - 1) - 6.0)**2) / (2.0 * 1.8**2))
        cumulative_risk = cumulative_risk + risk * timing_weight
        call random_number(random_value)

        adaptation = 0.70 * previous_adaptation + &
                0.20 * real(t - 1) + &
                0.75 * regulation + &
                1.10 * support + &
                1.00 * stability + &
                0.70 * support * transition_weight - &
                0.85 * cumulative_risk - &
                1.10 * risk * timing_weight + &
                0.60 * sensitivity * support + &
                0.75 * support * stability + &
                2.3 * (random_value - 0.5)

        trajectory(t) = trajectory(t) + adaptation
        previous_adaptation = adaptation
     end do
  end do

  open(unit=10, file="outputs/fortran_developmental_psychopathology.csv", status="replace")
  write(10, '(A)') "time,average_adaptation"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4)') t - 1, ",", trajectory(t) / real(n_children)
  end do
  close(10)

  print *, "Wrote outputs/fortran_developmental_psychopathology.csv"
end program developmental_psychopathology_simulation
