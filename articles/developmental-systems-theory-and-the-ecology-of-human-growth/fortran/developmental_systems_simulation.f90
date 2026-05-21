program developmental_systems_simulation
  implicit none

  integer, parameter :: n_children = 850
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: bio, family, peer, school, curriculum, neighborhood, service, material
  real :: intervention, previous_development, development, support, stress
  real :: random_value
  real :: development_trajectory(n_periods)
  real :: support_trajectory(n_periods)
  real :: stress_trajectory(n_periods)

  call random_seed()
  development_trajectory = 0.0
  support_trajectory = 0.0
  stress_trajectory = 0.0

  do i = 1, n_children
     call random_number(random_value)
     bio = 2.0 * random_value - 1.0
     call random_number(random_value)
     family = 2.0 * random_value - 1.0
     call random_number(random_value)
     peer = 1.6 * random_value - 0.8
     call random_number(random_value)
     school = 1.2 * random_value - 0.6
     call random_number(random_value)
     curriculum = 1.0 * random_value - 0.5
     call random_number(random_value)
     neighborhood = 1.2 * random_value - 0.6
     call random_number(random_value)
     service = 1.0 * random_value - 0.5
     call random_number(random_value)
     material = 1.0 * random_value - 0.5
     call random_number(random_value)
     if (random_value < 0.35) then
        intervention = 1.0
     else
        intervention = 0.0
     end if
     call random_number(random_value)
     previous_development = 47.0 + 6.0 * random_value

     do t = 1, n_periods
        call random_number(random_value)

        support = family + peer + school + curriculum + neighborhood + service + material
        stress = -0.25 * family - 0.20 * school - 0.20 * neighborhood - 0.15 * material + 0.70 * (random_value - 0.5)

        development = 0.70 * previous_development + &
                0.24 * real(t - 1) + &
                0.85 * bio + &
                1.15 * family + &
                0.95 * peer + &
                0.95 * school + &
                0.80 * curriculum + &
                0.85 * neighborhood + &
                0.70 * service + &
                0.65 * material + &
                0.90 * intervention - &
                1.10 * stress + &
                0.45 * bio * family - &
                0.35 * bio * stress + &
                2.3 * (random_value - 0.5)

        development_trajectory(t) = development_trajectory(t) + development
        support_trajectory(t) = support_trajectory(t) + support
        stress_trajectory(t) = stress_trajectory(t) + stress
        previous_development = development
     end do
  end do

  open(unit=10, file="outputs/fortran_developmental_systems.csv", status="replace")
  write(10, '(A)') "time,average_development,average_ecological_support,average_ecological_stress"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4,A,F10.4)') t - 1, ",", development_trajectory(t) / real(n_children), ",", support_trajectory(t) / real(n_children), ",", stress_trajectory(t) / real(n_children)
  end do
  close(10)

  print *, "Wrote outputs/fortran_developmental_systems.csv"
end program developmental_systems_simulation
