function xn=bisection(f,a0,b0,epsilon)
  if f(a0)*f(b0) > 0
    disp('Function must change sign over initial interval');
    xn=Inf;
    return;
  else
    k = ceil(log((b0-a0)/epsilon)/log(2))-1;
    an = a0;
    bn = b0;
    xn = (a0+b0)/2;
    for i = 1:k
      if f(an)*f(xn) < 0
	bn = xn;
      else
	an = xn;
      end
      xn = (an+bn)/2;
  end
end