import pygame
import time
from random import randint

pygame.init()
clock = pygame.time.Clock()

display_width = 768
display_height = 576

black = (0, 0, 0)
grey = (64, 64, 64)
white = (255, 255, 255)
red = (180, 0, 0)
bright_red = (255, 0, 0)
green = (0, 180, 0)
bright_green = (0, 255, 0)
ice_blue = (212, 240, 255)

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Sneaky Santa')
background = pygame.image.load("menu.png")
snowimg = pygame.image.load("snow.png")

def text_objects(text, font, colour=black):
    text_surface = font.render(text, True, colour)
    return text_surface, text_surface.get_rect()

def render_title(fontname, size, text):
    game_display.blit(background, (0, 0))
    # title
    large_text = pygame.font.Font(fontname, size)
    text_surf, text_rect = text_objects(text, large_text, white)
    text_rect.center = ((display_width/2)+4, (display_height/3)+4)
    game_display.blit(text_surf, text_rect)

    # shadow    
    large_text = pygame.font.Font(fontname, size)
    text_surf, text_rect = text_objects(text, large_text, black)
    text_rect.center = (display_width/2, display_height/3)
    game_display.blit(text_surf, text_rect)

    # subtitle ln 1
    large_text = pygame.font.Font(fontname, size//3)
    text_surf, text_rect = text_objects("It's 30 seconds 'til midnight...", large_text, black)
    text_rect.center = (display_width/2, 4*display_height/5)
    game_display.blit(text_surf, text_rect)

    # subtitle ln 2
    large_text = pygame.font.Font(fontname, size//3)
    text_surf, text_rect = text_objects("Deliver Tommy's presents before 12!", large_text, black)
    text_rect.center = (display_width/2, 9*display_height/10)
    game_display.blit(text_surf, text_rect)
    
    

def button(msg, x, y, width, height, colour, overcolour, action=None):

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    

    if x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y:
        pygame.draw.rect(game_display, colour, (x, y, width, height))
        pygame.draw.rect(game_display, overcolour, (x+5, y+5, width-10, height-10))
        if mouse_click[0] == 1 and action != None:
            if action == "play":
                return "play"
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(game_display, colour, (x, y, width, height))
            
    small_text = pygame.font.Font('8bitfont.ttf', 20)        
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = (((x + (width/2)), y + (height/2)))
    game_display.blit(text_surf, text_rect)
            
def play_intro_music():
    pygame.mixer.music.load("menu_theme_wav.wav")
    pygame.mixer.music.play(-1, 0.0)

def init_snowflakes():
    snowflakes = []
    for i in range(80):
        x = randint(-200,768)
        y = randint(-768, 0)
        snowflakes.append([snowimg, x, y])
    return snowflakes

def animate(snowflakes):
    for s in snowflakes:
        s[1] += 2
        s[2] += 5
        if s[1] > 768:
            s[1] = randint(-200, 768)
        if s[2] > 576:
            s[2] = randint(-768, 0)
        game_display.blit(s[0], (s[1], s[2]))
    return snowflakes

def display_menu():
    pygame.init()
    play_intro_music()
    intro = True
    snowflakes = init_snowflakes()
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                    
        game_display.fill(ice_blue)

        render_title("8bitfont.ttf", 90, "Sneaky Santa")

        if button("Start Game", (display_width/(16/3)), (display_height/(8/5)), 200, 50, green, bright_green, "play") == "play":
            break
        button("Quit Game", (display_width/(16/9)), (display_height/(8/5)), 200, 50, red, bright_red, "quit")
          
        snowflakes = animate(snowflakes)
        pygame.display.update()
        clock.tick()
