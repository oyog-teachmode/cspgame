import pygame, sys

from settings import *
from songs import *
from level import Level

#initiation
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('The place.')
pygame.font.init()
font = pygame.font.Font("Ubuntu.ttf", 21)  #text box text

clock = pygame.time.Clock()

#txt_box = pygame.image.load("img/txt_box.png").convert_alpha()
#cur = pygame.image.load("img/cursor.png").convert_alpha()

level = Level(level_map, screen)

#variable initiation

#jihugyftdresrtyuhiytxdzs
print("Initiating Sound...")
pygame.mixer.pre_init(32000, -16, 16, 512)
print('init =', pygame.mixer.get_init())
print('channels =', pygame.mixer.get_num_channels())
#iouyiture

from battle import *
from menu import menu_loop

MENU_CLICK = pygame.mixer.Sound('sound/click.wav')


menu_BGM = pygame.mixer.Sound('music/menu.wav')
BGM = pygame.mixer.Sound('music/00.wav')

txtScr = 0
input_allowed = True
current_line = 1
txt1 = ""
txt2 = ""
txt3 = ""
txt1_out = ""
txt2_out = ""
txt3_out = ""

battle_music_init = False # has the battle music been played yet?

print("Sound Success! \n")
"""
printB() usage:
automatically formats text to be displayed in the text box
dont put printB or update_text in a loop
"""


def printB(i1, i2, i3):  #used for printing text into the text boxes
    global txt1, txt2, txt3
    global current_line
    txt1 = i1
    txt2 = i2
    txt3 = i3
    current_line = 1


def update_text(
):  #does the scrolling text thing in RPGs, I am very sorry for the jankiness.
    global current_line, txtScr
    global txt1_out, txt2_out, txt3_out
    global txt1, txt2, txt3
    global text_has_finished

    txt1_out = txt1
    txt2_out = txt2
    txt3_out = txt3

    line1 = font.render(txt1_out, True, (255, 255, 255))
    line2 = font.render(txt2_out, True, (255, 255, 255))
    line3 = font.render(txt3_out, True, (255, 255, 255))
    screen.blit(line1, (25, 20))  #BGLAYER0
    screen.blit(line2, (25, 45))  #BGLAYER0
    screen.blit(line3, (25, 70))  #BGLAYER0


def debug(a):
    if a == 1:
        print("reserved")
    else:
        print("What you entered was invalid")


while True:
  # Limit to 60 frames
  clock.tick(60)

  #mus_track = 0
  #mus_track_string = str(mus_track)
  #BGM = pygame.mixer.Sound('music/' + mus_track_string + '.wav')

  #updates display every frame
  pygame.display.flip()

  update_text()

  if code_bank == 0:
    screen.fill("blue")
    level.run()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.KEYDOWN and input_allowed == True:
        
        if event.key == pygame.K_j or event.key == pygame.K_z:
          code_bank = 1
          menu_BGM.play(-1)
        if event.key == pygame.K_k or event.key == pygame.K_x:
          printB("No problem here.", " ", " ")
          MENU_CLICK.play()

        if event.key == pygame.K_1:
          print("WARNING: THE WINDOW IS NO LONGER RUNNING \n\n _______DEBUG MENU_______ \n 1. I have no idea what this does \n ")
          debug(int(input("Pick your number:")))

  if code_bank == 1:
    screen.fill((70, 45, 30))
    menu_loop()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
              sys.exit()
            if event.type == pygame.KEYDOWN and input_allowed == True:
              if event.key == pygame.K_j or event.key == pygame.K_z:
                code_bank = 0
                menu_BGM.fadeout(400)

              if event.key == pygame.K_k or event.key == pygame.K_x:
                MENU_CLICK.play()
                code_bank = 2
                menu_BGM.fadeout(200)
                battle_music_init = False

              if event.key == pygame.K_1:
                print("WARNING: THE WINDOW IS NO LONGER RUNNING \n\n _______DEBUG MENU_______ \n 1. Replace item in slot \n ")
                debug(int(input("Pick your number:")))

  if code_bank == 2:
    battle_loop()
    
    if battle_music_init == False:
      battle_music_init = True
      BGM1.play(-1)
      BGM2.play(-1)
      BGM2.set_volume(0)
      
