import pygame, random
from pygame.locals import *

from src.quadtree.quadtree import Quad, Rect, Point
from src.quadtree.locals import *

def new_cellmap():
    cellmap = [0 for i in range(CELLMAP_WIDTH*CELLMAP_WIDTH)]
    return cellmap

def random_cellmap(chance):
    cellmap = [random.randint(1, 1/chance) for i in range(CELLMAP_WIDTH*CELLMAP_WIDTH)]
    return cellmap

def get_cell(cellmap, row, col):
    return cellmap[row*CELLMAP_WIDTH + col]

def set_cell(cellmap, row, col, value):
    cellmap[row*CELLMAP_WIDTH + col] = value

class CellMap:
    def __init__(self, initial_state=None):
        if initial_state is None:
            self.current_map = new_cellmap()
        else:
            self.current_map = initial_state
        
        self.quad_boundary = Rect(0, 0, CELLMAP_WIDTH, CELLMAP_HEIGHT)
        self.quadtree = Quad(self.quad_boundary, 5)
        self.search_rect = Rect(0, 0, 10, 10)

    def update_quadtree(self):
        self.quadtree = Quad(self.quad_boundary, 5)
        for i in range(CELLMAP_WIDTH*CELLMAP_HEIGHT):
            if self.current_map[i] == 1:
                self.quadtree.insert(Point(i % CELLMAP_WIDTH, i // CELLMAP_WIDTH))
    
class App:
    def __init__(self, cellmap=None):

        successes, fails = pygame.init()

        self.cellmap = CellMap(cellmap)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.running = True

        self.mouse_down = False
        self.mouse_up = False

        self.hold = False
        self.hold_value = None

        self.mouse_row = None
        self.mouse_col = None
        

    def run(self):
        while self.running:

            self.clock.tick(60)

            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_up = True

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                self.mouse_col, self.mouse_row = int(mouse_pos[0] // CELL_WIDTH), int(mouse_pos[1] // CELL_HEIGHT)
            
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.cellmap.current_map = new_cellmap()
                    self.cellmap.generation = 0
                    print('clear')

                elif event.key == pygame.K_r:
                    self.cellmap.current_map = random_cellmap(RANDOM_CHANCE)
                    print('random')

        if self.mouse_down:

            self.hold = True

            if get_cell(self.cellmap.current_map, self.mouse_row, self.mouse_col) == 1:

                set_cell(self.cellmap.current_map, self.mouse_row, self.mouse_col, 0)
                self.hold_value = 0

            elif get_cell(self.cellmap.current_map, self.mouse_row, self.mouse_col) == 0:

                set_cell(self.cellmap.current_map, self.mouse_row, self.mouse_col, 1)
                self.hold_value = 1

            self.mouse_down = False

        if self.hold:

            set_cell(self.cellmap.current_map, self.mouse_row, self.mouse_col, self.hold_value)

            if self.mouse_up:

                self.hold = False
                self.mouse_up = False

    def update(self):
        self.cellmap.update_quadtree()

    def draw(self):
        self.screen.fill(BLACK)
        color = BLACK
        for i in range(CELLMAP_HEIGHT*CELLMAP_WIDTH):

            row = i // CELLMAP_WIDTH
            col = i % CELLMAP_WIDTH

            if self.cellmap.current_map[i] == 1:
                color = WHITE
                pygame.draw.rect(self.screen, color, pygame.Rect((col * CELL_WIDTH, row * CELL_HEIGHT), (CELL_WIDTH, CELL_HEIGHT)), FILL_CELL ^ 1)
           
        if SHOW_QUADTREE:
            self.cellmap.quadtree.draw(self.screen, WHITE)
        
        pygame.display.update()


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()