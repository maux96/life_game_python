import pygame
import asyncio
from time import time

from life_game import LifeGame
from cell import Cell

class PyGameCell:
    def __init__(self, x, y, life_game: LifeGame):
        self.x = x
        self.y = y
        self.life_game= life_game
        self.last_click = 0

    def draw(self, screen):
        is_dead = self.life_game._board[self.x][self.y]==Cell.DEAD
        if is_dead:
            color =DEAD_COLOR 
        else:
            color =LIFE_COLOR 

        xx = self.x * SIZE + self.x * GAP
        yy = self.y*SIZE+self.y*GAP
        pygame.draw.rect(screen, color, (xx,yy,SIZE, SIZE),
                         border_radius=2 if ROUNDED else 0)
        if ROUNDED and not is_dead  :
            pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(xx+3,yy+1,SIZE/3,3))

    def draw_border(self, screen):
        if self.is_hover(*pygame.mouse.get_pos()):
            xx = self.x * SIZE + (self.x-1) * GAP
            yy = self.y*SIZE+(self.y-1)*GAP
            pygame.draw.rect(screen, (255,255,255), (xx,yy,int(SIZE+GAP*2), int(SIZE+GAP*2)),2,
                         border_radius=2 if ROUNDED else 0 )
            pass
    def is_hover(self, mouse_x, mouse_y):
        if (self.x*SIZE+ self.x * GAP < mouse_x < (self.x+1)*SIZE + self.x * GAP) and\
            (self.y*SIZE+ self.y * GAP < mouse_y < (self.y+1)*SIZE+ self.y * GAP ):
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


async def pygame_main(life_game, size=12, gap=3,
                      bg_color=(50,20,20),
                      life_color=(0, 255, 0),
                      dead_color=(150, 20, 20),
                      text_color=(220,220,220),
                      rounded=True):

    xs =life_game._width
    ys =life_game._height

    global SIZE, GAP, BG_COLOR, LIFE_COLOR, DEAD_COLOR, ROUNDED, TEXT_COLOR
    SIZE = size
    GAP= gap
    BG_COLOR=bg_color
    LIFE_COLOR=life_color
    DEAD_COLOR=dead_color
    TEXT_COLOR=text_color
    ROUNDED=rounded

    screen = init_pygame_and_get_screen(xs, ys)

    clickable_cells = [
        [PyGameCell(x,y, life_game) for y in range(ys)] for x in range(xs)] 

    await asyncio.gather(
        move_across_time(life_game),
        pygame_event_loop(life_game, screen, clickable_cells) )

def init_pygame_and_get_screen(xs: int, ys: int):
    pygame.init()
    pygame.font.init()
    size = (xs*(SIZE+GAP), ys*(SIZE+GAP)  )
    screen = pygame.display.set_mode(size)

    return screen


async def pygame_event_loop(life_game: LifeGame, screen, clickable_cells:list[list[PyGameCell]]):
    
    
    global semi_paused, paused
    is_clicking=False
    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                is_clicking = True
                change_on_touch(clickable_cells)
                semi_paused=True
            elif event.type == pygame.MOUSEBUTTONUP:
                is_clicking = False
                semi_paused= False
            elif is_clicking :
                change_on_touch(clickable_cells)
            elif event.type == pygame.KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[pygame.K_SPACE]:
                    print(f"Game {'started' if paused  else 'paused'}!")
                    paused=not paused
                if pressed_keys[pygame.K_ESCAPE] or pressed_keys[pygame.K_q] :
                    pygame.quit()
                    exit()
                if pressed_keys[pygame.K_h] :
                    global is_text_hidden
                    is_text_hidden=not is_text_hidden
                global TIME
                if pressed_keys[pygame.K_KP_PLUS] or pressed_keys[pygame.K_PLUS] :
                    TIME/=2 
                    print(f"Speed Increased! ({TIME})")
                elif pressed_keys[pygame.K_MINUS] or pressed_keys[pygame.K_KP_MINUS] :
                    TIME*=2 
                    print(f"Speed Decreased! ({TIME})")

            

        await asyncio.sleep(0.05)
        draw_cells(clickable_cells, screen) 
        if not is_text_hidden:
            draw_current_status(screen)
        pygame.display.flip()
    pygame.quit()

def change_on_touch(clickable_cells: list[list[PyGameCell]]):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for row in clickable_cells:
        for cell in row:
            if cell.is_hover(mouse_x, mouse_y) and not cell.is_recently_clicked:
                cell.holly_intervention()

paused = False 
semi_paused = False 
gen_passed = 0
is_text_hidden = False
TIME = 0.1 
async def move_across_time(life_game: LifeGame):
     while True:
        while not paused and not semi_paused:
            global gen_passed
            gen_passed +=1 
            life_game.next_generation()
            await asyncio.sleep(TIME)
        await asyncio.sleep(1)

def draw_current_status(screen):
    font = pygame.font.SysFont('Comic Sans MS', 24)
    content = f"generations: {str(gen_passed)} (Speed: {TIME}) {'(Paused)' if paused else ''}" 
    content += '(Semi-paused)' if not paused and semi_paused else ''
    text = font.render(content, True, TEXT_COLOR)
    screen.blit(text,(0,0)) 
    pass

def draw_cells(cells, screen: pygame.Surface):
    screen.fill(BG_COLOR)
    for row in cells: 
        for cell in row:
            cell.draw(screen)
            cell.draw_border(screen)
