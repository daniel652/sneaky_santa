import pygame
from math import sqrt

class Santa:
    def __init__(self, x=0, y=0):
        self.imgF = pygame.image.load("santa_forward.png")
        self.imgB = pygame.image.load("santa_back.png")
        self.imgR = pygame.image.load("santa_right.png")
        self.imgL = pygame.image.load("santa_left.png")
        self.imgUR = pygame.image.load("santa_UR.png")
        self.imgDR = pygame.image.load("santa_DR.png")
        self.imgDL = pygame.image.load("santa_DL.png")
        self.imgUL = pygame.image.load("santa_UL.png")
        self.currentImage = self.imgF
        self.posx = x
        self.posy = y
        self.width = 48
        self.height = 48
        self.velx = 0
        self.vely = 0
        self.speed = 4
        self.diagonal_speed = self.speed/(2**0.5)
        self.hp = 5

    def setvel(self, up, down, left, right):
        if left and not right:
            self.velx = -self.speed
        elif right and not left:
            self.velx = self.speed
        elif (not left and not right) or (left and right):
            self.velx = 0

        if up and not down:
            self.vely = -self.speed
        elif down and not up:
            self.vely = self.speed
        elif (not up and not down) or (up and down):
            self.vely = 0

        if up and right:
            self.velx = self.diagonal_speed
            self.vely = -self.diagonal_speed
        if up and left:
            self.velx = -self.diagonal_speed
            self.vely = -self.diagonal_speed
        if down and left:
            self.velx = -self.diagonal_speed
            self.vely = self.diagonal_speed
        if down and right:
            self.velx = self.diagonal_speed
            self.vely = self.diagonal_speed
        
        
        
    def update(self):
        """Updates santa's position according to his velocity.
        """
        self.posx += self.velx
        self.posy += self.vely

    def setpos(self, pos):
        self.posx, self.posy = pos

    def hard_object(self):
        self.vely = -self.vely
        self.velx  = -self.velx
        self.hp -= 1
        return True

    def another_collision(self):
        self.vely = -self.vely
        self.velx = -self.velx
        return False

    def wall_collide(self):
        if self.posx < 96:
            self.posx = 96
            
        elif self.posx > 672 - self.width:
            self.posx = 672 - self.width
            
        if self.posy < 0:
            self.posy = 0

        elif self.posy > 576 - self.height:
            self.posy = 576 - self.height

    def isdead(self):
        return self.hp == 0
    def victory_check(self, exitpos):
        if exitpos[0] == 96 or exitpos[0] == 663:
            if self.posx + self.width > exitpos[0] and \
               self.posx < exitpos[0] + 9 and \
               self.posy + self.height > exitpos[1] and \
               self.posy < exitpos[1] + 100:
                return True
        else:
            if self.posx + self.width > exitpos[0] and \
               self.posx < exitpos[0] + 123 and \
               self.posy + self.height > exitpos[1] and \
               self.posy < exitpos[1] + 10:
                return True
        return False
            
    
    def getimg(self):
        """Returns santa's png image.
        """
        if self.velx > 0:
            if self.vely > 0:
                self.currentImage = self.imgDR
            elif self.vely < 0:
                self.currentImage = self.imgUR
            else:
                self.currentImage = self.imgR
        elif self.velx < 0:
            if self.vely > 0:
                self.currentImage = self.imgDL
            elif self.vely < 0:
                self.currentImage = self.imgUL
            else:
                self.currentImage = self.imgL
        elif self.vely < 0:
            self.currentImage = self.imgF
        elif self.vely > 0:
            self.currentImage = self.imgB
        else:
            return self.currentImage
        return self.currentImage
    def getx(self):
        """Retuns santa's x position.
        """
        return self.posx
    def gety(self):
        """Returns santa's y position.
        """
        return self.posy
    def getpos(self):
        """Returns santa's position as a tuple.
        """
        return (self.posx, self.posy)

    def getwidth(self):
        """Returns santa's width.
        """
        return self.width
    def getheight(self):
        """Returns santa's height.
        """
        return self.height
    def getsize(self):
        """Returns santa's size as a tuple.
        """
        return (self.width, self.height)
