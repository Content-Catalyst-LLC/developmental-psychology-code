program wisdom_meaning_simulation
  implicit none

  integer, parameter :: n_older_adults = 900
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: baseline_meaning, connection_base, reflection_base, health_base
  real :: support_base, legacy_base, dignity, services, community
  real :: previous_meaning, connection, reflection, health, support, legacy
  real :: wisdom, meaning, random_value
  real :: meaning_trajectory(n_periods)
  real :: wisdom_trajectory(n_periods)
  real :: connection_trajectory(n_periods)
  real :: health_trajectory(n_periods)

  call random_seed()
  meaning_trajectory = 0.0
  wisdom_trajectory = 0.0
  connection_trajectory = 0.0
  health_trajectory = 0.0

  do i = 1, n_older_adults
     call random_number(random_value)
     baseline_meaning = 42.0 + 16.0 * random_value
     call random_number(random_value)
     connection_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     reflection_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     health_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     support_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     legacy_base = 1.6 * random_value - 0.8
     call random_number(random_value)
     dignity = 1.2 * random_value - 0.6
     call random_number(random_value)
     services = 1.0 * random_value - 0.5
     call random_number(random_value)
     community = 1.0 * random_value - 0.5
     previous_meaning = baseline_meaning

     do t = 1, n_periods
        call random_number(random_value)
        connection = connection_base + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        reflection = reflection_base + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        health = health_base + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        support = support_base + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        legacy = legacy_base + 0.55 * (random_value - 0.5)

        wisdom = 0.35 * reflection + 0.25 * connection + 0.20 * legacy + 0.20 * dignity - 0.20 * health

        meaning = 0.70 * previous_meaning + &
                0.35 * real(t - 1) + &
                1.10 * connection + &
                1.05 * reflection + &
                0.90 * support + &
                0.75 * legacy + &
                0.75 * dignity + &
                0.60 * services + &
                0.55 * community - &
                1.15 * health + &
                0.85 * wisdom

        meaning_trajectory(t) = meaning_trajectory(t) + meaning
        wisdom_trajectory(t) = wisdom_trajectory(t) + wisdom
        connection_trajectory(t) = connection_trajectory(t) + connection
        health_trajectory(t) = health_trajectory(t) + health
        previous_meaning = meaning
     end do
  end do

  open(unit=10, file="outputs/fortran_wisdom_meaning.csv", status="replace")
  write(10, '(A)') "time,average_meaning,average_wisdom,average_connection,average_health"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4,A,F10.4,A,F10.4)') t - 1, ",", meaning_trajectory(t) / real(n_older_adults), ",", wisdom_trajectory(t) / real(n_older_adults), ",", connection_trajectory(t) / real(n_older_adults), ",", health_trajectory(t) / real(n_older_adults)
  end do
  close(10)

  print *, "Wrote outputs/fortran_wisdom_meaning.csv"
end program wisdom_meaning_simulation
