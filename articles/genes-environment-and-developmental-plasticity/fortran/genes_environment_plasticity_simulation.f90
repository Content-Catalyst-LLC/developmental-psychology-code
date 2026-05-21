program genes_environment_plasticity_simulation
  implicit none

  integer, parameter :: n_children = 900
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: bio, care, stress, nutrition, school, safety, services
  real :: early, intervention, previous_development, development
  real :: timing_weight, stress_accum, support_accum, embedded_stress, embedded_support
  real :: random_value
  real :: development_trajectory(n_periods)
  real :: embedded_stress_trajectory(n_periods)
  real :: embedded_support_trajectory(n_periods)

  call random_seed()
  development_trajectory = 0.0
  embedded_stress_trajectory = 0.0
  embedded_support_trajectory = 0.0

  do i = 1, n_children
     call random_number(random_value)
     bio = 2.0 * random_value - 1.0
     call random_number(random_value)
     care = 2.0 * random_value - 1.0
     call random_number(random_value)
     stress = 2.0 * random_value - 1.0
     call random_number(random_value)
     nutrition = 1.6 * random_value - 0.8
     call random_number(random_value)
     school = 1.2 * random_value - 0.6
     call random_number(random_value)
     safety = 1.2 * random_value - 0.6
     call random_number(random_value)
     services = 1.0 * random_value - 0.5
     call random_number(random_value)
     if (random_value < 0.40) then
        early = 1.0
     else
        early = 0.0
     end if
     call random_number(random_value)
     if (random_value < 0.35) then
        intervention = 1.0
     else
        intervention = 0.0
     end if
     call random_number(random_value)
     previous_development = 47.0 + 6.0 * random_value
     stress_accum = 0.0
     support_accum = 0.0

     do t = 1, n_periods
        call random_number(random_value)
        timing_weight = exp(-0.30 * real(t - 1))
        stress_accum = stress_accum + stress * timing_weight
        support_accum = support_accum + (care + nutrition + school) * timing_weight
        embedded_stress = stress_accum / real(t)
        embedded_support = support_accum / real(t)

        development = 0.70 * previous_development + &
                0.22 * real(t - 1) + &
                0.90 * bio + &
                1.10 * care - &
                1.05 * stress + &
                0.80 * nutrition + &
                0.75 * school + &
                0.65 * safety + &
                0.60 * services + &
                0.85 * early * timing_weight + &
                0.85 * intervention + &
                0.95 * bio * care - &
                0.90 * bio * stress - &
                0.70 * embedded_stress + &
                0.60 * embedded_support + &
                2.3 * (random_value - 0.5)

        development_trajectory(t) = development_trajectory(t) + development
        embedded_stress_trajectory(t) = embedded_stress_trajectory(t) + embedded_stress
        embedded_support_trajectory(t) = embedded_support_trajectory(t) + embedded_support
        previous_development = development
     end do
  end do

  open(unit=10, file="outputs/fortran_genes_environment_plasticity.csv", status="replace")
  write(10, '(A)') "time,average_development,average_embedded_stress,average_embedded_support"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4,A,F10.4)') t - 1, ",", development_trajectory(t) / real(n_children), ",", embedded_stress_trajectory(t) / real(n_children), ",", embedded_support_trajectory(t) / real(n_children)
  end do
  close(10)

  print *, "Wrote outputs/fortran_genes_environment_plasticity.csv"
end program genes_environment_plasticity_simulation
