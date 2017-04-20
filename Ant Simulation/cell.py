from __future__ import division 
import pygame
from random import randint

class Cell:

  def __init__(self, i, j, dimens, grid_size):
    self.color = (255, 255, 255)

    self.grid_i = i
    self.grid_j = j

    self.pheromone_level = 0

    self.w = dimens[0] / grid_size
    self.h = dimens[1] / grid_size

    self.x = self.w * i
    self.y = self.h * j

  def set_pheromone_level(self, pheromone_level):
    self.pheromone_level = pheromone_level

  def inc_pheromone_level(self, i):
    new = self.pheromone_level + i

    if new < 0:
      new = 0
    elif new > 255:
      new = 255

    self.pheromone_level = new

  def update(self):
    self.inc_pheromone_level(-0.5)

  def get_intensity(self):
    intensity = (self.pheromone_level, self.pheromone_level, self.pheromone_level)
    return intensity

  def render(self, surface):
    rect = [self.x, self.y, self.w, self.h]

    pygame.draw.rect(surface, self.get_intensity(), rect, 0)