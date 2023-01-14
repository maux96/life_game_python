import pygame
import asyncio
from time import time

from life_game import LifeGame
from cell import Cell

class PyGameCell:
    def __init__(self, x, y, life_game: LifeGame):
        self.x = x
        self.y = y
        self.size =SIZE 
        self.gap =GAP 
        self.life_game= life_game
        self.last_click = 0

    def draw(self, screen):
        is_dead = self.life_game._board[self.x][self.y]==Cell.DEAD
        if is_dead:
            color = (150, 20, 20)
        else:
            color = (0, 255, 0)

        xx = self.x * self.size + self.x * self.gap
        yy = self.y*self.size+self.y*self.gap
        pygame.draw.rect(screen, color, (xx,yy,self.size, self.size),
                         border_radius=2)
        if not is_dead:
            pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(xx+3,yy+1,self.size/3,3))

    def is_clicked(self, mouse_x, mouse_y):
        if (self.x*self.size+ self.x * self.gap < mouse_x < (self.x+1)*self.size + self.x * self.gap) and\
            (self.y*self.size+ self.y * self.gap < mouse_y < (self.y+1)*self.size+ self.y * self.gap ):
            return True
        return False

    @property
    def is_recently_clicked(self):
        return time() - self.last_click < 2 

    def holly_intervention(self):
        self.last_click = time()
        current_value=self.life_game._board[self.x][self.y]  
        self.life_game._board[self.x][self.y] = Cell.DEAD if current_value ==Cell.LIFE\
                                                          else Cell.LIFE


SIZE =12 
GAP = 3

async def pygame_main(life_game):
    xs =life_game._width
    ys =life_game._height
    screen = init_pygame_and_get_screen(xs, ys)

    clickable_cells = [
        [PyGameCell(x,y, life_game) for y in range(ys)] for x in range(xs)] 

    await asyncio.gather(
        move_across_time(life_game, screen, clickable_cells),
        pygame_event_loop(life_game, screen, clickable_cells) )

def init_pygame_and_get_screen(xs: int, ys: int):
    pygame.init()
    pygame.font.init()
    size = (xs*(SIZE+GAP), ys*(SIZE+GAP)  )
    screen = pygame.display.set_mode(size)

    return screen


async def pygame_event_loop(life_game: LifeGame, screen, clickable_cells:list[list[PyGameCell]]):
    
    is_clicking=False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_clicking = True
                change_on_touch(clickable_cells)
            elif event.type == pygame.MOUSEBUTTONUP:
                is_clicking = False
            elif is_clicking :
                change_on_touch(clickable_cells)

            elif event.type == pygame.KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[pygame.K_SPACE]:
                    global paused
                    print(f"Game {'started' if paused  else 'paused'}!")
                    paused=not paused
                if pressed_keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    exit()

                global TIME
                if pressed_keys[pygame.K_KP_PLUS] or pressed_keys[pygame.K_PLUS] :
                    TIME/=2 
                    print(TIME)
                elif pressed_keys[pygame.K_MINUS] or pressed_keys[pygame.K_KP_MINUS] :
                    TIME*=2 
                    print(TIME)


        await asyncio.sleep(0.05)
        draw_cells(clickable_cells, screen) 
        draw_current_status(screen)
        pygame.display.flip()
    pygame.quit()

def change_on_touch(clickable_cells: list[list[PyGameCell]]):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for row in clickable_cells:
        for cell in row:
            if cell.is_clicked(mouse_x, mouse_y) and not cell.is_recently_clicked:
                cell.holly_intervention()

paused = False 
gen_passed = 0
TIME = 0.1 
async def move_across_time(life_game: LifeGame, screen, clickable_cells):
     while True:
        while not paused:
            global gen_passed
            gen_passed +=1 
            life_game.next_generation()
            #draw_cells(clickable_cells, screen)
            await asyncio.sleep(TIME)
        await asyncio.sleep(1)

def draw_current_status(screen):
    font = pygame.font.SysFont('Comic Sans MS', 24)
    content = f"generations: {str(gen_passed)} (Speed: {TIME}) {'(Paused)' if paused else ''}" 
    text = font.render(content, True, (255, 255, 255))
    screen.blit(text,(0,0)) 
    pass

def draw_cells(cells, screen: pygame.Surface):
    screen.fill((50,20,20))
    for row in cells: 
        for cell in row:
            cell.draw(screen)
