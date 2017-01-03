import pygame
from random import randint

class Roamer:
    def __init__(self, tx, ty, sp, r):
        self.img = pygame.image.load("hitbox.png")
        self.posx = 384
        self.posy = 288
        self.width = 48
        self.height = 48
        self.velx = 0
        self.vely = 0
        self.targetx = tx
        self.targety = ty
        self.width = 48
        self.height = 48
        self.speed = sp
        self.radius = r

    def detected(self, sx, sy, sw, sh):
        distsquared = (((self.posx+24) - (sx+sw/2))**2) + (((self.posy+24) - (sy+sh/2))**2)
        if distsquared < self.radius**2:
            return True
        else:
            return False

    def settarget(self):
        self.targetx = randint(120, 480)
        self.targety = randint(40, 400)
        
        xdist = self.targetx - self.posx
        ydist = self.targety - self.posy
        diadist = ((xdist**2) + (ydist**2))**0.5

        self.velx = (xdist/diadist) * self.speed
        self.vely = (ydist/diadist) * self.speed

    def update(self):
        self.posx += self.velx
        self.posy += self.vely
        if abs(self.posx-self.targetx) <= 10 and abs(self.posy-self.targety) <= 10:
            self.settarget()

    def getpos(self):
        return (int(self.posx), int(self.posy))
    def getimg(self):
        return self.img
