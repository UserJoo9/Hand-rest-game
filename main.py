import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from pygame.locals import *
import sys
from tkinter import messagebox
from threading import Thread
import serial
import serial.tools.list_ports

if not os.path.exists('cont.txt'):
    open('cont.txt', 'w').write("USB-SERIAL CH340\n"
                                "Silicon Labs CP210x")
try:
    supportedBoardsModel = open('cont.txt', 'r').read().split("\n")
    if "" in supportedBoardsModel:
        messagebox.showerror("Hierarchy error!", "Remove empty lines from 'cont.txt' file content!")
        exit()
except:
    messagebox.showerror("Hierarchy error!", "Adapt or fix the hierarchy of 'cont.txt' file content!")
    exit()
connectedBoard = None
isConnected = False


def start_connection():
    global links, boardConnected, MCU, connectedBoard, isConnected
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if any(one in p.description for one in supportedBoardsModel):
            port = p.description
            connectedBoard = port
            com = port.split("(")[-1][:-1]
            try:
                MCU = serial.Serial(port=com, baudrate=9600)
                isConnected = True
                MCU.close()
                MCU.open()
            except:
                pass
            boardConnected = True
            return "Connected"


start_connection()


def check_connectivity():
    global isConnected, MCU
    while 1:
        pygame.time.delay(100)
        ports = list(serial.tools.list_ports.comports())
        isConnected = False
        for p in ports:
            if any(one in p.description for one in supportedBoardsModel):
                isConnected = True


Thread(target=check_connectivity, daemon=True).start()


# check live sensor value
def active_press():
    global stillPressed, MCU, general_value, controller_nav
    while 1:
        pygame.time.delay(50)
        try:
            general_value = int(MCU.read().decode().strip())
        except:
            if not isConnected:
                try:
                    MCU.close()
                except:
                    pass
                start_connection()


Thread(target=active_press, daemon=True).start()


class SeaGame:
    pygame.init()
    running = True
    size = width, height = (500, 800)
    screen = pygame.display.set_mode(size)
    round = 0
    kilp_pos = 'r'
    retry = False
    new_round = False
    current_loc = None
    r_kilp_width = 520


    def __init__(self):
        self.set_configuration()
        pygame.display.set_caption(self.applicationName)

        # the sea image
        self.the_sea = pygame.image.load(self.resource_path('sea.png'))
        self.the_sea_loc = self.the_sea.get_rect()
        self.the_sea_loc.center = 220, 330

        # the fish
        self.the_fish = pygame.image.load(self.resource_path('fish.png'))
        self.the_fish_loc = self.the_fish.get_rect()
        self.the_fish_loc.center = 220, 1000
        self.res_the_fish = pygame.transform.scale(self.the_fish, (250, 300))

        # the shark
        self.the_shark = pygame.image.load(self.resource_path('shark.png'))
        self.the_shark_loc = self.the_shark.get_rect()
        self.the_shark_loc.center = 220, 1000
        self.res_the_shark = pygame.transform.scale(self.the_shark, (250, 300))
        self.shark_rect = self.res_the_shark.get_rect()

        # the penguin
        self.the_penguin = pygame.image.load(self.resource_path('penguin.png'))
        self.the_penguin_loc = self.the_penguin.get_rect()
        self.the_penguin_loc.center = 220, 1000
        self.res_the_penguin = pygame.transform.scale(self.the_penguin, (200, 250))
        self.penguin_rect = self.res_the_penguin.get_rect()

        # the kelp 1
        self.the_kilp = pygame.image.load(self.resource_path('kilp1.png'))
        self.the_kilp_loc = self.the_kilp.get_rect()
        self.the_kilp_loc.center = self.r_kilp_width, 400
        self.res_the_kilp = pygame.transform.scale(self.the_kilp, (240, 120))

        # the kelp 2
        self.the_kilp2 = pygame.image.load(self.resource_path('kilp2.png'))
        self.the_kilp2_loc = self.the_kilp2.get_rect()
        self.the_kilp2_loc.center = self.r_kilp_width, 400
        self.res_the_kilp2 = pygame.transform.scale(self.the_kilp2, (240, 120))

        # the kelp 3
        self.the_kilp3 = pygame.image.load(self.resource_path('kilp3.png'))
        self.the_kilp3_loc = self.the_kilp3.get_rect()
        self.the_kilp3_loc.center = self.r_kilp_width, 400
        self.res_the_kilp3 = pygame.transform.scale(self.the_kilp3, (240, 120))

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
        self.round_text = pygame.font.Font(self.resource_path('alfont_com_AA-TYPO.otf'), 100).render(f"Round {self.round + 1}", True, (0, 255, 0))
        self.round_text_loc = self.round_text.get_rect()
        self.round_text_loc.center = 250, 500

        Thread(target=self.round1, daemon=True).start()

    def set_configuration(self):
        if not os.path.exists('CONFIG.txt'):
            open('CONFIG.txt', 'w').write("Character speed: 3\n"
                                          "Round time: 60\n"
                                          "Game name: Hand rest game")
        try:
            for i, v in enumerate(open("CONFIG.txt", "r").read().split("\n")):
                if i == 0:
                    self.obstacle_speed = int(v.split(": ")[1])
                    if self.obstacle_speed > 3:
                        if messagebox.askokcancel("Configuration error!", "the character speed is too much\n"
                                                                          "edit fields in 'CONFIG.txt' file!\n"
                                                                          "or click 'OK' to reset it.", icon='error'):
                            os.remove("CONFIG.txt")
                            self.set_configuration()
                        else:
                            exit()
                if i == 1:
                    self.round_time = int(v.split(": ")[1])
                    if self.round_time < 25:
                        if messagebox.askokcancel("Configuration error!", "the round time is too short\n"
                                                                          "edit fields in 'CONFIG.txt' file!\n"
                                                                          "or click 'OK' to reset it.", icon='error'):
                            os.remove("CONFIG.txt")
                            self.set_configuration()
                        else:
                            exit()
                if i == 2:
                    self.applicationName = v.split(": ")[1]
        except:
            if messagebox.askokcancel("Configuration error!", "Check invalid fields in 'CONFIG.txt' file!\n"
                                                              "or click 'OK' to reset it.", icon='error'):
                os.remove("CONFIG.txt")
                self.set_configuration()
            else:
                exit()

    def mainloop(self):
        while self.running:
            pygame.time.delay(10)
            if not self.new_round:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        self.running = False
                    if (event.type == KEYDOWN and event.key == K_RIGHT) or any(num in general_value for num in [2, 4, 6]):
                        # print(self.the_fish_loc[0])
                        if self.round == 1 and general_value == 2:
                            if not self.the_fish_loc[0] > 112:
                                self.the_fish_loc = self.the_fish_loc.move(135, 0)
                        if self.round == 2 and general_value == 4:
                            if not self.the_shark_loc[0] > 142:
                                self.the_shark_loc = self.the_shark_loc.move(135, 0)
                        if self.round == 3 and general_value == 6:
                            if not self.the_penguin_loc[0] > 163:
                                self.the_penguin_loc = self.the_penguin_loc.move(135, 0)

                    if (event.type == KEYDOWN and event.key == K_LEFT) or any(num in general_value for num in [1, 3, 5]):
                        # print(self.the_fish_loc[0])
                        if self.round == 1 and general_value == 1:
                            if not self.the_fish_loc[0] < 112:
                                self.the_fish_loc = self.the_fish_loc.move(-135, 0)
                        if self.round == 2 and general_value == 3:
                            if not self.the_shark_loc[0] < 142:
                                self.the_shark_loc = self.the_shark_loc.move(-135, 0)
                        if self.round == 3 and general_value == 5:
                            if not self.the_penguin_loc[0] < 163:
                                self.the_penguin_loc = self.the_penguin_loc.move(-135, 0)

                    if (event.type == KEYDOWN and event.key == K_SPACE) or general_value == 0:
                        self.the_fish_loc.center = 485, 1120
                        self.the_shark_loc.center = 515, 1120
                        self.the_penguin_loc.center = 535, 1180
                        pygame.display.update()

                self.update_all_objects()

                if self.kilp_pos == 'r':
                    if self.round == 1:
                        if self.current_loc[0] >= self.the_kilp_loc[0] - 130 and self.the_kilp_loc[1] >= self.current_loc[1] - 110:
                            self.you_lost()
                    if self.round == 2:
                        if (self.current_loc[0] >= self.the_kilp2_loc[0] - 115 or self.current_loc[0] == 142) and self.the_kilp2_loc[1] >= self.current_loc[1] - 90:
                            self.you_lost()
                    # print(1, self.current_loc[0], self.the_kilp3_loc[0] - 115, self.the_kilp3_loc[1], self.current_loc[1] - 100)
                    if self.round == 3:
                        if self.current_loc[0] >= self.the_kilp3_loc[0] - 115 and self.the_kilp3_loc[1] >= self.current_loc[1] - 100:
                            self.you_lost()
                else:
                    if self.round == 1:
                        if (self.current_loc[0] == -23 or self.current_loc[0] == 112) and self.the_kilp_loc[1] >= self.current_loc[1] - 110:
                            self.you_lost()
                    if self.round == 2:
                        if (self.current_loc[0] <= self.the_kilp2_loc[0] or self.current_loc[0] == 142) and self.the_kilp2_loc[1] >= self.current_loc[1] - 90:
                            self.you_lost()
                    # print(2, self.current_loc[0], self.the_kilp3_loc[0] + 18, self.the_kilp3_loc[1], self.current_loc[1] - 100)
                    if self.round == 3:
                        if (self.current_loc[0] <= self.the_kilp3_loc[0] + 18 or self.current_loc[0] == 163) and self.the_kilp3_loc[1] >= self.current_loc[1] - 100:
                            self.you_lost()

                if any(l > 750 for l in [self.the_kilp_loc[1], self.the_kilp2_loc[1], self.the_kilp3_loc[1]]):
                    if self.kilp_pos == 'r':
                        self.kilp_pos = 'l'
                        self.the_kilp_loc.center = 280, 100
                        self.the_kilp2_loc.center = 280, 100
                        self.the_kilp3_loc.center = 280, 100
                    else:
                        self.kilp_pos = 'r'
                        self.the_kilp_loc.center = self.r_kilp_width, 100
                        self.the_kilp2_loc.center = self.r_kilp_width, 100
                        self.the_kilp3_loc.center = self.r_kilp_width, 100

    def round1(self):
        MCU.write('a'.encode())
        self.active_new_round()
        rt = self.round_time
        while rt >= 1:
            pygame.time.delay(1000)
            if self.retry:
                rt = self.round_time
            else:
                rt -= 1
        Thread(target=self.round2, daemon=True).start()

    def round2(self):
        MCU.write('b'.encode())
        self.active_new_round()
        rt = self.round_time
        while rt >= 1:
            pygame.time.delay(1000)
            if self.retry:
                rt = self.round_time
            else:
                rt -= 1
        Thread(target=self.round3, daemon=True).start()

    def round3(self):
        MCU.write('c'.encode())
        self.active_new_round()
        rt = self.round_time
        while rt >= 1:
            pygame.time.delay(1000)
            if self.retry:
                rt = self.round_time
            else:
                rt -= 1
        self.you_win()

    def update_all_objects(self):
        self.screen.blit(self.the_sea, self.the_sea_loc)
        if self.round == 1:
            self.screen.blit(self.res_the_fish, self.the_fish_loc)
            self.current_loc = self.the_fish_loc
            self.screen.blit(self.res_the_kilp, self.the_kilp_loc)
            self.the_kilp_loc = self.the_kilp_loc.move(0, self.obstacle_speed)
            # self.screen.blit(pygame.transform.rotate(self.screen, 270), (0, 0))
        if self.round == 2:
            self.screen.blit(self.res_the_shark, self.the_shark_loc)
            self.current_loc = self.the_shark_loc
            self.screen.blit(self.res_the_kilp2, self.the_kilp2_loc)
            self.the_kilp2_loc = self.the_kilp2_loc.move(0, self.obstacle_speed)
        if self.round == 3:
            self.screen.blit(self.res_the_penguin, self.the_penguin_loc)
            self.current_loc = self.the_penguin_loc
            self.screen.blit(self.res_the_kilp3, self.the_kilp3_loc)
            self.the_kilp3_loc = self.the_kilp3_loc.move(0, self.obstacle_speed)
        pygame.display.update()

    def active_new_round(self):
        self.new_round = True
        if self.round == 0:
            self.screen.blit(self.res_updown, self.updown_loc)
            pygame.display.update()
            self.the_fish_loc.center = 485, 1120
        if self.round == 1:
            self.screen.blit(self.res_flip, self.flip_loc)
            pygame.display.update()
            self.the_shark_loc.center = 515, 1120
        if self.round == 2:
            self.screen.blit(self.res_leftright, self.leftright_loc)
            pygame.display.update()
            self.the_penguin_loc.center = 535, 1180
        self.round += 1
        self.round_text = pygame.font.Font(self.resource_path('alfont_com_AA-TYPO.otf'), 100).render(f"Round {self.round}", True, (0, 255, 0))
        self.screen.blit(self.round_text, self.round_text_loc)
        pygame.display.update()
        pygame.time.delay(3000)
        self.kilp_pos = 'r'
        self.the_kilp_loc.center = self.r_kilp_width, 100
        self.the_kilp2_loc.center = self.r_kilp_width, 100
        self.the_kilp3_loc.center = self.r_kilp_width, 100
        self.update_all_objects()
        self.new_round = False

    def you_lost(self):
        self.screen.blit(self.lose_text, self.lose_text_loc)
        self.retry = True
        self.kilp_pos = 'r'
        self.the_kilp_loc.center = self.r_kilp_width, 100
        self.the_kilp2_loc.center = self.r_kilp_width, 100
        self.the_kilp3_loc.center = self.r_kilp_width, 100
        if self.round == 0:
            self.the_fish_loc.center = 350, 1020
        if self.round == 1:
            self.the_shark_loc.center = 380, 1020
        if self.round == 2:
            self.the_penguin_loc.center = 400, 1080
        pygame.display.update()
        pygame.time.delay(2000)
        self.retry = False

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