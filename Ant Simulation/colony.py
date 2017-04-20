from __future__ import division
import pygame
from ant import Ant

class Colony:

  def __init__(self, sim):
    self.sim = sim

    self.x = int(self.sim.dimens[0] / 2)
    self.y = int(self.sim.dimens[1] / 2)

    self.radius = 10
    self.color = (0, 0, 255)

    self.food_level = 0

    self.spawn_rate = 20

    self.ants = []

    self.spawn_count = 0

    self.spawn()

  def inc_spawn_count(self, i):
    self.spawn_count = (self.spawn_count + i)

  def update(self, dimens):
    self.inc_spawn_count(1)

    spawn_limit = (1 / self.spawn_rate) * 1000
    if self.spawn_count > spawn_limit:
      self.spawn()
      self.spawn_count = 0

    for ant in self.ants:
      ant.update(dimens)

  def render(self, surface):
    pos = (self.x, self.y)
    pygame.draw.circle(surface, self.color, pos, self.radius, 0)

    for ant in self.ants:
      ant.render(surface)

  def spawn(self):
    ant = Ant(self)
    self.ants.append(ant)

  def kill(self, ant):
    cell = self.sim.get_cell_at((ant.x, ant.y))
    cell.pheromone_level = 0
    for cell in self.sim.get_surrounding_cells((ant.x, ant.y)):
      cell.pheromone_level = 0

    self.ants.remove(ant)