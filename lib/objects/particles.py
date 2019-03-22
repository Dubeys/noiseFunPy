import pygame, random, noise
from lib.utilities.utils import *


class Particle:

    def __init__(self, x = 0, y = 0, size = 4, color = (255, 255, 255), rnd = 0): 
        self.pos = vector2(x,y)
        self.origin = vector2(x, y)

        self.oriDir = vector2(0,0)

        self.dir = vector2(0, 0)

        self.rnd = rnd

        self.sum = 0
        self.counter = 0
        self.size = size
        self.color = color

        self.firstFrame = True

    def draw(self, display):
        if self.color == (0,0,0):
            return
        pygame.draw.rect(display, self.color, pygame.Rect(self.pos["x"], self.pos["y"], self.size, self.size))

    def setRandomDir(self,offset = 0, scale = .02):        
        self.dir['x'] = mapPolar(noise.pnoise3(self.origin['x'] * scale, self.origin['y'] * scale ,offset,base=self.rnd))
        self.dir['y'] = mapPolar(noise.pnoise3(self.origin['x'] * scale, self.origin['y'] * scale ,offset+1,base=self.rnd))
        x,y = self.getDirection()
        self.oriDir = vector2(x,y)

    def nudge(self, value, timeFactor=1, hueOffset = 0, firstRender = False):
        dx,dy = self.getDirection()
        ox,oy = self.getOrigin()

        ox, oy = self.getOrigin()

        self.pos['x'] = value * dx + ox
        self.pos['y'] = -value * dy + oy

        x,y = self.getPosition()

        # self.color = clamp(hsv2rgb(velocity * .2, velocity / 2 + .5, velocity / 2 + .5), 0, 255)
        if not firstRender:
            distanceTraveled = math.sqrt((ox - x) * (ox - x) + (oy - y) * (oy - y))
            # velocity = clamp(distanceTraveled / 2 * elapsedTime * 100, 0, 1)
            velocity = clamp(distanceTraveled / 2 * (1/ timeFactor), 0, 1)
            self.color = clamp(hsv2rgb((velocity * .05 + hueOffset) % 1, 1, (velocity * velocity) * .1 + .9), 0, 255)
        else:
            self.color = clamp(hsv2rgb(hueOffset % 1, 1,.3), 0, 255)
        # self.color = clamp(hsv2rgb(0, 0, velocity / 2 + .5), 0, 255)

    def testNudge(self, value):
        dx, dy = self.getDirection()
        ox, oy = self.getOrigin()

        oldx, oldy = self.getPosition()

        return value * dx + ox, -value * dy + oy

    def rotateDirection(self, angle):
        direction = self.getOriginalDirection()
        x,y = rotate(direction, angle)
        self.setDirection(x,y)

    def setDirection(self, x, y):
        self.dir['x'] = x
        self.dir['y'] = y

    def getPosition(self):
        return (self.pos['x'], self.pos['y'])

    def getOrigin(self):
        return (self.origin['x'], self.origin['y'])

    def getOriginalDirection(self):
        return (self.oriDir['x'], self.oriDir['y'])

    def getDirection(self):
        return (self.dir['x'], self.dir['y'])
