import cv2
import pygame
import numpy as np

# Initialize Pygame
pygame.init()
screen_width, screen_height = 640, 480
game_display = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catch the Moving Object")

# Set up the game variables
object_size = 50
object_position = np.array([screen_width/2, screen_height/2])
object_velocity = np.random.uniform(-5, 5, size=2)
score = 0
max_rounds = 10
round_number = 0

# Set up the font for displaying the score
font = pygame.font.Font(None, 36)

# Start the game loop
while round_number < max_rounds:
    # Update the object position
    object_position += object_velocity
    if object_position[0] < 0 or object_position[0] > screen_width - object_size:
        object_velocity[0] *= -1
    if object_position[1] < 0 or object_position[1] > screen_height - object_size:
        object_velocity[1] *= -1
    
    # Draw the object on the screen
    game_display.fill((255, 255, 255))
    pygame.draw.rect(game_display, (255, 0, 0), (object_position[0], object_position[1], object_size, object_size))
    
    # Display the score on the screen
    score_text = font.render("Score: {}".format(score), True, (0, 0, 0))
    game_display.blit(score_text, (10, 10))
    
    # Update the Pygame display
    pygame.display.update()
    
    # Check for user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = np.array(pygame.mouse.get_pos())
            if np.all(mouse_position >= object_position) and np.all(mouse_position <= object_position + object_size):
                score += 1
                object_position = np.array([screen_width/2, screen_height/2])
                object_velocity = np.random.uniform(-5, 5, size=2)
                round_number += 1
                
# End the game
game_display.fill((255, 255, 255))
end_text = font.render("Game over! Final score: {}".format(score), True, (0, 0, 0))
game_display.blit(end_text, (screen_width/2 - end_text.get_width()/2, screen_height/2 - end_text.get_height()/2))
pygame.display.update()
pygame.time.delay(3000)
pygame.quit()
quit()