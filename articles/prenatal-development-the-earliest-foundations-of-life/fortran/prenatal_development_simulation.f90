program prenatal_development_simulation
  implicit none

  integer, parameter :: n_cases = 1500
  integer :: i
  real :: random_value
  real :: gestational_weeks, maternal_health, prenatal_care, chronic_stress
  real :: toxic_exposure, nutrition_support, social_support
  real :: healthcare_access, environmental_burden, economic_security
  real :: effective_care, developmental_risk, early_outcome
  real :: outcome_sum, care_sum, risk_sum, gestation_sum, health_sum

  call random_seed()

  outcome_sum = 0.0
  care_sum = 0.0
  risk_sum = 0.0
  gestation_sum = 0.0
  health_sum = 0.0

  do i = 1, n_cases
     call random_number(random_value)
     gestational_weeks = 36.0 + 6.0 * random_value
     call random_number(random_value)
     maternal_health = 2.0 * random_value - 1.0
     call random_number(random_value)
     prenatal_care = 2.0 * random_value - 1.0
     call random_number(random_value)
     chronic_stress = 2.0 * random_value - 1.0
     call random_number(random_value)
     toxic_exposure = 2.0 * random_value - 1.0
     call random_number(random_value)
     nutrition_support = 2.0 * random_value - 1.0
     call random_number(random_value)
     social_support = 2.0 * random_value - 1.0
     call random_number(random_value)
     healthcare_access = 1.2 * random_value - 0.6
     call random_number(random_value)
     environmental_burden = 1.2 * random_value - 0.6
     call random_number(random_value)
     economic_security = 1.0 * random_value - 0.5

     effective_care = prenatal_care + healthcare_access + 0.30 * social_support
     developmental_risk = chronic_stress + toxic_exposure + environmental_burden - 0.40 * economic_security

     early_outcome = 10.0 + &
          0.85 * gestational_weeks + &
          1.60 * maternal_health + &
          1.35 * effective_care + &
          1.10 * nutrition_support + &
          0.85 * social_support - &
          1.55 * chronic_stress - &
          1.45 * toxic_exposure - &
          1.10 * environmental_burden + &
          0.70 * maternal_health * effective_care - &
          0.60 * maternal_health * chronic_stress - &
          0.55 * developmental_risk * effective_care

     outcome_sum = outcome_sum + early_outcome
     care_sum = care_sum + effective_care
     risk_sum = risk_sum + developmental_risk
     gestation_sum = gestation_sum + gestational_weeks
     health_sum = health_sum + maternal_health
  end do

  open(unit=10, file="outputs/fortran_prenatal_development.csv", status="replace")
  write(10, '(A)') "measure,value"
  write(10, '(A,F10.4)') "average_early_outcome,", outcome_sum / real(n_cases)
  write(10, '(A,F10.4)') "average_effective_care,", care_sum / real(n_cases)
  write(10, '(A,F10.4)') "average_developmental_risk,", risk_sum / real(n_cases)
  write(10, '(A,F10.4)') "average_gestational_weeks,", gestation_sum / real(n_cases)
  write(10, '(A,F10.4)') "average_maternal_health,", health_sum / real(n_cases)
  close(10)

  print *, "Wrote outputs/fortran_prenatal_development.csv"
end program prenatal_development_simulation
