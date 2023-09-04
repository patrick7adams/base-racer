import math
import pygame, sys
from random import randint, choice
from typing import Tuple, List
from pygame.locals import QUIT
# Types of conversions necessary:
# int to bin, bin to int, hex to int, int to hex, bin to hex, hex to bin

str_int_dict = {str(i):i for i in range(10)}
str_int_dict.update({letter:val for letter,val in zip('abcdefghijklmnopqrstuvwxyz', range(10, 36))})
int_str_dict = {str(i):k for k, i in str_int_dict.items()}

def base_convert(A: str, baseA: int, baseB: int) -> str:
    """ Converts the base of the number to base. """
    num_int = sum(str_int_dict[num]*baseA**(len(A)-1-i) for i, num in enumerate(A))
    try:
        num_digits = math.floor(math.log(num_int, baseB))+1
    except:
        num_digits = 1
    final_val = ''
    for i in range(num_digits, 0, -1):
      final_val = int_str_dict[str(num_int % baseB)] + final_val
      num_int //= baseB
    return final_val

color_white = (255, 255, 255)
color_orange = (255, 140, 0)
color_red = (200, 0, 0)

res_x = 1280
res_y = 720
global frame_count

pygame.init()
screen = pygame.display.set_mode((res_x, res_y))
pygame.display.set_caption('Base Racer')
clock = pygame.time.Clock()

ticker_width = 75
ticker_x_range = (100, 1000)
ticker_y_val = 570

button_dim = (200, 60)
button_center = (535, 320)
low_button_center = (535, 650)

exit_button_loc = (545, 380)
restart_button_loc = (545, 310)

on_ticker = pygame.transform.scale(pygame.image.load('resources/on.png'), (ticker_width, ticker_width))
off_ticker = pygame.transform.scale(pygame.image.load('resources/off.png'), (ticker_width, ticker_width))
start_button = pygame.transform.scale(pygame.image.load('resources/start_button.png'), button_dim)
submit_button = pygame.transform.scale(pygame.image.load('resources/submit_button.png'), button_dim)
exit_button = pygame.transform.scale(pygame.image.load('resources/exit_button.png'), button_dim)
background = pygame.transform.scale(pygame.image.load('resources/background.png'), (res_x, res_y))
slider_outline = pygame.transform.scale(pygame.image.load('resources/slider_outline.png'), (200, 80))
bin_slide = pygame.transform.scale(pygame.image.load('resources/bin_slide.png'), (80, 80))
hex_slide = pygame.transform.scale(pygame.image.load('resources/hex_slide.png'), (80, 80))

slider_loc = (100, 100)
slider_rect = pygame.Rect(*slider_loc, 200, 80)

exit_button_rect = pygame.Rect(*exit_button_loc, *button_dim)
restart_button_rect = pygame.Rect(*restart_button_loc, *button_dim)

start_button_rect = pygame.Rect(*button_center, *button_dim)
submit_button_rect = pygame.Rect(*low_button_center, *button_dim)

type_font = pygame.font.Font('resources/ERASBD.TTF', 32)
big_font = pygame.font.Font('resources/ERASBD.TTF', 64)

race = type_font.render("Ready to race?", True, color_white)

class Ticker:
    ticker_list: List
    int_val: int
    bin_val: str
    output_base: int
    
    def __init__(self, loc: Tuple[int, int], index: int):
        self.loc = loc
        self.index = index
        self.on = False
        self.sprite = off_ticker
        rect_loc = (loc[0]-10, loc[1]-20)
        self.rect = pygame.Rect(*rect_loc, ticker_width, ticker_width)
        
    def click(self):
        ''' Click event. Flips to other sprite and changes bin_val accordingly. '''
        if self.on == True:
            self.on = False
            Ticker.bin_val = Ticker.bin_val[:self.index] + '0' + Ticker.bin_val[self.index+1:]
            self.sprite = off_ticker
        else:
            self.on = True
            Ticker.bin_val = Ticker.bin_val[:self.index] + '1' + Ticker.bin_val[self.index+1:]
            self.sprite = on_ticker
        Ticker.int_val = Ticker.get_total_value()
        
    @staticmethod
    def reset():
        for ticker in Ticker.ticker_list:
            if ticker.on == True: ticker.click()
        
    @staticmethod
    def get_total_value() -> str:
        return base_convert(Ticker.bin_val, 2, Ticker.output_base)
    
    @staticmethod
    def render(screen, type_font):
        for ticker in Ticker.ticker_list:
            loc = (ticker.loc[0]-10, ticker.loc[1]-20)
            screen.blit(ticker.sprite, loc)
            num = type_font.render(str(2**(len(Ticker.ticker_list)-ticker.index-1)), True, color_white)
            screen.blit(num, ticker.loc)
    
    @staticmethod
    def init_tickers(num_tickers:int, base):
        Ticker.ticker_list = []
        Ticker.bin_val = '0'*num_tickers
        Ticker.int_val = '0'
        Ticker.output_base = 10 if base == 2 else 16
        
        for i in range(num_tickers):
            loc = (ticker_x_range[0] + (ticker_x_range[1] - ticker_x_range[0]) / num_tickers * i, ticker_y_val)
            Ticker.ticker_list.append(Ticker(loc, i))
            
class LevelHandler:
    bin_max_value_time_dict = {1: (8, 10), 2: (16, 10), 3: (32, 9), 4: (32, 8), 5: (64, 7), 6: (128, 7), 7: (256, 7), 8: (256, 6), 9: (256, 15), 10: (256, 13), 11: (256, 10)}
    hex_max_value_time_dict = {1: (16, 10), 2: (32, 10), 3: (32, 9), 4: (32, 8), 5: (32, 7), 6: (64, 7), 7: (128, 7), 8: (128, 7), 9: (256, 7), 10: (256, 15), 11: (256, 13)}
    
    def __init__(self, base):
        self.level = 0
        self.threshold = 1
        self.int_val = '0'
        self.value_dict = LevelHandler.bin_max_value_time_dict if base == 2 else LevelHandler.hex_max_value_time_dict
        self.generate_new_level()
        
    def generate_new_level(self):
        global frame_count
        frame_count = 1
        self.threshold -= 1
        if self.threshold == 0:
            self.threshold = 10
            self.level += 1
        if self.level+1 == len(self.value_dict.keys()):
            win()
        Ticker.reset()
        max_val, self.time = self.value_dict[self.level]
        
        rand_list = [item for item in range(max_val)]
        rand_list.remove(int(base_convert(self.int_val, Ticker.output_base, 10)))
        self.int_val = base_convert(str(choice(rand_list)), 10, Ticker.output_base)
        
    def submit(self, check_val):
        if check_val == self.int_val:
            self.generate_new_level()
        else:
            death_menu('Wrong Answer', self)

def main_ui_render(lvl):
    screen.blit(submit_button, low_button_center)
    
    level_text = type_font.render(f"Level {lvl.level}", True, color_white)
    placeholder_text = type_font.render(f"What is {' '*(2+len(lvl.int_val)*6)} in binary?", True, color_white)
    time_text = type_font.render(f"{lvl.time} seconds left", True, color_white)
    
    answer_text = big_font.render(Ticker.int_val, True, color_orange)
    number_text = big_font.render(lvl.int_val, True, color_orange)
    
    screen.blit(level_text, (580, 200))
    screen.blit(answer_text, (1000, 550))
    screen.blit(placeholder_text, (460, 300))
    screen.blit(number_text, (605, 280))
    screen.blit(time_text, (515, 400))
        
            
def event_loop(Level):
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
        if event.type == pygame.MOUSEBUTTONUP:
            for ticker in Ticker.ticker_list:
                if ticker.rect.collidepoint(mouse_pos):
                    ticker.click()
            if submit_button_rect.collidepoint(mouse_pos):
                Level.submit(Ticker.int_val)
            
def start_menu() -> None:
    answer_base = 2
    while(True):
        screen.blit(background, (0, 0))
        screen.blit(start_button, button_center)
        screen.blit(race, (520, 270))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if start_button_rect.collidepoint(pygame.mouse.get_pos()):
                    main(answer_base)
                if slider_rect.collidepoint(pygame.mouse.get_pos()):
                    answer_base = 2 if answer_base == 16 else 16
                    
        screen.blit(slider_outline, slider_loc)
        if answer_base == 2:
            screen.blit(bin_slide, slider_loc)
        elif answer_base == 16:
            slider_loc_2 = (slider_loc[0]+120, slider_loc[1])
            screen.blit(hex_slide, slider_loc_2)
        
        pygame.display.update()
        clock.tick(60)
        
def death_menu(msg, lvl):
    while(True):
        screen.blit(background, (0, 0))
        level_text = type_font.render(f"You made it to level {lvl.level}!", True, color_white)
        race_text = type_font.render("Ready to race?", True, color_white)
        death_text = type_font.render(msg, True, color_red)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if exit_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
                if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
                    start_menu()
        
        
        screen.blit(level_text, (465, 200))
        screen.blit(race_text, (530, 250))
        screen.blit(death_text, (520, 440))
        
        screen.blit(exit_button, exit_button_loc)
        screen.blit(start_button, restart_button_loc)
        
        pygame.display.update()
        clock.tick(60)

def win():
    while(True):
        screen.blit(background, (0, 0))
        level_text = type_font.render("Winner winner chicken dinner.", True, color_white)
        race_text = type_font.render("Race again?", True, color_white)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if exit_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
                if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
                    start_menu()
        
        
        screen.blit(level_text, (400, 200))
        screen.blit(race_text, (550, 250))
        
        screen.blit(exit_button, exit_button_loc)
        screen.blit(start_button, restart_button_loc)
        
        pygame.display.update()
        clock.tick(60)

def main(answer_base) -> None:
    global frame_count
    Ticker.init_tickers(8, answer_base)
    lvl = LevelHandler(answer_base)
    frame_count = 0
    while(True):
        frame_count += 1
        screen.blit(background, (0, 0))

        Ticker.render(screen, type_font)
        
        event_loop(lvl)
        
        main_ui_render(lvl)
        
        if frame_count % 60 == 0:
            lvl.time -= 1
            if lvl.time == -1:
                death_menu("      Time out", lvl)
                
        pygame.display.update()
        clock.tick(60)
        
start_menu()