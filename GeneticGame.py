import pygame
import random

# Define the fitness function
def fitness(agent_behavior):
    # Initialize the Pygame and the game window
    pygame.init()
    # Define the font
    pygame.font.init()
    FONT = pygame.font.SysFont('Comic Sans MS', 20)

    screen = pygame.display.set_mode((200, 200))
    pygame.display.set_caption("Genetic Algorithm Pygame")

    # Set up the game objects
    player = pygame.Rect(100, 100, 20, 20)
    food = pygame.Rect(random.randint(0, 180), random.randint(0, 180), 20, 20)
    score = 0

    # Set up the clock and the game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update the game objects
        player_behavior = agent_behavior(player, food)
        player.move_ip(player_behavior)
        if player.colliderect(food):
            food = pygame.Rect(random.randint(0, 180), random.randint(0, 180), 20, 20)
            score += 1
        
        # Draw the game objects
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0,0,255), player)
        pygame.draw.rect(screen, (0, 255, 0), food)
        text_gen = FONT.render(f'Score: {score}', True, (255,255,255))
        screen.blit(text_gen, (10, 10))
        pygame.display.flip()

        # Check for game over
        if player.left < 0 or player.right > 200 or player.top < 0 or player.bottom > 200:
            running = False
        
        # Tick the clock
        clock.tick(10)

    # Clean up the Pygame and return the score
    pygame.quit()
    return score

# Define the genetic algorithm
def genetic_algorithm(population_size, generations):
    # Create a population of random agents
    population = []
    for i in range(population_size):
        agent_behavior = lambda player, food: (random.randint(-10, 10), random.randint(-10, 10))
        population.append(agent_behavior)
    
    # Iterate through the generations
    for generation in range(generations):
        # Evaluate the fitness of each agent
        fitness_scores = []
        for agent_behavior in population:
            fitness_scores.append(fitness(agent_behavior))
        
        # Select the top performers
        top_performers = []
        for i in range(5): # Select the top 5 performers
            index = fitness_scores.index(max(fitness_scores))
            top_performers.append(population[index])
            fitness_scores.pop(index)
            population.pop(index)
        
        # Generate the next generation
        for i in range(population_size - 5): # Create new agents to fill out the population
            parent1 = random.choice(top_performers)
            parent2 = random.choice(top_performers)
            child_behavior = lambda player, food: (parent1(player, food)[0], parent2(player, food)[1])
            population.append(child_behavior)
    
    # Return the best performing agent
    best_agent_behavior = top_performers[0]
    return best_agent_behavior

# Run the genetic algorithm and play the game with the best agent
best_agent_behavior = genetic_algorithm(10, 5)
fitness_score = fitness(best_agent_behavior)
print("Best agent behavior:", best_agent_behavior)
print("Fitness score:", fitness_score)