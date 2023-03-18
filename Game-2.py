import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
WINDOW_TITLE = "Pygame Game"
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# Set up the game clock
clock = pygame.time.Clock()

# Set up the player
player_x = 100
player_y = 100
player_speed = 5
player_size = 50
player_color = (random.uniform(0,255), random.uniform(0,255), random.uniform(0,255))

# Set up the enemy
enemy_x = random.randint(0, WINDOW_WIDTH - player_size)
enemy_y = random.randint(0, WINDOW_HEIGHT - player_size)
enemy_speed = 3
enemy_size = 50
enemy_color = (random.uniform(0,255), random.uniform(0,255), random.uniform(0,255))

# Set up the score
score = 0
font = pygame.font.Font(None, 36)

# Game loop
game_running = True
while game_running:

    score += 1

    # check if player is outside of the screen
    if player_x < -25 or player_x > WINDOW_WIDTH + 25 or \
            player_y < -25 or player_y > WINDOW_HEIGHT + 25:
        score -= 100

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Move the enemy
    if enemy_x < player_x:
        enemy_x += enemy_speed
    elif enemy_x > player_x:
        enemy_x -= enemy_speed
    if enemy_y < player_y:
        enemy_y += enemy_speed
    elif enemy_y > player_y:
        enemy_y -= enemy_speed

    # Check for collision
    if (player_x < enemy_x + enemy_size and
            player_x + player_size > enemy_x and
            player_y < enemy_y + enemy_size and
            player_y + player_size > enemy_y):
        score -= 10
        enemy_x = random.randint(0, WINDOW_WIDTH - player_size)
        enemy_y = random.randint(0, WINDOW_HEIGHT - player_size)

    # Draw the game
    window.fill((0, 0, 0))
    pygame.draw.rect(window, player_color, (player_x, player_y, player_size, player_size))
    pygame.draw.rect(window, enemy_color, (enemy_x, enemy_y, enemy_size, enemy_size))
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(score_text, (10, 10))
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Clean up
pygame.quit()