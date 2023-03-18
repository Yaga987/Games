import pygame
import random

# initialize pygame
pygame.init()

# set the window size
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))

# set the game title
pygame.display.set_caption("Maze Runner")

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set the game clock
clock = pygame.time.Clock()

# define the player class
class Player(pygame.sprite.Sprite):
    def __init__(self, game_over):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
        self.health = 5
        self.game_over = game_over

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def hit(self):
        self.health -= 1
        print(self.health)
        if self.health <= 0:
            self.game_over = True
            print("Game Over!")
            # self.kill()
            # self.all_sprites.remove(self)

# define the coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, window_width - 10)
        self.rect.y = random.randint(0, window_height - 10)

        # generate a new position that is not too close to any existing sprite
        while True:
            self.rect.x = random.randint(0, window_width - 30)
            self.rect.y = random.randint(0, window_height - 30)
            if not any(sprite.rect.colliderect(self.rect.inflate(50, 50)) for sprite in all_sprites):
                break
        
        def update(self):
            self.all_sprites.add(self)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        # generate a new position that is not too close to any existing sprite
        while True:
            self.rect.x = random.randint(0, window_width - 30)
            self.rect.y = random.randint(0, window_height - 30)
            if not any(sprite.rect.colliderect(self.rect.inflate(50, 50)) for sprite in all_sprites):
                break

        self.health = 1
        self.all_sprites = all_sprites

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            pygame.time.set_timer(pygame.USEREVENT, 3000)  # spawn new enemy after 3 seconds
            self.all_sprites.remove(self)

    def update(self):
        self.all_sprites.add(self)

game_over = False

# create the player object
player = Player(game_over)

# create the coins and obstacles groups
coins = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# add coins to the coins group
for i in range(10):
    coin = Coin(all_sprites)
    coins.add(coin)
    all_sprites.add(coin)

# add the player to all_sprites
all_sprites.add(player)

# add obstacles to the obstacles group
for i in range(5):
    obstacle = Obstacle(all_sprites)
    obstacles.add(obstacle)
    all_sprites.add(obstacle)

# set the game loop
score = 0
while not game_over:
    # set flags for continuous movement
    move_left = False
    move_right = False
    move_up = False
    move_down = False

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_UP:
                move_up = True
            elif event.key == pygame.K_DOWN:
                move_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_UP:
                move_up = False
            elif event.key == pygame.K_DOWN:
                move_down = False

    # move the player continuously
    if move_left:
        player.move(-5, 0)
    if move_right:
        player.move(5, 0)
    if move_up:
        player.move(0, -5)
    if move_down:
        player.move(0, 5)

    # check collisions between the player and coins
    coins_hit = pygame.sprite.spritecollide(player, coins, True)
    for coin in coins_hit:
        score += 1

    # check collisions between the player and obstacles
    obstacles_hit = pygame.sprite.spritecollide(player, obstacles, False)
    for obstacle in obstacles_hit:
        player.hit()
        obstacle.hit()

    # spawn new obstacle if needed
    if len(obstacles) == 0  or len(obstacles) <= 5:
        obstacle = Obstacle(all_sprites)
        obstacles.add(obstacle)

    # spawn new obstacle if needed
    if len(coins) == 0 or len(coins) <= 10:
        coin = Coin(all_sprites)
        coins.add(coin)

    # spawn new obstacle after 3 seconds
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            obstacle = Obstacle(all_sprites)
            obstacles.add(obstacle)

    # if player.health <= 0:
    #     game_over = True

    # update the health bar
    # health_bar_width = 100
    # health_bar_height = 20
    # health_bar_rect = pygame.Rect(10, 30, health_bar_width, health_bar_height)
    # health_bar_inner_rect = pygame.Rect(0, 0, health_bar_width * player.health / 3, health_bar_height)
    # pygame.draw.rect(window, GREEN, health_bar_rect)
    # pygame.draw.rect(window, RED, health_bar_inner_rect)

    # update the screen
    window.fill(WHITE)
    coins.draw(window)
    obstacles.draw(window)
    window.blit(player.image, player.rect)
    pygame.display.flip()

    # set the game score
    font = pygame.font.Font(None, 30)

    # check if the player collected all the coins
    # if len(coins) == 0:
    #     game_over = True

    # update the score
    score_text = font.render("Score: {}".format(score), True, BLACK)
    window.blit(score_text, (10, 10))

    # check if game over
    if player.game_over:
        game_over = True

    # set the game speed
    clock.tick(60)

# handle game over
window.fill(WHITE)
game_over_text = font.render("Game Over!", True, BLACK)
score_text = font.render("Final Score: {}".format(score), True, BLACK)
window.blit(game_over_text, (window_width // 2 - 50, window_height // 2 - 20))
window.blit(score_text, (window_width // 2 - 70, window_height // 2 + 20))
pygame.display.flip()

pygame.time.wait(2000)  # wait for 2 seconds before quitting
pygame.quit()
quit()