import pygame
import numpy as np

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
NUM_ANTS = 5
NUM_FOOD = 3
PHEROMONE_EVAP_RATE = 0.99
MAX_PHEROMONE = 1000
FOOD_VALUE = 50
NEARBY_DISTANCE = 50
NEARBY_PHEROMONE_FACTOR = 0.1
PHEROMONE_FACTOR = 1

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define Ant class
class Ant:
    def __init__(self):
        self.position = np.random.rand(2) * (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.velocity = np.zeros(2)
        self.food = False
        self.pheromone = np.zeros(2)
        
    def update(self, ants, food):
        # Move towards food or pheromone trail
        if self.food:
            target = np.array([SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
            nearby_pheromones = [a.pheromone for a in ants if not a.food and np.linalg.norm(self.position - a.position) < NEARBY_DISTANCE]
            if nearby_pheromones:
                self.velocity += NEARBY_PHEROMONE_FACTOR * sum(nearby_pheromones) / len(nearby_pheromones)
        else:
            if np.linalg.norm(self.position - food.position) < NEARBY_DISTANCE:
                self.velocity += PHEROMONE_FACTOR * food.pheromone
            else:
                self.velocity += PHEROMONE_FACTOR * (food.position - self.position) / np.linalg.norm(food.position - self.position)
        
        # Move and update pheromones
        self.position += self.velocity
        self.pheromone += self.velocity
        self.pheromone *= PHEROMONE_EVAP_RATE
        self.pheromone = np.clip(self.pheromone, 0, MAX_PHEROMONE)
        
        # Check for food or nest
        if not self.food and np.linalg.norm(self.position - food.position) < 5:
            self.food = True
            food.value -= FOOD_VALUE
        elif self.food and np.linalg.norm(self.position - target) < 5:
            self.food = False
            food.value += FOOD_VALUE
            self.pheromone = np.zeros(2)
        
        # Wrap around screen edges
        self.position = self.position % (SCREEN_WIDTH, SCREEN_HEIGHT)
        
    def draw(self):
        if self.food:
            color = (255, 0, 0)
        else:
            color = (0, 255, 0)
        pygame.draw.circle(screen, color, self.position.astype(int), 5)
        pygame.draw.circle(screen, color, self.position.astype(int), int(np.sqrt(np.sum(self.pheromone)))//2, 1)

# Define Food class
class Food:
    def __init__(self):
        self.position = np.array([SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
        self.value = NUM_FOOD * FOOD_VALUE
        self.pheromone = np.zeros(2)
        
    def update(self):
        self.pheromone += self.value / MAX_PHEROMONE
        self.pheromone = np.clip(self.pheromone, 0, MAX_PHEROMONE)
        
    def draw(self):
        pygame.draw.circle(screen, (255, 255, 0), self.position.astype(int), 10)
        pygame.draw.circle(screen, (255, 255, 0), self.position.astype(int), int(np.sqrt(np.sum(self.pheromone)))//2, 1)

# Initialize ants and food
ants = [Ant() for i in range(NUM_ANTS)]
food = Food()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update ants and food
    for ant in ants:
        ant.update(ants, food)
    food.update()
    
    # Draw everything
    screen.fill((0, 0, 0))
    for ant in ants:
        ant.draw()
    food.draw()
    pygame.display.flip()
    
# Quit Pygame
pygame.quit()