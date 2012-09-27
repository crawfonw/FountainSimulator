from vec import vec3d
from math import e

class Droplet():

    def __init__(self, xs, ys, zs):
        #velocities
        self.xs = xs
        self.ys = ys
        self.zs = zs
        
        #current pos
        self.pos = vec3d(0,0,0)
        
        #time counters
        self.ty = 0
        self.tx = 0
        self.tz = 0
        
        #starting pos
        self.xp = 0
        self.yp = 0
        self.zp = 0

    def y(self, t):
        return -.2102040816*e**(-4.757281553*t)*(self.ys+2.060000000)-2.060000000*t+.2102040816*self.ys+.4330204082 + self.yp

    def x(self, t, we, ww):
        return -.2102040816*e**(-4.757281553*t)*(self.xs-1.*we-1.*ww)+(we+ww)*t+self.xp+.2102040816*self.xs-.2102040816*we-.2102040816*ww
    
    def z(self, t, wn, ws):
        return -.2102040816*e**(-4.757281553*t)*(self.zs-1.*wn-1.*ws)+(wn+ws)*t+self.zp+.2102040816*self.zs-.2102040816*wn-.2102040816*ws

class Wind():

    def __init__(self, v, d):
        self.v = v
        self.duration = d

    def __str__(self):
        return '%s m/s' % self.v
        
    def __add__(self, other):
        return self.v + other
        
    __radd__ = __add__
    
    def __sub__(self, other):
        return self.v - other
        
    __rsub__ = __sub__

    def __neg__(self):
        return -self.v

    def __mul__(self, other):
        return self.v * other

    __rmul__ = __mul__