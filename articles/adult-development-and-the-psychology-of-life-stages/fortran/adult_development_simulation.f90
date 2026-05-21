program adult_development_simulation
  implicit none

  integer, parameter :: n_adults = 950
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: baseline_adjustment, support_base, work_base, health_base
  real :: resources_base, burden_base, institutional, community
  real :: previous_adjustment, support, work, health, resources, burden
  real :: adjustment, random_value
  real :: adjustment_trajectory(n_periods)
  real :: support_trajectory(n_periods)
  real :: work_trajectory(n_periods)
  real :: health_trajectory(n_periods)
  real :: burden_trajectory(n_periods)

  call random_seed()
  adjustment_trajectory = 0.0
  support_trajectory = 0.0
  work_trajectory = 0.0
  health_trajectory = 0.0
  burden_trajectory = 0.0

  do i = 1, n_adults
     call random_number(random_value)
     baseline_adjustment = 42.0 + 16.0 * random_value
     call random_number(random_value)
     support_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     work_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     health_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     resources_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     burden_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     institutional = 1.2 * random_value - 0.6
     call random_number(random_value)
     community = 1.0 * random_value - 0.5
     previous_adjustment = baseline_adjustment

     do t = 1, n_periods
        call random_number(random_value)
        support = support_base + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        work = work_base + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        health = health_base + 0.03 * real(t - 1) + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        resources = resources_base + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        burden = burden_base + 0.70 * (random_value - 0.5)

        adjustment = 0.70 * previous_adjustment + &
                0.55 * real(t - 1) + &
                1.15 * support + &
                1.05 * work + &
                0.95 * resources + &
                0.70 * institutional + &
                0.55 * community - &
                1.20 * health - &
                0.80 * burden + &
                0.25 * support * resources

        adjustment_trajectory(t) = adjustment_trajectory(t) + adjustment
        support_trajectory(t) = support_trajectory(t) + support
        work_trajectory(t) = work_trajectory(t) + work
        health_trajectory(t) = health_trajectory(t) + health
        burden_trajectory(t) = burden_trajectory(t) + burden
        previous_adjustment = adjustment
     end do
  end do

  open(unit=10, file="outputs/fortran_adult_development.csv", status="replace")
  write(10, '(A)') "time,average_adjustment,average_support,average_work,average_health,average_role_burden"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4,A,F10.4,A,F10.4,A,F10.4)') t - 1, ",", adjustment_trajectory(t) / real(n_adults), ",", support_trajectory(t) / real(n_adults), ",", work_trajectory(t) / real(n_adults), ",", health_trajectory(t) / real(n_adults), ",", burden_trajectory(t) / real(n_adults)
  end do
  close(10)

  print *, "Wrote outputs/fortran_adult_development.csv"
end program adult_development_simulation
