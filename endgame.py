import pygame
import sys
from urllib.request import urlopen
import io

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()
# Set the window size
WINDOW_SIZE = screen_width, screen_height = (800, 600)

# Create the window
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set the font and size
font1 = pygame.font.Font("Augusta.ttf", 75)
font2 = pygame.font.Font("Augusta.ttf", 100)

# Set the text for the button
exit = font1.render("Exit", True, (255, 255, 255))

# Create the button
exit_button = pygame.Rect(
    (WINDOW_SIZE[0] // 2) - 85,
    (WINDOW_SIZE[1] // 2) - 40,
    200,
    80
)

# Set the flag for the exit button and the image display
exit_button_displayed = False
image_displayed = False


def play_song():
    song = pygame.mixer.Sound('kops8b2_2.wav')
    song.set_volume(1)
    if not(pygame.mixer.get_busy()):
        song.play()

# Set the clock for the game loop
clock = pygame.time.Clock()

# Start the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Show the exit button
            exit_button_displayed = True
            image_displayed = True
            image_start_time = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONDOWN and exit_button_displayed:
            # Check if the mouse clicked on the exit button
            if exit_button.collidepoint(event.pos):
              pygame.quit()
              sys.exit()
              # Hide the exit button
              # Display the image for 10 seconds
        elif exit_button_displayed == True:
            play_song()
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the exit button if it's displayed
    if exit_button_displayed:
        pygame.draw.rect(screen, (125, 0, 0, 0), exit_button)
        exit = font1.render("Exit", True, (255, 255, 255))      
        screen.blit(exit, (
            exit_button.centerx - (exit.get_width() // 2),
            exit_button.centery - (exit.get_height() // 2)
        ))
    
    # Draw the image if it's displayed
    if image_displayed:
      # Load the image from a URL
      #image_url = "https://codehs.com/uploads/cdd56fbf4c3c4c41e1bbb7cbf29f2433"
      #image_str = urlopen(image_url).read()
      #image_file = io.BytesIO(image_str)
      image_file = 'end1.png'
      x,y = 800, 566
      scale = .85
      x, y = int(scale*x),int(scale*y)
      size = (x,y)
      pos_x, pos_y = (x//2), (y//2)
      image = pygame.image.load(image_file)
      image = pygame.transform.scale(image,size)
      image_location = (WINDOW_SIZE[0]//2-pos_x, WINDOW_SIZE[1]//2-pos_y)
      # Display the image
      screen.blit(image, image_location)
      if exit_button_displayed:
        pygame.draw.rect(screen, (125, 0, 0), exit_button)
        exit = font1.render("Exit", True, (255, 255, 255))
        screen.blit(exit, (
            exit_button.centerx - (exit.get_width() // 2),
            exit_button.centery - (exit.get_height() // 2)
        ))
      text = font2.render("Game Over", True, (125, 0, 0, 25))
      screen.blit(text, ((WINDOW_SIZE[0] // 2) - int(pos_x//(1.75)), (WINDOW_SIZE[1] // 4) - int(pos_y//2.1)))
      # Check if 10 seconds have passed since the image was displayed
      
      if pygame.time.get_ticks() - image_start_time >= 34000:
          # End the program
          pygame.quit()
          sys.exit()
    
    # Update the screen
    pygame.display.update()
    
    # Tick the clock
    clock.tick(60)