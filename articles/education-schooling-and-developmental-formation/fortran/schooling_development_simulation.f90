program schooling_development_simulation
  implicit none

  integer, parameter :: n_students = 850
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: teacher, peer, stress, climate, curriculum, resources, intervention
  real :: previous_development, development, connectedness
  real :: random_value
  real :: development_trajectory(n_periods)
  real :: connectedness_trajectory(n_periods)

  call random_seed()
  development_trajectory = 0.0
  connectedness_trajectory = 0.0

  do i = 1, n_students
     call random_number(random_value)
     teacher = 2.0 * random_value - 1.0
     call random_number(random_value)
     peer = 2.0 * random_value - 1.0
     call random_number(random_value)
     stress = 2.0 * random_value - 1.0
     call random_number(random_value)
     climate = 1.2 * random_value - 0.6
     call random_number(random_value)
     curriculum = 1.2 * random_value - 0.6
     call random_number(random_value)
     resources = 1.0 * random_value - 0.5
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

        connectedness = 45.0 + &
                0.45 * real(t - 1) + &
                1.20 * teacher + &
                1.05 * peer + &
                0.80 * climate - &
                1.10 * stress + &
                2.2 * (random_value - 0.5)

        development = 0.70 * previous_development + &
                0.22 * real(t - 1) + &
                1.10 * teacher + &
                1.00 * peer + &
                0.95 * climate + &
                0.90 * curriculum + &
                0.65 * resources + &
                0.85 * intervention + &
                0.55 * connectedness / 10.0 - &
                1.05 * stress + &
                0.50 * teacher * peer + &
                2.3 * (random_value - 0.5)

        development_trajectory(t) = development_trajectory(t) + development
        connectedness_trajectory(t) = connectedness_trajectory(t) + connectedness
        previous_development = development
     end do
  end do

  open(unit=10, file="outputs/fortran_schooling_development.csv", status="replace")
  write(10, '(A)') "time,average_development,average_connectedness"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4)') t - 1, ",", development_trajectory(t) / real(n_students), ",", connectedness_trajectory(t) / real(n_students)
  end do
  close(10)

  print *, "Wrote outputs/fortran_schooling_development.csv"
end program schooling_development_simulation
