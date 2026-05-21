program nature_nurture_simulation
  implicit none

  integer, parameter :: n_children = 900
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: random_value
  real :: biological_sensitivity, baseline_functioning, structural_risk, chronic_adversity
  real :: family_support_context, institutional_support, disability_support, resource_stability
  real :: previous_score, caregiver_support, acute_stress, intervention
  real :: protective_context, development_score
  real :: development_trajectory(n_periods)
  real :: protective_trajectory(n_periods)
  real :: support_trajectory(n_periods)
  real :: stress_trajectory(n_periods)
  real :: risk_trajectory(n_periods)
  real :: sensitivity_trajectory(n_periods)

  call random_seed()
  development_trajectory = 0.0
  protective_trajectory = 0.0
  support_trajectory = 0.0
  stress_trajectory = 0.0
  risk_trajectory = 0.0
  sensitivity_trajectory = 0.0

  do i = 1, n_children
     call random_number(random_value)
     biological_sensitivity = 2.0 * random_value - 1.0
     call random_number(random_value)
     baseline_functioning = 43.0 + 14.0 * random_value
     call random_number(random_value)
     structural_risk = merge(1.0, 0.0, random_value < 0.35)
     call random_number(random_value)
     chronic_adversity = merge(1.0, 0.0, random_value < 0.32)
     call random_number(random_value)
     family_support_context = 2.0 * random_value - 1.0
     call random_number(random_value)
     institutional_support = 1.4 * random_value - 0.7
     call random_number(random_value)
     disability_support = 1.2 * random_value - 0.6
     call random_number(random_value)
     resource_stability = 1.0 * random_value - 0.5
     previous_score = baseline_functioning

     do t = 1, n_periods
        call random_number(random_value)
        caregiver_support = 0.4 + family_support_context - 0.5 * structural_risk + 0.9 * (random_value - 0.5)
        call random_number(random_value)
        acute_stress = 0.3 * structural_risk + 0.35 * chronic_adversity + 0.8 * (random_value - 0.5)
        call random_number(random_value)
        intervention = merge(1.0, 0.0, (t - 1) >= 5 .and. random_value < 0.28)

        protective_context = caregiver_support + institutional_support + disability_support + resource_stability + intervention

        development_score = 0.70 * previous_score + &
             0.90 * real(t - 1) + &
             1.20 * caregiver_support - &
             1.40 * acute_stress - &
             2.20 * structural_risk - &
             1.80 * chronic_adversity + &
             0.95 * institutional_support + &
             0.85 * disability_support + &
             0.70 * resource_stability + &
             1.60 * intervention + &
             1.00 * biological_sensitivity * caregiver_support - &
             0.90 * biological_sensitivity * acute_stress + &
             0.65 * biological_sensitivity * protective_context

        development_trajectory(t) = development_trajectory(t) + development_score
        protective_trajectory(t) = protective_trajectory(t) + protective_context
        support_trajectory(t) = support_trajectory(t) + caregiver_support
        stress_trajectory(t) = stress_trajectory(t) + acute_stress
        risk_trajectory(t) = risk_trajectory(t) + structural_risk
        sensitivity_trajectory(t) = sensitivity_trajectory(t) + biological_sensitivity
        previous_score = development_score
     end do
  end do

  open(unit=10, file="outputs/fortran_nature_nurture.csv", status="replace")
  write(10, '(A)') "time,average_development_score,average_protective_context,average_caregiver_support,average_acute_stress,average_structural_risk,average_biological_sensitivity"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4,A,F10.4,A,F10.4,A,F10.4,A,F10.4)') t - 1, ",", development_trajectory(t) / real(n_children), ",", protective_trajectory(t) / real(n_children), ",", support_trajectory(t) / real(n_children), ",", stress_trajectory(t) / real(n_children), ",", risk_trajectory(t) / real(n_children), ",", sensitivity_trajectory(t) / real(n_children)
  end do
  close(10)

  print *, "Wrote outputs/fortran_nature_nurture.csv"
end program nature_nurture_simulation
