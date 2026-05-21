program continuity_discontinuity_simulation
  implicit none

  integer, parameter :: n_people = 950
  integer, parameter :: n_periods = 10
  integer :: i, t, threshold_time
  real :: random_value
  real :: baseline, growth_rate, curvature, support_context, chronic_stress
  real :: institutional_rupture, intervention_exposure, threshold_sensitive
  real :: school_support, resource_stability, previous_score, current_support
  real :: threshold_on, smooth_transition, readiness, continuous_component, score
  real :: score_trajectory(n_periods)
  real :: readiness_trajectory(n_periods)
  real :: support_trajectory(n_periods)
  real :: stress_trajectory(n_periods)
  real :: rupture_trajectory(n_periods)
  real :: intervention_trajectory(n_periods)

  call random_seed()
  score_trajectory = 0.0
  readiness_trajectory = 0.0
  support_trajectory = 0.0
  stress_trajectory = 0.0
  rupture_trajectory = 0.0
  intervention_trajectory = 0.0

  do i = 1, n_people
     call random_number(random_value)
     baseline = 38.0 + 14.0 * random_value
     call random_number(random_value)
     growth_rate = 1.30 + 1.00 * random_value
     call random_number(random_value)
     curvature = -0.02 + 0.10 * random_value
     call random_number(random_value)
     support_context = 2.0 * random_value - 1.0
     call random_number(random_value)
     chronic_stress = merge(1.0, 0.0, random_value < 0.30)
     call random_number(random_value)
     institutional_rupture = merge(1.0, 0.0, random_value < 0.18)
     call random_number(random_value)
     intervention_exposure = merge(1.0, 0.0, random_value < 0.35)
     call random_number(random_value)
     threshold_time = 4 + int(4.0 * random_value)
     call random_number(random_value)
     threshold_sensitive = merge(1.0, 0.0, random_value < 0.45)
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
        readiness = current_support + school_support + resource_stability + &
             0.85 * intervention_exposure - 0.75 * chronic_stress - 0.80 * institutional_rupture

        continuous_component = baseline + growth_rate * real(t - 1) + curvature * real((t - 1) * (t - 1))

        score = 0.58 * previous_score + &
             0.42 * continuous_component + &
             1.25 * current_support + &
             0.90 * school_support + &
             0.70 * resource_stability + &
             1.30 * intervention_exposure - &
             2.00 * chronic_stress - &
             2.40 * institutional_rupture + &
             3.10 * threshold_on * threshold_sensitive + &
             2.10 * smooth_transition * threshold_sensitive + &
             0.75 * threshold_on * threshold_sensitive * readiness

        score_trajectory(t) = score_trajectory(t) + score
        readiness_trajectory(t) = readiness_trajectory(t) + readiness
        support_trajectory(t) = support_trajectory(t) + current_support
        stress_trajectory(t) = stress_trajectory(t) + chronic_stress
        rupture_trajectory(t) = rupture_trajectory(t) + institutional_rupture
        intervention_trajectory(t) = intervention_trajectory(t) + intervention_exposure
        previous_score = score
     end do
  end do

  open(unit=10, file="outputs/fortran_continuity_discontinuity.csv", status="replace")
  write(10, '(A)') "time,average_development_score,average_transition_readiness,average_support,average_stress,average_rupture,average_intervention"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4,A,F10.4,A,F10.4,A,F10.4,A,F10.4)') t - 1, ",", score_trajectory(t) / real(n_people), ",", readiness_trajectory(t) / real(n_people), ",", support_trajectory(t) / real(n_people), ",", stress_trajectory(t) / real(n_people), ",", rupture_trajectory(t) / real(n_people), ",", intervention_trajectory(t) / real(n_people)
  end do
  close(10)

  print *, "Wrote outputs/fortran_continuity_discontinuity.csv"
end program continuity_discontinuity_simulation
