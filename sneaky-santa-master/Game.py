import pygame
from Santa import Santa
from Obstacle import Obstacle
from Room import Room
from random import randint
import tkinter as tk
import time

class Game:
    def __init__(self):
        pygame.init()
        self.timer = 0
        self.score = 0
        
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load("game_theme_wav.wav")
        pygame.mixer.music.play(-1, 0.0)
        # screen size
        pygame.RESIZABLE = False
        root = tk.Tk()
        self.WIDTH = 768
        self.HEIGHT = 576
        
        # movement booleans
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        
        # pygame inits
        self.game_display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Sneaky Santa')
        self.gameExit = False

    def button(self, msg, x, y, width, height, colour, overcolour, action=None):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        

        if x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y:
                pygame.draw.rect(self.game_display, colour, (x, y, width, height))
                pygame.draw.rect(self.game_display, overcolour, (x+5, y+5, width-10, height-10))
                if mouse_click[0] == 1 and action != None:
                    if action == "play":
                        return "play"
                    elif action == "quit":
                        pygame.quit()
                        quit()
        else:
                pygame.draw.rect(self.game_display, colour, (x, y, width, height))
                
        small_text = pygame.font.Font('8bitfont.ttf', 20)        
        text_surf, text_rect = self.text_objects(msg, small_text)
        text_rect.center = (((x + (width/2)), y + (height/2)))
        self.game_display.blit(text_surf, text_rect)

    def text_objects(self, text, font, colour=(255, 255, 0)):
        text_surface = font.render(text, True, colour)
        return text_surface, text_surface.get_rect()
    
    def render_timer(self, timer1):
        left = 30 - timer1
        small_text = pygame.font.Font('8bitfont.ttf', 28)        
        text_surf, text_rect = self.text_objects("{0:.2f}".format(left), small_text)
        text_rect.center = ((self.WIDTH/1.07, self.HEIGHT/11))
        self.game_display.blit(text_surf, text_rect)
        
    def render_score(self):
        large_text = pygame.font.Font("8bitfont.ttf", 30)
        text_surf, text_rect = self.text_objects("Room", large_text, (255, 255, 0))
        text_rect.center = ((self.WIDTH/1.066, 3*self.HEIGHT/11))
        self.game_display.blit(text_surf, text_rect)
        
        large_text = pygame.font.Font("8bitfont.ttf", 34)
        text_surf, text_rect = self.text_objects(str(self.score), large_text, (255, 255, 0))
        text_rect.center = ((self.WIDTH/1.07, 4*self.HEIGHT/11))
        self.game_display.blit(text_surf, text_rect)
    
    def render_title(self, fontname, size, text):
        
        large_text = pygame.font.Font(fontname, size)
        text_surf, text_rect = self.text_objects(text, large_text, (255, 255, 255))
        text_rect.center = (((self.WIDTH/2)+4), ((self.HEIGHT/3)+4))
        self.game_display.blit(text_surf, text_rect)
        
        large_text = pygame.font.Font(fontname, size)
        text_surf, text_rect = self.text_objects(text, large_text, (0,0,0))
        text_rect.center = ((self.WIDTH/2), (self.HEIGHT/3))
        self.game_display.blit(text_surf, text_rect)

    def render_result(self):
        large_text = pygame.font.Font("8bitfont.ttf", 34)
        text_surf, text_rect = self.text_objects("Your score was "+str(self.score), large_text, (255, 255, 0))
        text_rect.center = ((self.WIDTH/2, 5*self.HEIGHT/9))
        self.game_display.blit(text_surf, text_rect)
        
    def game_over(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    

            self.render_title("8bitfont.ttf", 90, "GAME OVER")
            self.render_result()
            if self.button("Try again?", (self.WIDTH/(16/3)), (self.HEIGHT/(8/5)), 200, 50, (0, 180, 0), (0, 255, 0), "play") == "play":
                return "play"
            self.button("Quit Game", (self.WIDTH/(16/9)), (self.HEIGHT/(8/5)), 200, 50, (180, 0, 0), (255, 0, 0), "quit")
          
            pygame.display.update()
            self.clock.tick()

    def display_health(self):
        pygame.draw.rect(self.game_display, (0,255,0), (40, 50 + 100*(5-self.santa.hp), 20, self.santa.hp*100))
        pygame.draw.rect(self.game_display, (255,0,0), (40, 50, 20, 100*(5-self.santa.hp)))
        
    
    def game_loop(self, obstacles):
        hard_collision = False
        a_collision = True
        count = 0
        while True:
            if hard_collision:
                collision_status = self.room.obj_collision(self.santa)
                if collision_status == "HARD_OBJECT":
                    a_collision = self.collision_handler("ANOTHER")
                    count = 10
                    hard_collision = False
            count += 1

            if count == 15:
                hard_collision = False
                a_collision = True
            
            self.game_display.fill( (0, 0, 0) )
            self.game_display.blit(self.room.getimg(), (768/2 - 576/2, 0))
            self.game_display.blit(self.room.getexitimg(), self.room.exit.getpos())
            for o in obstacles:
                self.game_display.blit(o.getimg(), o.getpos())
            self.room.order_roamers()
            for r in self.room.roamers:
                self.game_display.blit(r.getimg(), r.getpos())
                if r.detected(self.santa.getx(), self.santa.gety(), self.santa.getwidth(), self.santa.getheight()):
                    return self.game_over()
            
            self.game_display.blit(self.santa.getimg(), self.santa.getpos())
            if not hard_collision and a_collision:
                count = 0
                self.controls()
                self.santa.setvel(self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed)
                collision_status = self.room.obj_collision(self.santa)
                hard_collision = self.collision_handler(collision_status)
            
            if 30 - self.timer < 0:
                return self.game_over()
            self.clock.tick()
            self.timer += 0.015
            self.render_timer((self.timer))
            self.render_score()
            FPS = str(int(self.clock.get_fps()))
            pygame.display.set_caption('Sneaky Santa '+ 'FPS: '+ FPS)
            self.santa.wall_collide()
            self.santa.update()
            self.display_health()
            if self.santa.isdead():
                return self.game_over()
            pygame.display.update()
            
            if self.santa.victory_check(self.room.getexitpos()):
                self.score += 1
                break

    def controls(self):
        for event in pygame.event.get():
                                    
            if event.type == pygame.QUIT:
                quit()

            # key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.up_pressed = True
                
                if event.key == pygame.K_s:
                    self.down_pressed = True
                
                if event.key == pygame.K_a:
                    self.left_pressed = True
                    
                if event.key == pygame.K_d:
                    self.right_pressed = True

            # key released
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.up_pressed = False
                
                if event.key == pygame.K_s:
                    self.down_pressed = False
                
                if event.key == pygame.K_a:
                    self.left_pressed = False
                    
                if event.key == pygame.K_d:
                    self.right_pressed = False

    def collision_handler(self, status):
        if status == "NO_COLLISION":
            return False
        elif status == "HARD_OBJECT":
            return self.santa.hard_object()
        elif status == "ANOTHER":
            return self.santa.another_collision()
            
      

