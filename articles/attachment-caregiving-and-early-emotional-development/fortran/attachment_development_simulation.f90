program attachment_development_simulation
  implicit none
  integer, parameter :: n=900, waves=10
  integer :: i,t
  real :: r, baseline, care, repair, caregiver_support, chronic, temperament, support_need
  real :: childcare, safety, services, ecology
  real :: prev, stress, support_context, score
  real :: avg_score(waves), avg_context(waves), avg_stress(waves)
  call random_seed()
  avg_score=0.0; avg_context=0.0; avg_stress=0.0

  do i=1,n
    call random_number(r); baseline=42.0+16.0*r
    call random_number(r); chronic=merge(1.0,0.0,r<0.30)
    call random_number(r); support_need=merge(1.0,0.0,r<0.16)
    call random_number(r); temperament=2.0*r-1.0
    prev=baseline
    do t=1,waves
      call random_number(r); care=2.0*r-1.0
      call random_number(r); repair=2.0*r-1.0
      call random_number(r); caregiver_support=2.0*r-1.0
      call random_number(r); childcare=1.2*r-0.6
      call random_number(r); safety=1.2*r-0.6
      call random_number(r); services=1.2*r-0.6
      call random_number(r); ecology=1.2*r-0.6
      call random_number(r); stress=0.35*chronic+0.8*(r-0.5)
      support_context=care+repair+caregiver_support+childcare+safety+services+ecology
      score=0.70*prev+0.90*real(t-1)+1.35*care+1.10*repair+1.00*caregiver_support+0.80*childcare+0.75*safety+0.80*services+0.75*ecology-1.30*stress-0.95*chronic+0.75*temperament*care-0.85*temperament*stress+0.70*support_need*services+0.25*support_context
      avg_score(t)=avg_score(t)+score
      avg_context(t)=avg_context(t)+support_context
      avg_stress(t)=avg_stress(t)+stress
      prev=score
    end do
  end do

  open(unit=10,file="outputs/fortran_attachment_development.csv",status="replace")
  write(10,'(A)') "time,average_regulation,average_support_context,average_stress"
  do t=1,waves
    write(10,'(I0,A,F10.4,A,F10.4,A,F10.4)') t-1,",",avg_score(t)/real(n),",",avg_context(t)/real(n),",",avg_stress(t)/real(n)
  end do
  close(10)
  print *, "Wrote outputs/fortran_attachment_development.csv"
end program attachment_development_simulation
