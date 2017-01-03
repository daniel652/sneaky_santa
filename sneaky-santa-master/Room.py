import pygame
from random import randint

class Exit:
    def __init__(self):
        self.posx = 0
        self.posy = 0
    
    def setpos(self, pos):
        self.posx, self.posy = pos
    def getpos(self):
        return (self.posx, self.posy)
        
class Room:
    def __init__(self, obs, roa):
        self.img1 = pygame.image.load("room_green.png")
        self.img2 = pygame.image.load("room_pink.png")
        self.img3 = pygame.image.load("room_blue.png")
        self.img4 = pygame.image.load("room_yellow.png")
        imgs = [self.img1, self.img2, self.img3, self.img4]
        self.curr_img = imgs[randint(0,3)]
        self.obstacles = obs
        self.roamers = roa
        self.width = 576
        self.height = self.width
        self.exit = Exit()
        self.exitimg = None
    
    def obj_collision(self, santa):
        """Check each obstacle to see if santa has collided.
        """
        for o in self.obstacles:
            status = o.collided(santa)
            if status != "NO_COLLISION":
                return status
        return status

    def order_roamers(self):
        for r in self.roamers:
            r.update()
    
    def gen_positions(self, sw, sh):
        """Returns santa's starting position."""
        santa_pos = [(96, randint(0, self.height - sh)), #left
                     (randint(96, self.width - sw), 0), #top
                     ((96+self.width) - sw, randint(0, self.height - sh)), #right
                     (randint(96, self.width - sw), self.height - sh)] #bottom
                                                             
        exit_pos = [(96, randint(0, self.height - 100)), #left
                    (randint(96, self.width - 123), 0), #top
                    ((96+self.width) - 9, randint(0, self.height - 100)), #right
                    (randint(96, self.width - 123), 566)] #bottom

        exit_int = randint(0,3)
        if exit_int%2 == 0:
            self.exitimg = pygame.image.load("doorv.png")
        else:
            self.exitimg = pygame.image.load("door.png")
        self.exit.setpos(exit_pos[exit_int])
        return santa_pos[(exit_int+2)%4]

    def setobstacles(self, obstacles):
        self.obstacles = obstacles
    
    def getexitpos(self):
        return self.exit.getpos()
    def getimg(self):
        return self.curr_img
    def getexitimg(self):
        return self.exitimg
    def getobstacles(self):
        return self.obstacles
