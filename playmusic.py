#pygame
import pygame

def play_music(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

while True:
    command = input("Enter 'p' to play, 's' to stop, 'q' to quit: ")
    if command.lower() == 'p':
        play_music('kops8b.mp3')
        #play_music('C:\\Users\\zach.oyog\\OneDrive - Capital Christian Center\\Documents\\CSP\\aba.mp3') # copy the path of the file use \\ in place of  \
    elif command.lower() == 's':
        pygame.mixer.music.stop()
    elif command.lower() == 'q':
        break
    else:
        print("Invalid command!")

