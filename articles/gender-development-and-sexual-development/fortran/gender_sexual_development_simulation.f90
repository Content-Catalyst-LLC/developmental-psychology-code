program gender_sexual_development_simulation
  implicit none

  integer, parameter :: n_adolescents = 900
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: random_value
  real :: baseline_adjustment, family_support, social_recognition, consent_knowledge
  real :: school_connectedness, chronic_stigma, school_climate, health_education_quality
  real :: anti_harassment_support, previous_adjustment, pubertal_progress
  real :: current_family, current_recognition, current_consent, current_connectedness
  real :: current_stigma, protective_context, adjustment
  real :: adjustment_trajectory(n_periods)
  real :: protective_trajectory(n_periods)
  real :: stigma_trajectory(n_periods)
  real :: family_trajectory(n_periods)
  real :: consent_trajectory(n_periods)

  call random_seed()
  adjustment_trajectory = 0.0
  protective_trajectory = 0.0
  stigma_trajectory = 0.0
  family_trajectory = 0.0
  consent_trajectory = 0.0

  do i = 1, n_adolescents
     call random_number(random_value)
     baseline_adjustment = 42.0 + 16.0 * random_value
     call random_number(random_value)
     family_support = 2.0 * random_value - 1.0
     call random_number(random_value)
     social_recognition = 2.0 * random_value - 1.0
     call random_number(random_value)
     consent_knowledge = 2.0 * random_value - 1.0
     call random_number(random_value)
     school_connectedness = 2.0 * random_value - 1.0
     call random_number(random_value)
     chronic_stigma = merge(1.0, 0.0, random_value < 0.24)
     call random_number(random_value)
     school_climate = 1.2 * random_value - 0.6
     call random_number(random_value)
     health_education_quality = 1.2 * random_value - 0.6
     call random_number(random_value)
     anti_harassment_support = 1.0 * random_value - 0.5
     previous_adjustment = baseline_adjustment

     do t = 1, n_periods
        call random_number(random_value)
        pubertal_progress = real(t - 1) + 0.40 * (random_value - 0.5)
        call random_number(random_value)
        current_family = family_support + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        current_recognition = social_recognition + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        current_consent = consent_knowledge + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        current_connectedness = school_connectedness + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        current_stigma = 0.40 * chronic_stigma + 0.70 * (random_value - 0.5)

        protective_context = current_family + current_recognition + current_consent + &
             current_connectedness + school_climate + health_education_quality + anti_harassment_support

        adjustment = 0.70 * previous_adjustment + &
             0.75 * pubertal_progress + &
             1.15 * current_family + &
             1.05 * current_recognition + &
             1.00 * current_consent + &
             0.95 * current_connectedness + &
             0.70 * school_climate + &
             0.70 * health_education_quality + &
             0.65 * anti_harassment_support - &
             1.40 * current_stigma - &
             0.90 * chronic_stigma - &
             0.35 * current_stigma * protective_context

        adjustment_trajectory(t) = adjustment_trajectory(t) + adjustment
        protective_trajectory(t) = protective_trajectory(t) + protective_context
        stigma_trajectory(t) = stigma_trajectory(t) + current_stigma
        family_trajectory(t) = family_trajectory(t) + current_family
        consent_trajectory(t) = consent_trajectory(t) + current_consent
        previous_adjustment = adjustment
     end do
  end do

  open(unit=10, file="outputs/fortran_gender_sexual_development.csv", status="replace")
  write(10, '(A)') "time,average_adjustment,average_protective_context,average_stigma,average_family_support,average_consent_knowledge"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4,A,F10.4,A,F10.4,A,F10.4)') t - 1, ",", adjustment_trajectory(t) / real(n_adolescents), ",", protective_trajectory(t) / real(n_adolescents), ",", stigma_trajectory(t) / real(n_adolescents), ",", family_trajectory(t) / real(n_adolescents), ",", consent_trajectory(t) / real(n_adolescents)
  end do
  close(10)

  print *, "Wrote outputs/fortran_gender_sexual_development.csv"
end program gender_sexual_development_simulation
