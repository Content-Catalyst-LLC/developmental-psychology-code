program adolescence_identity_simulation
  implicit none
  integer, parameter :: n=900, waves=10
  integer :: i,t
  real :: r, baseline, peer, family, connected, future, chronic, climate, counseling, extra, safety, dsafe
  real :: prev, p, f, s, a, x, d, ctx, score
  real :: identity(waves), support(waves), exclusion(waves), digital(waves)
  call random_seed()
  identity=0.0; support=0.0; exclusion=0.0; digital=0.0
  do i=1,n
    call random_number(r); baseline=42.0+16.0*r
    call random_number(r); peer=2.0*r-1.0
    call random_number(r); family=2.0*r-1.0
    call random_number(r); connected=2.0*r-1.0
    call random_number(r); future=2.0*r-1.0
    call random_number(r); chronic=merge(1.0,0.0,r<0.24)
    call random_number(r); climate=1.2*r-0.6
    call random_number(r); counseling=1.0*r-0.5
    call random_number(r); extra=1.0*r-0.5
    call random_number(r); safety=1.2*r-0.6
    call random_number(r); dsafe=1.0*r-0.5
    prev=baseline
    do t=1,waves
      call random_number(r); p=peer+0.7*(r-0.5)
      call random_number(r); f=family+0.7*(r-0.5)
      call random_number(r); s=connected+0.7*(r-0.5)
      call random_number(r); a=future+0.7*(r-0.5)
      call random_number(r); x=0.45*chronic-0.20*safety+0.70*(r-0.5)
      call random_number(r); d=0.30*chronic-0.25*dsafe+0.65*(r-0.5)
      ctx=p+f+s+a+climate+counseling+extra+safety+dsafe
      score=0.70*prev+0.85*real(t-1)+1.10*p+1.00*f+0.95*s+0.90*a+0.80*climate+0.70*counseling+0.65*extra+0.85*safety+0.55*dsafe-1.25*x-0.75*d-0.90*chronic
      identity(t)=identity(t)+score; support(t)=support(t)+ctx; exclusion(t)=exclusion(t)+x; digital(t)=digital(t)+d; prev=score
    end do
  end do
  open(unit=10,file="outputs/fortran_adolescence_identity.csv",status="replace")
  write(10,'(A)') "time,average_identity_score,average_support_context,average_exclusion,average_digital_stress"
  do t=1,waves
    write(10,'(I0,A,F10.4,A,F10.4,A,F10.4,A,F10.4)') t-1,",",identity(t)/real(n),",",support(t)/real(n),",",exclusion(t)/real(n),",",digital(t)/real(n)
  end do
  close(10)
  print *, "Wrote outputs/fortran_adolescence_identity.csv"
end program adolescence_identity_simulation
