program timing_window_simulation
  implicit none

  integer, parameter :: n_people = 900
  integer, parameter :: n_periods = 14
  integer :: i, t
  real :: experience, support, adversity, random_value
  real :: critical_weight, early_sensitive, adolescent_sensitive
  real :: critical_outcome, sensitive_outcome, multi_window_outcome
  real :: critical_sum(n_periods), sensitive_sum(n_periods), multi_sum(n_periods)

  call random_seed()
  critical_sum = 0.0
  sensitive_sum = 0.0
  multi_sum = 0.0

  do i = 1, n_people
     call random_number(support)
     call random_number(adversity)
     support = 2.0 * support - 1.0
     adversity = 2.0 * adversity - 1.0

     do t = 1, n_periods
        call random_number(random_value)
        experience = 2.0 * random_value - 1.0

        if (t >= 3 .and. t <= 5) then
           critical_weight = 1.0
        else
           critical_weight = 0.0
        end if

        early_sensitive = exp(-((real(t) - 4.0)**2) / (2.0 * 2.0**2))
        adolescent_sensitive = exp(-((real(t) - 10.0)**2) / (2.0 * 2.2**2))

        call random_number(random_value)
        critical_outcome = 50.0 + 0.3 * real(t) + &
             2.2 * experience * critical_weight + &
             0.6 * support - 0.7 * adversity + &
             2.0 * (random_value - 0.5)

        call random_number(random_value)
        sensitive_outcome = 50.0 + 0.3 * real(t) + &
             2.0 * experience * early_sensitive + &
             0.6 * support - 0.7 * adversity + &
             2.0 * (random_value - 0.5)

        call random_number(random_value)
        multi_window_outcome = 50.0 + 0.3 * real(t) + &
             1.4 * experience * early_sensitive + &
             1.2 * experience * adolescent_sensitive + &
             0.6 * support - 0.7 * adversity + &
             2.0 * (random_value - 0.5)

        critical_sum(t) = critical_sum(t) + critical_outcome
        sensitive_sum(t) = sensitive_sum(t) + sensitive_outcome
        multi_sum(t) = multi_sum(t) + multi_window_outcome
     end do
  end do

  open(unit=10, file="outputs/fortran_timing_windows.csv", status="replace")
  write(10, '(A)') "time,critical_outcome,sensitive_outcome,multi_window_outcome"

  do t = 1, n_periods
     write(10, '(I0,A,F10.4,A,F10.4,A,F10.4)') &
        t, ",", critical_sum(t) / real(n_people), ",", &
        sensitive_sum(t) / real(n_people), ",", &
        multi_sum(t) / real(n_people)
  end do

  close(10)

  print *, "Wrote outputs/fortran_timing_windows.csv"
end program timing_window_simulation
