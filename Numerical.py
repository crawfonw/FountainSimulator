import math

def bisection(f, a0, b0, epsilon):
    if f(a0) * f(b0) > 0:
        print 'Function must change sign over initial interval'
        return float('inf')
    else:
        k = math.ceil(math.log((b0 - a0)/epsilon)/math.log(2)) - 1
        an = a0
        bn = b0
        xn = (a0 + b0)/2.0
        for i in range(1, int(k)+1):
            if f(an) * f(xn) < 0:
                bn = xn
            else:
                an = xn
            xn = (an + bn)/2.0
    return xn

def get_velocity(vt, g, vx, wx, d):
    x = lambda t:-vt*math.e**(-g*t/vt)*(vx-wx)/g+wx*t-vt*(-vx+wx)/g-d
    s = bisection(x,0.01,100,10**(-10));
    if s == float('inf'):
        print 'Water will never reach the given distance.'
        return float('inf')
    y = lambda vy: -vt*math.e**(-g*s/vt)*(vy+vt)/g-vt*s+(vy+vt)*vt/g;
    if y == float('inf'):
        print 'Water will never reach the given distance before it hits the ground.'
        return float('inf')
    return bisection(y,0,500,10**(-10))