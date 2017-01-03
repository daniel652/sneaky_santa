from Game import Game
from Santa import Santa
from Room import Room
from Obstacle import Obstacle
from Roamer import Roamer
from random import randint
import Menu

while True:
    Menu.display_menu()
    game = Game()
    while True:
        game.santa = Santa()
        obstacles = []
        roamer = Roamer(200, 150, 5, 72)
        roamer.settarget()
        game.room = Room(obstacles, [roamer])
        game.santa.setpos(game.room.gen_positions(game.santa.width, game.santa.height))
        
        for i in range(20):
            validpos = True
            while validpos:
                posx = randint(96, 528)
                posy = randint(0, 528)
                for o in obstacles:
                    distsquared = ((posx - o.getx())**2) + ((posy - o.gety())**2)
                    if distsquared < 15000:
                        validpos = False
                        break
                    distsquared = ((posx - game.santa.getx())**2) + ((posy - game.santa.gety())**2)
                    if distsquared < 15000:
                        validpos = False
                        break
                    distsquared = ((posx - game.room.getexitpos()[0])**2) + ((posy - game.room.getexitpos()[1])**2)
                    if distsquared < 15000:
                        validpos = False
                        break
                if validpos:
                    obstacles.append(Obstacle(posx, posy))
                    break
        game.room.setobstacles(obstacles)
        if game.game_loop(obstacles) == "play":
            break
