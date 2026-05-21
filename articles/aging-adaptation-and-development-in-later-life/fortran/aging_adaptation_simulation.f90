program aging_adaptation_simulation
  implicit none

  integer, parameter :: n_older_adults = 900
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: baseline_adjustment, function_base, support_base, health_base
  real :: adaptation_base, meaning_base, accessibility, dignity, services
  real :: previous_adjustment, current_function, current_support, current_health
  real :: current_adaptation, current_meaning, functional_fit, adjustment, random_value
  real :: adjustment_trajectory(n_periods)
  real :: fit_trajectory(n_periods)
  real :: support_trajectory(n_periods)
  real :: health_trajectory(n_periods)

  call random_seed()
  adjustment_trajectory = 0.0
  fit_trajectory = 0.0
  support_trajectory = 0.0
  health_trajectory = 0.0

  do i = 1, n_older_adults
     call random_number(random_value)
     baseline_adjustment = 42.0 + 16.0 * random_value
     call random_number(random_value)
     function_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     support_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     health_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     adaptation_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     meaning_base = 1.6 * random_value - 0.8
     call random_number(random_value)
     accessibility = 1.2 * random_value - 0.6
     call random_number(random_value)
     dignity = 1.2 * random_value - 0.6
     call random_number(random_value)
     services = 1.0 * random_value - 0.5
     previous_adjustment = baseline_adjustment

     do t = 1, n_periods
        call random_number(random_value)
        current_function = function_base - 0.04 * real(t - 1) + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        current_support = support_base + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        current_health = health_base + 0.05 * real(t - 1) + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        current_adaptation = adaptation_base + 0.03 * real(t - 1) + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        current_meaning = meaning_base + 0.55 * (random_value - 0.5)

        functional_fit = current_function + accessibility + 0.35 * current_function * accessibility

        adjustment = 0.70 * previous_adjustment + &
                0.35 * real(t - 1) + &
                1.15 * functional_fit + &
                1.05 * current_support + &
                0.95 * current_adaptation + &
                0.80 * current_meaning + &
                0.75 * dignity + &
                0.60 * services - &
                1.30 * current_health

        adjustment_trajectory(t) = adjustment_trajectory(t) + adjustment
        fit_trajectory(t) = fit_trajectory(t) + functional_fit
        support_trajectory(t) = support_trajectory(t) + current_support
        health_trajectory(t) = health_trajectory(t) + current_health
        previous_adjustment = adjustment
     end do
  end do

  open(unit=10, file="outputs/fortran_aging_adaptation.csv", status="replace")
  write(10, '(A)') "time,average_adjustment,average_functional_fit,average_support,average_health"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4,A,F10.4,A,F10.4)') t - 1, ",", adjustment_trajectory(t) / real(n_older_adults), ",", fit_trajectory(t) / real(n_older_adults), ",", support_trajectory(t) / real(n_older_adults), ",", health_trajectory(t) / real(n_older_adults)
  end do
  close(10)

  print *, "Wrote outputs/fortran_aging_adaptation.csv"
end program aging_adaptation_simulation
