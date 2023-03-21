import pygame
import neat
import random
import graphviz
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

# Define some constants for the simulation
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SHIP_SIZE = 20
FPS = 60
path = 'D:/Code/Python/Pygame-NEAT-Ship/config-feedforward.txt'
generation = 100
gen_num = 1
clock = pygame.time.Clock()

# Define the radius of the nodes in the neural network visualization
NODE_RADIUS = 10
INPUT_COLOR = (128, 0, 0)
OUTPUT_COLOR = (0, 128, 0)
HIDDEN_COLOR = (128, 128, 128)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# BLUE = (random.randint(0,100), random.randint(0,100), random.randint(200,255))
BLUE = (75, 225, 250)
RANDOM_COLOR = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

# Initialize Pygame and set up the screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NEAT Ship Simulation")

# Define the Ship class
class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        pygame.draw.rect(screen, RANDOM_COLOR, (self.x, self.y, SHIP_SIZE, SHIP_SIZE))

"""
def visualize_network(screen, net, inputs, gen):
    # Visualize a neural network on the Pygame screen.
    if gen <= generation:
        # Get the configuration for the network
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            path)

        # Calculate the positions of the nodes in the neural network
        node_positions = []
        num_layers = len(config.genome_config.layers)
        layer_height = SCREEN_HEIGHT / (num_layers + 1)
        for layer_idx in range(num_layers):
            layer_top = (layer_idx + 1) * layer_height
            num_nodes = config.genome_config.layers[layer_idx].size
            node_spacing = SCREEN_WIDTH / (num_nodes + 1)
            for node_idx in range(num_nodes):
                node_left = node_spacing * (node_idx + 1)
                node_positions.append((node_left, layer_top))

        # Calculate the outputs of the nodes in the neural network
        outputs = net.activate(inputs)

        # Draw the nodes in the network
        for node_idx, node_pos in enumerate(node_positions):
            node_color = int(outputs[node_idx] * 255)
            pygame.draw.circle(screen, (node_color, node_color, node_color), node_pos, NODE_RADIUS)

        # Draw the connections between nodes in the network
        for node_idx, node_pos in enumerate(node_positions):
            for conn in net.connections.values():
                if conn.enabled and conn.key[1] == node_idx:
                    conn_color = int(conn.weight * 255)
                    pygame.draw.line(screen, (conn_color, conn_color, conn_color), node_pos, node_positions[conn.key[0]], 1)
    """

# Define the fitness function for the NEAT algorithm
def calculate_fitness(genomes, config):
    global gen_num
    for genome_id, genome in genomes:
        genome.fitness = 0

        # Create a new Ship object for this genome
        ship = Ship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Create a feedforward neural network from the genome and the configuration file
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        # Run the simulation for a fixed number of frames
        prev_pos = (ship.x, ship.y)  # Keep track of previous position to check if the ship is stuck
        frames_stuck = 0  # Keep track of how many frames the ship has been stuck in one place
        for i in range(FPS * 10):
            # Get the output of the neural network
            output = net.activate([ship.x, ship.y, ship.vel_x, ship.vel_y])

            # Set the ship's velocity based on the output of the neural network
            ship.vel_x = output[0] * 10 - 5
            ship.vel_y = output[1] * 10 - 5

            # Update the ship's position
            ship.update()

            # Check if the ship has gone off the screen
            if ship.x < 0 or ship.x > SCREEN_WIDTH or ship.y < 0 or ship.y > SCREEN_HEIGHT:
                break

            # Check if the ship has been stuck in one place for too long
            curr_pos = (ship.x, ship.y)
            if abs(curr_pos[0] - prev_pos[0]) < 5 and abs(curr_pos[1] - prev_pos[1]) < 5:
                frames_stuck += 1
                if frames_stuck >= FPS * 15:  # If the ship has been stuck for more than 5 seconds
                    genome.fitness = 0  # Set the fitness to 0
                    print(f'Ship has not moved for too long.')
                    break
            else:
                frames_stuck = 0  # Reset the frames_stuck counter if the ship has moved

            # Increase the genome's fitness for each frame the ship is on the screen
            genome.fitness += 1

            prev_pos = curr_pos

        # Increase gen_num at the end of the generation
        gen_num += 1

# Set up the NEAT algorithm
config_file = path
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
population = neat.Population(config)

# Add the fitness function to the NEAT algorithm
population.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
population.add_reporter(stats)

# Run the NEAT algorithm for a fixed number of generations
winner = population.run(calculate_fitness, 10)

# Draw the winning Ship on the screen
ship = Ship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
net = neat.nn.FeedForwardNetwork.create(winner, config)
boolean_value = True
while boolean_value:
    if gen_num > generation:
        boolean_value = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            boolean_value = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                boolean_value = False

    output = net.activate([ship.x, ship.y, ship.vel_x, ship.vel_y])
    ship.vel_x = output[0] * 10 - 5
    ship.vel_y = output[1] * 10 - 5
    ship.update()

    screen.fill(BLUE)
    ship.draw()
    """
    output = net.activate([ship.x, ship.y, ship.vel_x, ship.vel_y])
    inputs = [ship.x, ship.y, ship.vel_x, ship.vel_y]
    visualize_network(screen, net, inputs, gen_num)
    """
    pygame.display.update()

    # Wait for a short time
    clock.tick(30)


# Quit the simulation
pygame.quit()