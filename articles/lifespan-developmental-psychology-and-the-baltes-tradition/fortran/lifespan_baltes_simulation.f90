program lifespan_baltes_simulation
  implicit none

  integer, parameter :: n_people = 950
  integer, parameter :: n_periods = 12
  integer :: i, t
  real :: baseline, plasticity, support_base, comp_base, health, historical, institutional
  real :: previous_development, gains, losses, support, current_comp
  real :: selection, optimization, compensation, soc, development
  real :: random_value
  real :: development_trajectory(n_periods)
  real :: gains_trajectory(n_periods)
  real :: losses_trajectory(n_periods)
  real :: soc_trajectory(n_periods)

  call random_seed()
  development_trajectory = 0.0
  gains_trajectory = 0.0
  losses_trajectory = 0.0
  soc_trajectory = 0.0

  do i = 1, n_people
     call random_number(random_value)
     baseline = 42.0 + 16.0 * random_value
     call random_number(random_value)
     plasticity = 2.0 * random_value - 1.0
     call random_number(random_value)
     support_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     comp_base = 2.0 * random_value - 1.0
     call random_number(random_value)
     health = 1.6 * random_value - 0.8
     call random_number(random_value)
     historical = 1.2 * random_value - 0.6
     call random_number(random_value)
     institutional = 1.2 * random_value - 0.6
     previous_development = baseline

     do t = 1, n_periods
        call random_number(random_value)
        gains = 0.90 - 0.05 * real(t - 1) + 0.50 * (random_value - 0.5)
        call random_number(random_value)
        losses = 0.20 + 0.07 * real(t - 1) + 0.50 * (random_value - 0.5)
        call random_number(random_value)
        support = support_base + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        current_comp = comp_base + 0.70 * (random_value - 0.5)
        call random_number(random_value)
        selection = 0.30 + 0.04 * real(t - 1) + 0.50 * (random_value - 0.5)
        call random_number(random_value)
        optimization = 0.50 + 0.50 * (random_value - 0.5)
        call random_number(random_value)
        compensation = comp_base + 0.05 * real(t - 1) + 0.50 * (random_value - 0.5)
        soc = 0.35 * selection + 0.35 * optimization + 0.30 * compensation

        development = 0.70 * previous_development + &
                0.20 * real(t - 1) + &
                1.05 * gains - &
                1.00 * losses + &
                0.90 * plasticity + &
                0.95 * support + &
                0.80 * current_comp + &
                0.65 * health + &
                0.75 * historical + &
                0.70 * institutional + &
                0.90 * soc + &
                0.35 * plasticity * support - &
                0.30 * losses * compensation

        development_trajectory(t) = development_trajectory(t) + development
        gains_trajectory(t) = gains_trajectory(t) + gains
        losses_trajectory(t) = losses_trajectory(t) + losses
        soc_trajectory(t) = soc_trajectory(t) + soc
        previous_development = development
     end do
  end do

  open(unit=10, file="outputs/fortran_lifespan_baltes.csv", status="replace")
  write(10, '(A)') "time,average_development,average_gains,average_losses,average_soc"
  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4,A,F10.4,A,F10.4)') t - 1, ",", development_trajectory(t) / real(n_people), ",", gains_trajectory(t) / real(n_people), ",", losses_trajectory(t) / real(n_people), ",", soc_trajectory(t) / real(n_people)
  end do
  close(10)

  print *, "Wrote outputs/fortran_lifespan_baltes.csv"
end program lifespan_baltes_simulation
