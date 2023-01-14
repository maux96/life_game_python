from time import sleep
from random import randint 

from life_game import LifeGame
from pygame_rendering import pygame_main
from constructions import GLIDER
import asyncio

def main():
    sizex=50
    sizey=40
    life_game = LifeGame(sizex,sizey)
    #life_game.set_random_cell_alive(total=10) 

    life_game.insert_configuration_in(randint(0,sizex),randint(0,sizey),GLIDER) 
    life_game.insert_configuration_in(randint(0,sizex),randint(0,sizey),GLIDER) 
    life_game.insert_configuration_in(randint(0,sizex),randint(0,sizey),GLIDER) 
    life_game.insert_configuration_in(randint(0,sizex),randint(0,sizey),GLIDER) 

    life_game.insert_configuration_in(randint(0,sizex),randint(0,sizey),GLIDER) 
    life_game.insert_configuration_in(randint(0,sizex),randint(0,sizey),GLIDER) 
    life_game.insert_configuration_in(randint(0,sizex),randint(0,sizey),GLIDER) 
    life_game.insert_configuration_in(randint(0,sizex),randint(0,sizey),GLIDER) 

    life_game.insert_configuration_in(randint(0,sizex),randint(0,sizey),GLIDER) 
    life_game.insert_configuration_in(randint(0,sizex),randint(0,sizey),GLIDER) 
    life_game.insert_configuration_in(randint(0,sizex),randint(0,sizey),GLIDER) 
    life_game.insert_configuration_in(randint(0,sizex),randint(0,sizey),GLIDER) 



    #console_loop(life_game)
    asyncio.run(pygame_main(life_game))
    
 

def console_loop(life_game):
    while not life_game.is_game_ended:
        print_board(life_game.get_board())
        print("="*30)
        sleep(0.5)
        life_game.next_generation()


def print_board(board):
    for row in board:
        print(" ".join(map(lambda x:str(x.value),row)))


if __name__=="__main__":
    main()
