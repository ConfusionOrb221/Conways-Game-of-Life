import sys
import pygame as pg
import ctypes
import time
import random
class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

class Menu(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game'
        self.buttons = []
    def cleanup(self):
        print('Cleaning up Menu Stuff')
    def startup(self):
        print('Starting up Menu State Stuff')
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Menu State Keydown')
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((255,255,255))

class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pg.display.set_mode(self.size)
        self.clock = pg.time.Clock()
        self.gridsize = 40
        self.width = self.size[0] / 1.6
        self.height = self.size[1] / 1.2
        self.white = 0,0,0
        self.black = 255,255,255
        self.grid = []
        self.objects = []
        self.gridcopy = []
        self.fps_string = str(self.fps)
        self.gens = 1
        self.gridwidth = (self.width / self.gridsize) - 5
        self.gridheight = (self.height / self.gridsize) - 5
        self.start = pg.Rect(0, self.size[1] - 100, 100, 100)
        self.stop = pg.Rect(150, self.size[1] - 100, 100, 100)
        self.reset = pg.Rect(300, self.size[1] - 100, 100, 100)
        self.gliderGun = pg.Rect(self.width, 0, 200, 100)
        self.pulsar = pg.Rect(self.width, 200, 200, 100)
        self.DieHard = pg.Rect(self.width, 400, 200, 100)
        self.random = pg.Rect(self.width, 600, 200, 100)
        self.generation = pg.Rect(self.width - 250, self.height, 200, 50)
        self.fps_box = pg.Rect(self.width, self.height, 150, 50)
        self.button = False
        self.font = pg.font.Font('freesansbold.ttf', 32) 
        for row in range(self.gridsize):
            self.grid.append([])
            for column in range(self.gridsize):
                self.grid[row].append(False)
        self.objects = [x[:] for x in self.grid]
        self.start_text = self.font.render('Start', True, self.black)
        self.stop_text = self.font.render('Stop', True, self.black)
        self.reset_text = self.font.render('Reset', True, self.black)
        self.gliderGun_text = self.font.render('Glider Gun', True, self.black)
        self.pulsar_text = self.font.render('Pulsar', True, self.black)
        self.DieHard_text = self.font.render('Die Hard', True, self.black)
        self.random_text = self.font.render('Random', True, self.black)
        self.input = False
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
    def flip_state(self):
        self.state.done = False
        previous,self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous
    def update(self, dt):
        if self.button == True:
            self.gridcopy = [x[:] for x in self.grid]
            for row in range(self.gridsize):
                for column in range(self.gridsize):
                    neighbors = 0
                    column1 = column + 1
                    row1 = row + 1
                    if (column == 0 or column == self.gridsize - 1) or (row == 0 or row == self.gridsize - 1):
                        self.gridcopy[row][column] = 0
                        continue
                    else:
                        if self.grid[row][column1] == 1:
                            neighbors+=1
                        if self.grid[row][column-1] == 1:
                            neighbors+=1
                        if self.grid[row1][column] == 1:
                            neighbors+=1
                        if self.grid[row1][column1] == 1:
                            neighbors+=1
                        if self.grid[row1][column-1] == 1:
                            neighbors+=1
                        if self.grid[row-1][column-1] == 1:
                            neighbors+=1
                        if self.grid[row-1][column1] == 1:
                            neighbors+=1
                        if self.grid[row-1][column] == 1:
                            neighbors+=1
                        if self.grid[row][column] == 1:
                            if neighbors == 2 or neighbors == 3:
                                self.gridcopy[row][column] = True
                            else:
                                self.gridcopy[row][column] = False
                        else:
                            if neighbors == 3:
                                self.gridcopy[row][column] = True
            self.grid = self.gridcopy
            self.gens += 1
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if self.input:
                    if event.key == pg.K_RETURN:
                        self.fps = int(self.fps_string)
                    elif event.key == pg.K_BACKSPACE:
                        self.fps_string = self.fps_string[:-1]
                    else:
                        self.fps_string += event.unicode
            elif event.type == pg.MOUSEBUTTONUP:
                if self.fps_box.collidepoint(pg.mouse.get_pos()):
                    self.input = True
                else:
                    self.input = False
                if self.start.collidepoint(pg.mouse.get_pos()):
                    self.button = True
                    break
                if self.stop.collidepoint(pg.mouse.get_pos()):
                    self.button = False
                    break
                if self.reset.collidepoint(pg.mouse.get_pos()):
                    self.button = False
                    self.gens = 1
                    self.resetGrid()
                if not self.button:
                    if self.gliderGun.collidepoint(pg.mouse.get_pos()):
                        self.button = False
                        self.gens = 1
                        self.resetGrid()
                        self.createGun()
                    elif self.pulsar.collidepoint(pg.mouse.get_pos()):
                        self.button = False
                        self.gens = 1
                        self.resetGrid()
                        self.createPulsar()
                    elif self.DieHard.collidepoint(pg.mouse.get_pos()):
                        self.button = False
                        self.gens = 1
                        self.resetGrid()
                        self.createDieHard()
                    elif self.random.collidepoint(pg.mouse.get_pos()):
                        self.button = False
                        self.gens = 1
                        self.resetGrid()
                        self.createRandom()
                    else:
                        for row in range(self.gridsize):
                            for column in range(self.gridsize):
                                if self.objects[row][column].collidepoint(pg.mouse.get_pos()):
                                    self.grid[row][column] = not self.grid[row][column]
            self.state.get_event(event)
    def createGun(self):
        self.grid[5][1] = True
        self.grid[6][1] = True
        self.grid[5][2] = True
        self.grid[6][2] = True
        self.grid[3][13] = True
        self.grid[3][14] = True
        self.grid[4][12] = True
        self.grid[5][11] = True
        self.grid[6][11] = True
        self.grid[7][11] = True
        self.grid[8][12] = True
        self.grid[9][13] = True
        self.grid[9][14] = True
        self.grid[6][15] = True
        self.grid[4][16] = True
        self.grid[8][16] = True
        self.grid[5][17] = True
        self.grid[6][17] = True
        self.grid[7][17] = True
        self.grid[6][18] = True
        self.grid[3][21] = True
        self.grid[4][21] = True
        self.grid[5][21] = True
        self.grid[3][22] = True
        self.grid[4][22] = True
        self.grid[5][22] = True
        self.grid[2][23] = True
        self.grid[6][23] = True
        self.grid[1][25] = True
        self.grid[2][25] = True
        self.grid[6][25] = True
        self.grid[7][25] = True
        self.grid[3][35] = True
        self.grid[3][36] = True
        self.grid[4][35] = True
        self.grid[4][36] = True
    def createPulsar(self):
        self.grid[3][5] = True
        self.grid[3][6] = True
        self.grid[3][12] = True
        self.grid[3][13] = True
        self.grid[4][6] = True
        self.grid[4][7] = True
        self.grid[4][11] = True
        self.grid[4][12] = True
        self.grid[5][3] = True
        self.grid[5][6] = True
        self.grid[5][8] = True
        self.grid[5][10] = True
        self.grid[5][12] = True
        self.grid[6][3] = True
        self.grid[6][4] = True
        self.grid[6][5] = True
        self.grid[6][7] = True
        self.grid[6][8] = True
        self.grid[6][10] = True
        self.grid[6][11] = True
        self.grid[6][13] = True
        self.grid[6][14] = True
        self.grid[7][4] = True
        self.grid[7][6] = True
        self.grid[7][8] = True
        self.grid[7][10] = True
        self.grid[7][12] = True
        self.grid[7][14] = True
        self.grid[8][5] = True
        self.grid[8][6] = True
        self.grid[8][7] = True
        self.grid[8][11] = True
        self.grid[8][12] = True
        self.grid[8][13] = True
        self.grid[10][5] = True
        self.grid[10][6] = True
        self.grid[10][7] = True
        self.grid[10][11] = True
        self.grid[10][12] = True
        self.grid[10][13] = True
        self.grid[11][4] = True
        self.grid[11][6] = True
        self.grid[11][8] = True
        self.grid[11][10] = True
        self.grid[11][12] = True
        self.grid[11][14] = True
        self.grid[12][3] = True
        self.grid[12][4] = True
        self.grid[12][5] = True
        self.grid[12][7] = True
        self.grid[12][8] = True
        self.grid[12][10] = True
        self.grid[12][11] = True
        self.grid[12][13] = True
        self.grid[12][14] = True
        self.grid[13][3] = True
        self.grid[13][6] = True
        self.grid[13][8] = True
        self.grid[13][10] = True
        self.grid[13][12] = True
        self.grid[14][6] = True
        self.grid[14][7] = True
        self.grid[14][11] = True
        self.grid[14][12] = True
        self.grid[15][6] = True
        self.grid[15][5] = True
        self.grid[15][12] = True
        self.grid[15][13] = True
        self.grid[6][15] = True
        self.grid[5][15] = True
        self.grid[12][15] = True
        self.grid[13][15] = True
    def createDieHard(self):
        self.grid[5][4] = True
        self.grid[5][5] = True
        self.grid[6][5] = True
        self.grid[6][9] = True
        self.grid[6][10] = True
        self.grid[6][11] = True
        self.grid[4][10] = True
    def createRandom(self):
        for row in range(self.gridsize):
            for column in range(self.gridsize):
                if (column == 0 or column == self.gridsize - 1) or (row == 0 or row == self.gridsize - 1):
                        self.grid[row][column] = 0
                        continue
                else:
                    if random.getrandbits(1):
                        self.grid[row][column] = random.getrandbits(1)
    def resetGrid(self):
        for row in range(self.gridsize):
            for column in range(self.gridsize):
                self.grid[row][column] = 0
    def drawGrid(self):
        fill = 0
        for row in range(self.gridsize):
            for column in range(self.gridsize):
                if self.grid[row][column] == False:
                    fill = 1
                elif self.grid[row][column] == True:
                    fill = 0
                rect = pg.Rect((self.gridwidth + 5) * column, (self.gridheight + 5) * row, int(self.gridwidth), int(self.gridheight))
                self.objects[row][column] = rect
                pg.draw.rect(self.screen, self.white, rect, fill)
    def drawMenu(self, screen):
        pg.draw.rect(self.screen, self.white, self.start, 0)
        pg.draw.rect(self.screen, self.white, self.stop, 0)
        pg.draw.rect(self.screen, self.white, self.reset, 0)
        pg.draw.rect(self.screen, self.white, self.generation, 0)
        pg.draw.rect(self.screen, self.white, self.gliderGun, 0)
        pg.draw.rect(self.screen, self.white, self.pulsar, 0)
        pg.draw.rect(self.screen, self.white, self.fps_box, 1)
        pg.draw.rect(self.screen, self.white, self.DieHard, 0)
        pg.draw.rect(self.screen, self.white, self.random, 0)
        number = self.font.render(f'{self.gens}', True, self.black)
        self.fps_text = self.font.render(f'{self.fps_string}', True, self.white, None)
        self.screen.blit(self.gliderGun_text, (self.gliderGun.x + 10, self.gliderGun.y + self.gliderGun.height / 3.5))
        self.screen.blit(self.fps_text, (self.fps_box.x + self.fps_box.width - self.fps_text.get_rect().width, self.fps_box.y + self.fps_box.height / 3.5))
        self.screen.blit(number, self.generation)
        self.screen.blit(self.pulsar_text, (self.pulsar.x + 10, self.pulsar.y + self.pulsar.height / 3.5))
        self.screen.blit(self.start_text, (self.start.x + 10, self.start.y + self.start.height / 3.5))
        self.screen.blit(self.stop_text, (self.stop.x + 10, self.stop.y + self.stop.height / 3.5))
        self.screen.blit(self.reset_text, (self.reset.x + 5, self.reset.y + self.reset.height / 3.5))
        self.screen.blit(self.DieHard_text, (self.DieHard.x + 10, self.DieHard.y + self.DieHard.height / 3.5))
        self.screen.blit(self.random_text, (self.random.x + 10, self.random.y + self.random.height / 3.5))
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps) / 1000.0
            self.event_loop()
            self.update(delta_time)
            self.drawGrid()
            self.drawMenu(self.size)
            pg.display.update()

if __name__ == "__main__":
    settings = {
        'size': (int(ctypes.windll.user32.GetSystemMetrics(0) / 1.5 ), int(ctypes.windll.user32.GetSystemMetrics(1) / 1.5) ),
        'fps': 60
    }
    
    pg.init()
    app = Control(**settings)

    state_dict = {
        'menu': Menu()
    }

    app.setup_states(state_dict, 'menu')
    app.main_game_loop()
    pg.quit()
    sys.exit()