function vy=getvelocity(vt, g, vx, wx, d)
  x = @(t) -vt*exp(-g*t/vt)*(vx-wx)/g+wx*t-vt*(-vx+wx)/g-d
  s = bisection(x,0.01,100,10^-10);
  if(s == Inf)
    disp('Water will never reach the given distance.');
    vy = Inf;
    return;
  end
  y = @(vy) -vt*exp(-g*s/vt)*(vy+vt)/g-vt*s+(vy+vt)*vt/g;
  if(s == Inf)
    disp('Water will never reach the given distance before it hits the ground.');
    vy = Inf;
    return;
  end
  vy = bisection(y,0,500,10^-10);
end