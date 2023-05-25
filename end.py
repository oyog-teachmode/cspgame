import pygame
import sys
from urllib.request import urlopen
import io

# Initialize Pygame
#pygame.init()
pygame.font.init()
pygame.mixer.init()
# Set the window size
WINDOW_SIZE = screen_width, screen_height = (800, 600)

# Create the window
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set the font and size
font = pygame.font.Font("Augusta.ttf", 75)


# Set the text for the button
text = font.render("Exit", True, (255, 255, 255))

# Create the button
exit_button = pygame.Rect(
    (WINDOW_SIZE[0] // 2) - 100,
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
        elif event.type == pygame.MOUSEBUTTONDOWN and exit_button_displayed:
            # Check if the mouse clicked on the exit button
            if exit_button.collidepoint(event.pos):
                # Hide the exit button
                exit_button_displayed = False
                # Display the image for 10 seconds
                image_displayed = True
                image_start_time = pygame.time.get_ticks()
        elif exit_button_displayed == True:
            play_song()
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the exit button if it's displayed
    if exit_button_displayed:
        pygame.draw.rect(screen, (255, 0, 0), exit_button)
        screen.blit(text, (
            exit_button.centerx - (text.get_width() // 2),
            exit_button.centery - (text.get_height() // 2)
        ))
    
    # Draw the image if it's displayed
    if image_displayed:
        # Load the image from a URL
        #image_url = "https://codehs.com/uploads/cdd56fbf4c3c4c41e1bbb7cbf29f2433"
        #image_str = urlopen(image_url).read()
        #image_file = io.BytesIO(image_str)
        image_file = 'end1.png'
        x,y = 800, 566
        scale = .9
        x, y = int(scale*x),int(scale*y)
        size = (x,y)
        image = pygame.image.load(image_file)
        image = pygame.transform.scale(image,size)
        image_location = (WINDOW_SIZE[0]/2-(x//2), WINDOW_SIZE[1]/2-(y//2))
        # Display the image
        screen.blit(image, image_location)

        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, ((WINDOW_SIZE[0] // 2) - 150, (WINDOW_SIZE[1] // 2) + 200))
        # Check if 10 seconds have passed since the image was displayed
        
        if pygame.time.get_ticks() - image_start_time >= 28000:
            # End the program
            pygame.quit()
            sys.exit()
    
    # Update the screen
    pygame.display.update()
    
    # Tick the clock
    clock.tick(60)