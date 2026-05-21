program disability_neurodivergence_simulation
  implicit none

  integer, parameter :: n_children = 820
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: neuro_profile, support, access, barrier, communication
  real :: previous_development, development, participation
  real :: random_value
  real :: development_trajectory(n_periods)
  real :: participation_trajectory(n_periods)

  call random_seed()
  development_trajectory = 0.0
  participation_trajectory = 0.0

  do i = 1, n_children
     call random_number(random_value)
     neuro_profile = 2.0 * random_value - 1.0
     call random_number(random_value)
     support = 2.0 * random_value - 1.0
     call random_number(random_value)
     access = 2.0 * random_value - 1.0
     call random_number(random_value)
     barrier = 2.0 * random_value - 1.0
     call random_number(random_value)
     communication = 2.0 * random_value - 1.0
     call random_number(random_value)
     previous_development = 47.0 + 6.0 * random_value

     do t = 1, n_periods
        call random_number(random_value)

        participation = 45.0 + &
                0.50 * real(t - 1) + &
                1.15 * support + &
                1.10 * access + &
                0.95 * communication - &
                1.25 * barrier + &
                2.2 * (random_value - 0.5)

        development = 0.70 * previous_development + &
                0.20 * real(t - 1) + &
                0.45 * neuro_profile + &
                1.10 * support + &
                1.05 * access + &
                0.90 * communication + &
                0.80 * participation / 10.0 - &
                1.15 * barrier + &
                0.50 * support * access - &
                0.40 * barrier * abs(neuro_profile) + &
                2.3 * (random_value - 0.5)

        development_trajectory(t) = development_trajectory(t) + development
        participation_trajectory(t) = participation_trajectory(t) + participation
        previous_development = development
     end do
  end do

  open(unit=10, file="outputs/fortran_disability_neurodivergence.csv", status="replace")
  write(10, '(A)') "time,average_development,average_participation"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4)') t - 1, ",", development_trajectory(t) / real(n_children), ",", participation_trajectory(t) / real(n_children)
  end do
  close(10)

  print *, "Wrote outputs/fortran_disability_neurodivergence.csv"
end program disability_neurodivergence_simulation
