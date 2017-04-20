import pygame

class EventHandler:

  @staticmethod
  def process_event(sim, e):
    if e.type == pygame.QUIT:
      sim.stop()
