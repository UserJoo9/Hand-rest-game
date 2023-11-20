import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from pygame.locals import *
import sys
from tkinter import messagebox
from threading import Thread


class SeaGame:
    pygame.init()
    running = True
    size = width, height = (500, 660)
    screen = pygame.display.set_mode(size)
    round = 0
    kilp_pos = 'r'
    retry = False
    new_round = False
    current_loc = None
    if not os.path.exists('CONFIG.txt'):
        open('CONFIG.txt', 'w').write("Character speed: 100\n"
                                      "Obstacle speed: 5\n"
                                      "Round time: 30\n")
    try:
        for i, v in enumerate(open("CONFIG.txt", "r").read().split("\n")):
            if i == 0:
                character_speed = int(v.split(": ")[1])
            if i == 1:
                obstacle_speed = float(v.split(": ")[1])
            if i == 2:
                round_time = int(v.split(": ")[1])
    except:
        if messagebox.askokcancel("Configuration error!", "Check invalid fields in 'CONFIG.txt' file!\n"
                                                       "or click 'OK' to reset it.", icon='error'):
            open('CONFIG.txt', 'w').write("Character speed: 100\n"
                                          "Obstacle speed: 1\n"
                                          "Round time: 30\n")
        else:
            exit()

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

        # r1 guide
        self.updown = pygame.image.load(self.resource_path('updown.png'))
        self.updown_loc = self.updown.get_rect()
        self.updown_loc.center = self.width / 2 + 10, 250
        self.res_updown = pygame.transform.scale(self.updown, (500, 270))

        # r2 guide
        self.flip = pygame.image.load(self.resource_path('flip.png'))
        self.flip_loc = self.flip.get_rect()
        self.flip_loc.center = self.width / 2 + 10, 250
        self.res_flip = pygame.transform.scale(self.flip, (500, 270))

        # r2 guide
        self.leftright = pygame.image.load(self.resource_path('leftright.png'))
        self.leftright_loc = self.leftright.get_rect()
        self.leftright_loc.center = self.width / 2 + 10, 250
        self.res_leftright = pygame.transform.scale(self.leftright, (500, 270))

        # lose text
        self.lose_text = pygame.font.Font(self.resource_path('alfont_com_AA-TYPO.otf'), 100).render(f"You Lost.", True, (255, 0, 0))
        self.lose_text_loc = self.lose_text.get_rect()
        self.lose_text_loc.center = 250, 330

        # win text
        self.win_text = pygame.font.Font(self.resource_path('alfont_com_AA-TYPO.otf'), 100).render(f"You Win.", True, (0, 255, 0))
        self.win_text_loc = self.win_text.get_rect()
        self.win_text_loc.center = 250, 330

        # round text
        self.round_text = pygame.font.Font(self.resource_path('alfont_com_AA-TYPO.otf'), 100).render(f"Round {self.round + 1}.", True, (0, 255, 0))
        self.round_text_loc = self.round_text.get_rect()
        self.round_text_loc.center = 250, 500

        Thread(target=self.round1, daemon=True).start()

    def mainloop(self):
        while self.running:
            pygame.time.delay(10)
            if not self.new_round:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.running = False
                    if event.type == KEYDOWN and event.key == K_RIGHT:
                        if self.round == 1:
                            if not self.the_fish_loc[0] > 350:
                                self.the_fish_loc = self.the_fish_loc.move(self.character_speed, 0)
                        if self.round == 2:
                            if not self.the_shark_loc[0] > 350:
                                self.the_shark_loc = self.the_shark_loc.move(self.character_speed, 0)
                        if self.round == 3:
                            if not self.the_penguin_loc[0] > 400:
                                self.the_penguin_loc = self.the_penguin_loc.move(self.character_speed, 0)

                    if event.type == KEYDOWN and event.key == K_LEFT:
                        if self.round == 1:
                            if not self.the_fish_loc[0] < 15:
                                self.the_fish_loc = self.the_fish_loc.move(-self.character_speed, 0)
                        if self.round == 2:
                            if not self.the_shark_loc[0] < 15:
                                self.the_shark_loc = self.the_shark_loc.move(-self.character_speed, 0)
                        if self.round == 3:
                            if not self.the_penguin_loc[0] < 15:
                                self.the_penguin_loc = self.the_penguin_loc.move(-self.character_speed, 0)

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
                    if self.current_loc[0] >= self.the_kilp_loc[0] - 115 and self.the_kilp_loc[1] >= self.current_loc[1] - 140:
                        self.you_lost()
                else:
                    print(2, self.current_loc[0], self.the_kilp_loc[0] + 240, self.the_kilp_loc[1], self.current_loc[1] - 140)
                    if self.current_loc[0] <= self.the_kilp_loc[0] + 240 and self.the_kilp_loc[1] >= self.current_loc[1] - 140:
                        self.you_lost()


    def round1(self):
        self.active_new_round()
        rt = self.round_time
        while rt >= 1:
            pygame.time.delay(1000)
            if self.retry:
                rt = self.round_time
                self.retry = False
            else:
                rt -= 1
        Thread(target=self.round2, daemon=True).start()

    def round2(self):
        self.active_new_round()
        rt = self.round_time
        while rt >= 1:
            pygame.time.delay(1000)
            if self.retry:
                rt = self.round_time
                self.retry = False
            else:
                rt -= 1
        Thread(target=self.round3, daemon=True).start()

    def round3(self):
        self.active_new_round()
        rt = self.round_time
        while rt >= 1:
            pygame.time.delay(1000)
            if self.retry:
                rt = self.round_time
                self.retry = False
            else:
                rt -= 1
        self.you_win()

    def update_all_objects(self):
        self.screen.blit(self.the_sea, self.the_sea_loc)
        if self.round == 1:
            self.screen.blit(self.res_the_fish, self.the_fish_loc)
            self.current_loc = self.the_fish_loc
        if self.round == 2:
            self.screen.blit(self.res_the_shark, self.the_shark_loc)
            self.current_loc = self.the_shark_loc
        if self.round == 3:
            self.screen.blit(self.res_the_penguin, self.the_penguin_loc)
            self.current_loc = self.the_penguin_loc
        self.the_kilp_loc = self.the_kilp_loc.move(0, self.obstacle_speed)
        self.screen.blit(self.res_the_kilp, self.the_kilp_loc)
        pygame.display.update()

    def active_new_round(self):
        self.new_round = True
        if self.round == 0:
            self.screen.blit(self.res_updown, self.updown_loc)
            pygame.display.update()
            self.the_fish_loc.center = 540, 1100
        if self.round == 1:
            self.screen.blit(self.res_flip, self.flip_loc)
            pygame.display.update()
            self.the_shark_loc.center = 555, 1100
        if self.round == 2:
            self.screen.blit(self.res_leftright, self.leftright_loc)
            pygame.display.update()
            self.the_penguin_loc.center = 580, 1170
        self.round += 1
        self.round_text = pygame.font.Font(self.resource_path('alfont_com_AA-TYPO.otf'), 100).render(f"Round {self.round}.", True, (0, 255, 0))
        self.screen.blit(self.round_text, self.round_text_loc)
        pygame.display.update()
        pygame.time.delay(3000)
        self.kilp_pos = 'l'
        self.the_kilp_loc.center = 500, 100
        self.update_all_objects()
        self.new_round = False

    def you_lost(self):
        self.screen.blit(self.lose_text, self.lose_text_loc)
        self.kilp_pos = 'l'
        self.retry = True
        self.the_kilp_loc.center = 500, 100
        if self.round == 0:
            self.the_fish_loc.center = 540, 1100
        if self.round == 1:
            self.the_shark_loc.center = 555, 1100
        if self.round == 2:
            self.the_penguin_loc.center = 580, 1170
        pygame.display.update()
        pygame.time.delay(2000)

    def you_win(self):
        self.new_round = True
        self.screen.blit(self.win_text, self.win_text_loc)
        pygame.display.update()
        pygame.time.delay(2000)
        self.running = False
        pygame.quit()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    SeaGame().mainloop()