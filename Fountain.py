from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform, randint



class vec3d():

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def inttup(self):
        return (int(self.x), int(self.y), int(self.z))

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

class Animation(PygameHelper):

    def __init__(self, w, h, v):
    
        self.w = w
        self.h = h

        #tick tock
        self.time = 0
        self.dt = 0.05
        
        #initial velocities, etc.
        self.v = v
        self.wn = Wind(0, 10)
        self.ws = Wind(0, 10)
        self.we = Wind(0, 10)
        self.ww = Wind(0, 10)
        self.wind_enabled = { 'n': True, 's': True, 'e':True, 'w':True }

        #water drops
        self.radius = 2
        self.droplets = []
        self.max_drops = 500

        #pygame
        PygameHelper.__init__(self, size=(self.w, self.h), fill=((255,255,255)))

        #labels
        self.aFont = pygame.font.Font(None, 24)
        self.y_velocity_label = self.aFont.render('Initial y-velocity %s m/s:' % self.v, 1, (10, 10, 10))
        self.wind_east_label = self.aFont.render('Current easterly wind velocity: %s' % self.we, 1, (10, 10, 10))
        self.wind_west_label = self.aFont.render('Current westerly wind velocity: %s' % self.ww, 1, (10, 10, 10))
        self.wind_north_label = self.aFont.render('Current northerly wind velocity: %s' % self.wn, 1, (10, 10, 10))
        self.wind_south_label = self.aFont.render('Current southerly wind velocity: %s' % self.ws, 1, (10, 10, 10))
        self.time_label = self.aFont.render('Time: %s s' % self.time, 1, (10, 10, 10))
        self.screen.blit(self.y_velocity_label, (10,10))
        self.screen.blit(self.wind_east_label, (10,30))
        self.screen.blit(self.wind_west_label, (10,50))
        self.screen.blit(self.wind_north_label, (self.w / 2 + 10,30))
        self.screen.blit(self.wind_south_label, (self.w / 2 + 10,50))
        self.screen.blit(self.time_label, (self.w - 150,10))

        #drawings
        self.draw_xy_fountain()
        self.draw_xy_axis()
        
        self.draw_xz_fountain()
        self.draw_xz_axis()
        
        self.draw_buttons()
        
        self.draw_lines()
        
    def draw_lines(self):
        pygame.draw.line(self.screen, (0,0,0), (self.w / 2, 0), (self.w / 2, self.h))
        #pygame.draw.line(self.screen, (0,0,0), (0, self.h - 100), (self.w, self.h - 100))
        
    def redraw_wind_label(self, d):
        if d == 'n':
            pygame.draw.rect(self.screen, (255,255,255), (self.w / 2 + 10, 30, self.w - 10, 20))
            self.wind_north_label = self.aFont.render('Current northerly wind velocity: %s' % self.wn, 1, (10, 10, 10))
            self.screen.blit(self.wind_north_label, (self.w / 2 + 10,30))
        elif d == 's':
            pygame.draw.rect(self.screen, (255,255,255), (self.w / 2 + 10, 50, self.w - 10, 20))
            self.wind_south_label = self.aFont.render('Current southerly wind velocity: %s' % self.ws, 1, (10, 10, 10))
            self.screen.blit(self.wind_south_label, (self.w / 2 + 10,50))
        elif d == 'e':
            pygame.draw.rect(self.screen, (255,255,255), (10, 30, self.w / 2 - 10, 20))
            self.wind_east_label = self.aFont.render('Current easterly wind velocity: %s' % self.we, 1, (10, 10, 10))
            self.screen.blit(self.wind_east_label, (10,30))
        elif d == 'w':
            pygame.draw.rect(self.screen, (255,255,255), (10, 50, self.w / 2 - 10, 20))
            self.wind_west_label = self.aFont.render('Current westerly wind velocity: %s' % self.ww, 1, (10, 10, 10))
            self.screen.blit(self.wind_west_label, (10,50))
        else:
            raise ValueError
            
        
    def draw_buttons(self):
        print 'Keys:\nN,S,E,W - Toggle N/S/E/W Winds\n'
    
    #xz methods
    def draw_xz_fountain(self):
        pos = self.translate_xz_pos_to_screen(vec3d(0,0,0))
        pos2 = self.translate_xz_pos_to_screen(vec3d(2,0,4))
        pygame.draw.circle(self.screen, (150,150,150), (pos.x, pos.y), 30)
#        pygame.draw.ellipse(self.screen, (150,150,150), (pos.x, pos.y, pos2.x, pos2.y))
    
    def translate_xz_pos_to_screen(self, pos):
        return vec2d(7 * self.w / 9 + 30 * pos.x, 2 * self.h / 4 + 20 * (-pos.z))

    def draw_xz_droplet(self, oldpos, newpos, rgb=(0,0,255)):
        pygame.draw.circle(self.screen, (255,255,255), self.translate_xz_pos_to_screen(oldpos).inttup(), self.radius)
        pygame.draw.circle(self.screen, (newpos.y*10,0,255-newpos.y*10), self.translate_xz_pos_to_screen(newpos).inttup(), self.radius)
        
    def draw_xz_axis(self):
        aFont = pygame.font.Font(None, 16)
        for i in range(-10, 11):
            pos = self.translate_xz_pos_to_screen(vec3d(i,0,-12))
            label = aFont.render('%s' % i, 1, (10, 10, 10))
            self.screen.blit(label, pos)
            
            pos = self.translate_xz_pos_to_screen(vec3d(-11,0,i))
            label = aFont.render('%s' % i, 1, (10, 10, 10))
            self.screen.blit(label, pos)            
            
    def update_z_wind(self):
        wind_did_change = False
        
        if self.wind_enabled['n']:
            self.wn.duration -= self.dt
            if self.wn.duration <= 0:
                self.wn = Wind(uniform(0, 2), float(randint(15, 20)))
                self.redraw_wind_label('n')
                wind_did_change = True
        if self.wind_enabled['s']:
            self.ws.duration -= self.dt
            if self.ws.duration <= 0:
                self.ws = Wind(-uniform(0, 2), float(randint(15, 20)))
                self.redraw_wind_label('s')
                wind_did_change = True

        return wind_did_change

    #xy methods
    def draw_xy_fountain(self):
        pos = self.translate_xy_pos_to_screen(vec2d(0,0))
        pygame.draw.rect(self.screen, (150,150,150), (pos.x - 20, pos.y, 30, 60))

    def draw_xy_axis(self):
        aFont = pygame.font.Font(None, 16)
        for i in range(-10, 11):
            pos = self.translate_xy_pos_to_screen(vec2d(i,-10))
            label = aFont.render('%s' % i, 1, (10, 10, 10))
            self.screen.blit(label, pos)
            
            pos = self.translate_xy_pos_to_screen(vec3d(10,i,0))
            label = aFont.render('%s' % i, 1, (10, 10, 10))
            self.screen.blit(label, pos) 

    def translate_xy_pos_to_screen(self, pos):
        return vec2d(self.w / 4 + 30 * pos.x, 3 * self.h / 5 + 21 * (-pos.y))

    def draw_xy_droplet(self, oldpos, newpos, rgb=(0,0,255)):
        pygame.draw.circle(self.screen, (255,255,255), self.translate_xy_pos_to_screen(oldpos).inttup(), self.radius)
        pygame.draw.circle(self.screen, (newpos.y*10,0,255-newpos.y*10), self.translate_xy_pos_to_screen(newpos).inttup(), self.radius)
        
    def update_x_wind(self):
        wind_did_change = False
        
        if self.wind_enabled['e']:
            self.we.duration -= self.dt
            if self.we.duration <= 0:
                self.we = Wind(uniform(0, 2), float(randint(15, 20)))
                self.redraw_wind_label('e')
                wind_did_change = True
        if self.wind_enabled['w']:
            self.ww.duration -= self.dt
            if self.ww.duration <= 0:
                self.ww = Wind(-uniform(0, 2), float(randint(15, 20)))
                self.redraw_wind_label('w')
                wind_did_change = True
                
        return wind_did_change

    #pygame
    def update(self):
        self.draw_xz_fountain()
        self.draw_xz_axis()
        self.draw_xy_axis()
        self.draw_lines()
    
        self.time += self.dt
        pygame.draw.rect(self.screen, (255,255,255), (self.w - 150, 10, self.w, 50))
        self.time_label = self.aFont.render('Time: %s s' % self.time, 1, (10, 10, 10))
        self.screen.blit(self.time_label, (self.w - 150,10))
        
        x_wind_did_change = self.update_x_wind()
        z_wind_did_change = self.update_z_wind()
        
        if len(self.droplets) < self.max_drops:
            new_d = Droplet(uniform(-2, 2), self.v, uniform(-2, 2))
            self.draw_xy_droplet(vec2d(0,0), new_d.pos)
            self.droplets.append(new_d)
        for d in self.droplets:
            oldpos = d.pos
            d.tx += self.dt
            d.ty += self.dt
            d.tz += self.dt
            if x_wind_did_change:
                d.tx = self.dt
                d.xp = oldpos.x
            if z_wind_did_change:
                d.tz = self.dt
                d.zp = oldpos.z
            d.pos = vec3d(d.x(d.tx, self.we, self.ww), d.y(d.ty), d.z(d.tz, self.wn, self.ws))
            self.draw_xy_droplet(oldpos, d.pos)
            self.draw_xz_droplet(oldpos, d.pos)
            if d.pos.y <= 0 or self.translate_xy_pos_to_screen(d.pos).x >= self.w or self.translate_xy_pos_to_screen(d.pos).x <= 0:
                pygame.draw.circle(self.screen, (255,255,255), self.translate_xy_pos_to_screen(d.pos).inttup(), self.radius)
                pygame.draw.circle(self.screen, (255,255,255), self.translate_xz_pos_to_screen(d.pos).inttup(), self.radius)
                self.droplets.remove(d)
                
    def keyUp(self, key):
        if key == K_n:
            toggle = not self.wind_enabled['n']
            self.wind_enabled['n'] = toggle
            if toggle:
                self.wn = Wind(0, 1)
            else:
                self.wn = Wind(0, float('inf'))
            self.redraw_wind_label('n')
            print 'Northern Winds %s' % ('Enabled' if toggle else 'Disabled')
        if key == K_s:
            toggle = not self.wind_enabled['s']
            self.wind_enabled['s'] = toggle
            if toggle:
                self.ws = Wind(0, 1)
            else:
                self.ws = Wind(0, float('inf'))
            self.redraw_wind_label('s')
            print 'Southern Winds %s' % ('Enabled' if toggle else 'Disabled')
        if key == K_e:
            toggle = not self.wind_enabled['e']
            self.wind_enabled['e'] = toggle
            if toggle:
                self.we = Wind(0, 1)
            else:
                self.we = Wind(0, float('inf'))
            self.redraw_wind_label('e')
            print 'Eastern Winds %s' % ('Enabled' if toggle else 'Disabled')
        if key == K_w:
            toggle = not self.wind_enabled['w']
            self.wind_enabled['w'] = toggle
            if toggle:
                self.ww = Wind(0, 1)
            else:
                self.ww = Wind(0, float('inf'))
            self.redraw_wind_label('w')
            print 'Western Winds %s' % ('Enabled' if toggle else 'Disabled')


width = 1300
height = 800
initial_vel = 100

s = Animation(width, height, initial_vel)
s.mainLoop(60)
