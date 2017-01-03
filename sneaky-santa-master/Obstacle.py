import pygame
from random import randint

class Obstacle:
    def __init__(self, x=None, y=None):
        self.img1 = pygame.image.load("obstacles_lego.png")
        self.img2 = pygame.image.load("obstacles_track.png")
        self.img3 = pygame.image.load("obstacles_chair.png")
        self.img4 = pygame.image.load("table.png")
        imgs = [self.img1, self.img2, self.img3, self.img4]
        self.curr_img = imgs[randint(0,3)]
        self.posx = x
        self.posy = y
        self.width = 48
        self.height = 48

    def collided(self, santa):
        """Check if a given santa has collided with this obstacle.
        """
        sx, sy = santa.getpos()
        sw, sh = santa.getsize()
        if sx+sw > self.posx and \
           sx < self.posx + self.width and \
           sy+sh > self.posy and \
           sy < self.posy + self.height:
            return "HARD_OBJECT"
        else:
            return "NO_COLLISION"

    def getimg(self):
        return self.curr_img
    def getx(self):
        return self.posx
    def gety(self):
        return self.posy
    def getpos(self):
        return (self.posx, self.posy)
