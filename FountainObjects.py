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
        return -.7812500000*e**(-1.280000000*t)*(self.xs-.7812500000*we-.7812500000*ww)+(.7812500000*we+.7812500000*ww)*t+.7812500000*self.xs-.6103515625*we-.6103515625*ww + self.xp
    
    def z(self, t, wn, ws):
        return -.7812500000*e**(-1.280000000*t)*(self.zs-.7812500000*wn-.7812500000*ws)+(.7812500000*wn+.7812500000*ws)*t+.7812500000*self.zs-.6103515625*wn-.6103515625*ws + self.zp

class Wind():

    def __init__(self, v, d):
        self.v = v
        self.duration = d

    def __str__(self):
        return '%s m/s' % self.v

    def __neg__(self):
        return -self.v

    def __mul__(self, other):
        return self.v * other

    __rmul__ = __mul__