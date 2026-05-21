program stage_like_development_simulation
  implicit none

  integer, parameter :: n_children = 950
  integer, parameter :: n_periods = 10
  integer :: i, t, threshold_time
  real :: random_value
  real :: baseline, growth_rate, support_context, chronic_stress
  real :: stage_pattern, school_support, resource_stability, previous_score
  real :: current_support, threshold_on, smooth_transition, readiness, score
  real :: score_trajectory(n_periods)
  real :: readiness_trajectory(n_periods)
  real :: support_trajectory(n_periods)
  real :: stress_trajectory(n_periods)
  real :: logistic_trajectory(n_periods)

  call random_seed()
  score_trajectory = 0.0
  readiness_trajectory = 0.0
  support_trajectory = 0.0
  stress_trajectory = 0.0
  logistic_trajectory = 0.0

  do i = 1, n_children
     call random_number(random_value)
     baseline = 39.0 + 14.0 * random_value
     call random_number(random_value)
     growth_rate = 1.20 + 1.00 * random_value
     call random_number(random_value)
     support_context = 2.0 * random_value - 1.0
     call random_number(random_value)
     chronic_stress = merge(1.0, 0.0, random_value < 0.32)
     call random_number(random_value)
     threshold_time = 4 + int(4.0 * random_value)
     call random_number(random_value)
     stage_pattern = merge(1.0, 0.0, random_value < 0.50)
     call random_number(random_value)
     school_support = 1.2 * random_value - 0.6
     call random_number(random_value)
     resource_stability = 1.0 * random_value - 0.5
     previous_score = baseline

     do t = 1, n_periods
        call random_number(random_value)
        current_support = support_context + 0.70 * (random_value - 0.5)
        threshold_on = merge(1.0, 0.0, (t - 1) >= threshold_time)
        smooth_transition = 1.0 / (1.0 + exp(-1.35 * (real(t - 1) - real(threshold_time))))
        readiness = current_support + school_support + resource_stability - 0.75 * chronic_stress

        score = 0.58 * previous_score + &
             0.42 * (baseline + growth_rate * real(t - 1)) + &
             1.15 * current_support + &
             0.90 * school_support + &
             0.70 * resource_stability - &
             2.00 * chronic_stress + &
             3.00 * threshold_on * stage_pattern + &
             2.20 * smooth_transition * stage_pattern + &
             0.75 * threshold_on * stage_pattern * readiness

        score_trajectory(t) = score_trajectory(t) + score
        readiness_trajectory(t) = readiness_trajectory(t) + readiness
        support_trajectory(t) = support_trajectory(t) + current_support
        stress_trajectory(t) = stress_trajectory(t) + chronic_stress
        logistic_trajectory(t) = logistic_trajectory(t) + smooth_transition
        previous_score = score
     end do
  end do

  open(unit=10, file="outputs/fortran_stage_like_development.csv", status="replace")
  write(10, '(A)') "time,average_development_score,average_transition_readiness,average_support,average_stress,average_logistic_transition"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4,A,F10.4,A,F10.4,A,F10.4)') t - 1, ",", score_trajectory(t) / real(n_children), ",", readiness_trajectory(t) / real(n_children), ",", support_trajectory(t) / real(n_children), ",", stress_trajectory(t) / real(n_children), ",", logistic_trajectory(t) / real(n_children)
  end do
  close(10)

  print *, "Wrote outputs/fortran_stage_like_development.csv"
end program stage_like_development_simulation
