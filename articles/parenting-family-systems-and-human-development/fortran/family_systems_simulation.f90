program family_systems_simulation
  implicit none

  integer, parameter :: n_children = 850
  integer, parameter :: n_periods = 10
  integer :: i, t
  real :: parenting, family, stress, sibling, regulation
  real :: stability, kin, security, caregiver_support
  real :: previous_development, development, family_support
  real :: random_value
  real :: development_trajectory(n_periods)
  real :: support_trajectory(n_periods)

  call random_seed()
  development_trajectory = 0.0
  support_trajectory = 0.0

  do i = 1, n_children
     call random_number(random_value)
     parenting = 2.0 * random_value - 1.0
     call random_number(random_value)
     family = 2.0 * random_value - 1.0
     call random_number(random_value)
     stress = 2.0 * random_value - 1.0
     call random_number(random_value)
     sibling = 1.6 * random_value - 0.8
     call random_number(random_value)
     regulation = 1.6 * random_value - 0.8
     call random_number(random_value)
     stability = 1.2 * random_value - 0.6
     call random_number(random_value)
     kin = 1.0 * random_value - 0.5
     call random_number(random_value)
     security = 1.2 * random_value - 0.6
     call random_number(random_value)
     if (random_value < 0.35) then
        caregiver_support = 1.0
     else
        caregiver_support = 0.0
     end if
     call random_number(random_value)
     previous_development = 47.0 + 6.0 * random_value

     do t = 1, n_periods
        call random_number(random_value)

        family_support = parenting + family + stability + kin + security - stress

        development = 0.70 * previous_development + &
                0.24 * real(t - 1) + &
                1.15 * parenting + &
                1.05 * family + &
                0.90 * stability + &
                0.80 * kin + &
                0.75 * security + &
                0.70 * sibling + &
                0.65 * regulation + &
                0.85 * caregiver_support - &
                1.10 * stress + &
                0.45 * parenting * family + &
                2.3 * (random_value - 0.5)

        development_trajectory(t) = development_trajectory(t) + development
        support_trajectory(t) = support_trajectory(t) + family_support
        previous_development = development
     end do
  end do

  open(unit=10, file="outputs/fortran_family_systems.csv", status="replace")
  write(10, '(A)') "time,average_development,average_family_support"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4)') t - 1, ",", development_trajectory(t) / real(n_children), ",", support_trajectory(t) / real(n_children)
  end do
  close(10)

  print *, "Wrote outputs/fortran_family_systems.csv"
end program family_systems_simulation
