import pygame
import random
from simulation import Simulation
from event_handler import EventHandler

random.seed()

pygame.init()
pygame.display.set_caption('Ants')

size = (600, 600)
surface = pygame.display.set_mode(size)

sim = Simulation(surface, 75)

e_handler = EventHandler()

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

clock = pygame.time.Clock()

while sim.is_running:

  for event in pygame.event.get():
    e_handler.process_event(sim, event)

  sim.update()

  surface.fill(BLACK)

  sim.render(surface)

  pygame.display.flip()

pygame.quit()
