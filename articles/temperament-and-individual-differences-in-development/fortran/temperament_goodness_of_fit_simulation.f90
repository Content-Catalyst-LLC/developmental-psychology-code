program temperament_goodness_of_fit_simulation
  implicit none

  integer, parameter :: n_children = 900
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: reactivity, inhibition, activity, baseline_adjustment
  real :: family_support, school_fit, chronic_stress, classroom_structure
  real :: teacher, movement, previous_adjustment, support, current_school_fit
  real :: stress, accommodation, goodness_of_fit, adjustment, random_value
  real :: adjustment_trajectory(n_periods)
  real :: fit_trajectory(n_periods)
  real :: support_trajectory(n_periods)
  real :: stress_trajectory(n_periods)

  call random_seed()
  adjustment_trajectory = 0.0
  fit_trajectory = 0.0
  support_trajectory = 0.0
  stress_trajectory = 0.0

  do i = 1, n_children
     call random_number(random_value)
     reactivity = 2.0 * random_value - 1.0
     call random_number(random_value)
     inhibition = 2.0 * random_value - 1.0
     call random_number(random_value)
     activity = 2.0 * random_value - 1.0
     call random_number(random_value)
     baseline_adjustment = 42.0 + 16.0 * random_value
     call random_number(random_value)
     family_support = 2.0 * random_value - 1.0
     call random_number(random_value)
     school_fit = 2.0 * random_value - 1.0
     call random_number(random_value)
     chronic_stress = merge(1.0, 0.0, random_value < 0.30)
     call random_number(random_value)
     classroom_structure = 1.2 * random_value - 0.6
     call random_number(random_value)
     teacher = 1.2 * random_value - 0.6
     call random_number(random_value)
     movement = 1.0 * random_value - 0.5
     previous_adjustment = baseline_adjustment

     do t = 1, n_periods
        call random_number(random_value)
        support = family_support + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        current_school_fit = school_fit + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        stress = 0.3 * chronic_stress + 0.80 * (random_value - 0.5)
        call random_number(random_value)
        accommodation = 0.40 + 0.50 * (random_value - 0.5)

        goodness_of_fit = current_school_fit + teacher + movement - abs(reactivity - classroom_structure) + accommodation

        adjustment = 0.70 * previous_adjustment + &
                0.90 * real(t - 1) + &
                1.30 * support + &
                1.20 * goodness_of_fit + &
                0.50 * teacher - &
                1.50 * stress - &
                1.10 * chronic_stress - &
                0.25 * inhibition - &
                0.20 * activity + &
                0.95 * reactivity * support + &
                0.85 * reactivity * goodness_of_fit - &
                0.90 * reactivity * stress

        adjustment_trajectory(t) = adjustment_trajectory(t) + adjustment
        fit_trajectory(t) = fit_trajectory(t) + goodness_of_fit
        support_trajectory(t) = support_trajectory(t) + support
        stress_trajectory(t) = stress_trajectory(t) + stress
        previous_adjustment = adjustment
     end do
  end do

  open(unit=10, file="outputs/fortran_temperament_goodness_of_fit.csv", status="replace")
  write(10, '(A)') "time,average_adjustment,average_goodness_of_fit,average_support,average_stress"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4,A,F10.4,A,F10.4)') t - 1, ",", adjustment_trajectory(t) / real(n_children), ",", fit_trajectory(t) / real(n_children), ",", support_trajectory(t) / real(n_children), ",", stress_trajectory(t) / real(n_children)
  end do
  close(10)

  print *, "Wrote outputs/fortran_temperament_goodness_of_fit.csv"
end program temperament_goodness_of_fit_simulation
