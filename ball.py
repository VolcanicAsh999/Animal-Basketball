import pygame
import numpy as np
from scipy.integrate import ode


class Ball(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, dx=0, dy=0):
        super().__init__()
        self.image = pygame.image.load('images/basketball.png')
        self.state = [x,y,dx,dy]
        self.prev_state = [x,y,dx,dy]
        self.mass = 0.1
        self.t = 0
        self.radius = 15
        self.friction = 0.0001
        self.g = 9.8

        self.solver = ode(self.f)
        self.solver.set_integrator('dop853')
        self.solver.set_f_params(self.friction, self.g)
        self.solver.set_initial_value(self.state, self.t)

    @property
    def rect(self):
        rect = self.image.get_rect()
        rect.center = (self.state[0], 700 - self.state[1])
        return rect

    def f(self, t, state, arg1, arg2):
        dx = state[2]
        dy = state[3]
        dvx = -state[2] * arg1
        dvy = -arg2 - state[3] * arg1
        dx += dvx
        dy += dvy
        return [dx, dy, dvx, dvy]

    def set_pos(self, pos):
        self.state[0:2] = pos
        self.solver.set_initial_value(self.state, self.t)
        return self

    def set_vel(self, vel):
        self.state[2:] = vel
        self.solver.set_initial_value(self.state, self.t)


    def update(self, dt, ground):
        self.t += dt
        self.prev_state = self.state[:]
        self.state = self.solver.integrate(self.t)
        if (700 - self.state[1]) > 680:
            self.set_vel((self.state[2], -self.state[3]))
            self.state[1] += 5
        if self.state[0] < 0 or self.state[0] > 970:
            self.state[2] = -self.state[2]

    def move_by(self, delta):
        self.prev_state = self.state[:]
        self.state[0:2] = np.add(self.state[0:2], delta)
        return self
    
    def draw(self, surface):
        rect = self.image.get_rect()
        rect.center = (self.state[0], 700 - self.state[1])
        surface.blit(self.image, rect)
