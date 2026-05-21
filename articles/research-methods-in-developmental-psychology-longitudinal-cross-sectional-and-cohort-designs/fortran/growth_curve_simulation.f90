program growth_curve_simulation
  implicit none

  integer, parameter :: n_people = 1200
  integer, parameter :: n_waves = 6
  integer :: i, wave
  real :: age, centered_age, score, baseline, support, risk, random_value
  real :: wave_sum(n_waves), wave_count(n_waves)

  call random_seed()
  wave_sum = 0.0
  wave_count = 0.0

  do i = 1, n_people
     call random_number(random_value)
     baseline = 2.0 * random_value - 1.0

     call random_number(random_value)
     support = 2.0 * random_value - 1.0

     call random_number(random_value)
     risk = 2.0 * random_value - 1.0

     do wave = 1, n_waves
        age = 8.0 + real(wave - 1)
        centered_age = age - 11.5

        call random_number(random_value)

        score = 50.0 + &
                0.95 * centered_age - &
                0.035 * centered_age * centered_age + &
                1.0 * baseline + &
                1.1 * support - &
                1.2 * risk + &
                2.0 * (random_value - 0.5)

        wave_sum(wave) = wave_sum(wave) + score
        wave_count(wave) = wave_count(wave) + 1.0
     end do
  end do

  open(unit=10, file="outputs/fortran_growth_curve.csv", status="replace")
  write(10, '(A)') "study_wave,average_development_score"

  do wave = 1, n_waves
     write(10, '(I0,A,F10.4)') wave - 1, ",", wave_sum(wave) / wave_count(wave)
  end do

  close(10)

  print *, "Wrote outputs/fortran_growth_curve.csv"
end program growth_curve_simulation
