from time import sleep
from random import randint 
from sys import argv

from life_game import LifeGame
from pygame_rendering import pygame_main
from constructions import GLIDER
import asyncio


sizex=50
sizey=40
cellsize=12
gap=2
bg_color=(50,20,20)
life_color=(0, 255, 0)
dead_color=(150, 20, 20)
text_color=(220,220,220)
rounded=True

def config():
    global sizex, sizey,cellsize, gap,bg_color, dead_color,life_color, rounded, text_color
    i=0
    while i<len(argv):
        current = argv[i]
        if current == '--size-x':
            sizex=int(argv[i+1])
        elif current == '--size-y':
            sizey=int(argv[i+1])
        elif current == '--cell-size':
            cellsize=int(argv[i+1])
        elif current == '--gap':
            gap=int(argv[i+1])
        elif current == '--bg-color':
            bg_color=tuple(map(int,argv[i+1].split(",")))
        elif current == '--dead-color':
            dead_color=tuple(map(int,argv[i+1].split(",")))
        elif current == '--life-color':
            life_color=tuple(map(int,argv[i+1].split(",")))
        elif current == '--text-color':
            text_color=tuple(map(int,argv[i+1].split(",")))
        elif current == '--not-rounded':
            rounded=False
        elif current == '--help':
            print_help()
            exit()
        i+=1
def main():

    config()

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
    asyncio.run(pygame_main(life_game,size=cellsize, gap=gap,
                            bg_color=bg_color,
                            dead_color=dead_color,
                            life_color=life_color,
                            text_color=text_color,
                            rounded=rounded
                            )
                )
    
 

def console_loop(life_game):
    while not life_game.is_game_ended:
        print_board(life_game.get_board())
        print("="*30)
        sleep(0.5)
        life_game.next_generation()


def print_board(board):
    for row in board:
        print(" ".join(map(lambda x:str(x.value),row)))

def print_help():
    print("""
The total number of rows, columns, cell size, gap, background color,
dead cells color, life cells color and if the cell is not rounded can
be changed using the parameters as following:

python src/main.py --size-x n1\\
                   --size-y n2\\
                   --cell-size n3\\
                   --gap n4\\
                   --bg-color red_bg,green_bg,blue_bg\\
                   --dead-color red_dead,green_dead,blue_dead\\
                   --life-color red_life,green_life,blue_life\\
                   --text-color red_text,green_text,blue_text\\
                   --not-rounded

where `n1,n1,n3,n4` and the `[color]_[type]` are integers.

You can use `--help` to display this help.
""")


if __name__=="__main__":
    main()
