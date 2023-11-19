import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from pygame.locals import *
import sys


class SeaGame:
    pygame.init()
    running = True
    size = width, height = (500, 660)
    screen = pygame.display.set_mode(size)
    round = 0
    kilp_pos = 'r'
    current_loc = None

    def __init__(self):
        # the sea image
        self.the_sea = pygame.image.load(self.resource_path('sea.png'))
        self.the_sea_loc = self.the_sea.get_rect()
        self.the_sea_loc.center = 300, 330

        # the fish
        self.the_fish = pygame.image.load(self.resource_path('fish.png'))
        self.the_fish_loc = self.the_fish.get_rect()
        self.the_fish_loc.center = 540, 1100
        self.res_the_fish = pygame.transform.scale(self.the_fish, (150, 200))

        # the shark
        self.the_shark = pygame.image.load(self.resource_path('shark.png'))
        self.the_shark_loc = self.the_shark.get_rect()
        self.the_shark_loc.center = 555, 1100
        self.res_the_shark = pygame.transform.scale(self.the_shark, (130, 200))
        self.shark_rect = self.res_the_shark.get_rect()

        # the penguin
        self.the_penguin = pygame.image.load(self.resource_path('penguin.png'))
        self.the_penguin_loc = self.the_penguin.get_rect()
        self.the_penguin_loc.center = 580, 1170
        self.res_the_penguin = pygame.transform.scale(self.the_penguin, (80, 120))
        self.penguin_rect = self.res_the_penguin.get_rect()

        # the kelp
        self.the_kilp = pygame.image.load(self.resource_path('kilp.png'))
        self.the_kilp_loc = self.the_kilp.get_rect()
        self.the_kilp_loc.center = 700, 400
        self.res_the_kilp = pygame.transform.scale(self.the_kilp, (300, 150))

        # lose text
        self.lose_text = pygame.font.Font(self.resource_path('alfont_com_AA-TYPO.otf'), 100).render(f"You Lost.", True, (255, 0, 0))
        self.lose_text_loc = self.lose_text.get_rect()
        self.lose_text_loc.center = 250, 330

    def mainloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                if event.type == KEYDOWN and event.key == K_RIGHT:
                    if self.round == 0:
                        if not self.the_fish_loc[0] > 350:
                            self.the_fish_loc = self.the_fish_loc.move(100, 0)
                    if self.round == 1:
                        if not self.the_shark_loc[0] > 350:
                            self.the_shark_loc = self.the_shark_loc.move(100, 0)
                    if self.round == 2:
                        if not self.the_penguin_loc[0] > 400:
                            self.the_penguin_loc = self.the_penguin_loc.move(100, 0)

                if event.type == KEYDOWN and event.key == K_LEFT:
                    if self.round == 0:
                        if not self.the_fish_loc[0] < 15:
                            self.the_fish_loc = self.the_fish_loc.move(-100, 0)
                    if self.round == 1:
                        if not self.the_shark_loc[0] < 15:
                            self.the_shark_loc = self.the_shark_loc.move(-100, 0)
                    if self.round == 2:
                        if not self.the_penguin_loc[0] < 15:
                            self.the_penguin_loc = self.the_penguin_loc.move(-100, 0)

                if event.type == KEYDOWN and event.key == K_SPACE:
                    if self.round == 0:
                        self.the_fish_loc.center = 540, 1100
                    if self.round == 1:
                        self.the_shark_loc.center = 555, 1100
                    if self.round == 2:
                        self.the_penguin_loc.center = 580, 1170
                    self.round += 1
                    if self.round >= 3:
                        self.round = 0

            if self.the_kilp_loc[1] > 660:
                if self.kilp_pos == 'r':
                    self.kilp_pos = 'l'
                    self.the_kilp_loc.center = 500, 100
                else:
                    self.kilp_pos = 'r'
                    self.the_kilp_loc.center = 700, 100

            self.update_all_objects()

            if self.kilp_pos == 'r':
                print(1, self.current_loc[0], self.the_kilp_loc[0] - 115, self.the_kilp_loc[1], self.current_loc[1] - 140)
                if self.current_loc[0] >= self.the_kilp_loc[0] - 115 and self.the_kilp_loc[1] == self.current_loc[1] - 140:
                    self.you_lost()
            else:
                print(2, self.current_loc[0], self.the_kilp_loc[0] + 240, self.the_kilp_loc[1], self.current_loc[1] - 140)
                if self.current_loc[0] <= self.the_kilp_loc[0] + 240 and self.the_kilp_loc[1] == self.current_loc[1] - 140:
                    self.you_lost()

    def update_all_objects(self):
        self.screen.blit(self.the_sea, self.the_sea_loc)
        if self.round == 0:
            self.screen.blit(self.res_the_fish, self.the_fish_loc)
            self.current_loc = self.the_fish_loc
        if self.round == 1:
            self.screen.blit(self.res_the_shark, self.the_shark_loc)
            self.current_loc = self.the_shark_loc
        if self.round == 2:
            self.screen.blit(self.res_the_penguin, self.the_penguin_loc)
            self.current_loc = self.the_penguin_loc
        self.the_kilp_loc = self.the_kilp_loc.move(0, 1)
        self.screen.blit(self.res_the_kilp, self.the_kilp_loc)
        pygame.display.update()

    def you_lost(self):
        self.screen.blit(self.lose_text, self.lose_text_loc)
        self.kilp_pos = 'l'
        self.the_kilp_loc.center = 500, 100
        pygame.display.update()
        pygame.time.delay(2000)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    SeaGame().mainloop()