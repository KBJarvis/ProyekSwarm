import pygame
from random import randint

class Food:

  def __init__(self, sim):
    self.sim = sim

    self.set_position(sim.dimens)
    self.w = 20
    self.h = 20

    self.food_level = 1000

    self.color = (0, 255, 0)

  def update(self):
    if self.food_level == 0:
      self.sim.add_food()
      self.sim.kill_food(self)

  def set_position(self, dimens):
    width = dimens[0]
    height = dimens[1]

    offset = [
      randint(15, 150),
      randint(15, 150),
    ]

    directions = [-1, 1]

    direction = [
      directions[randint(0, 1)],
      directions[randint(0, 1)],
    ]

    x = 0
    y = 0

    x = (x + offset[0] * direction[0]) % width 
    y = (y + offset[1] * direction[1]) % height 

    self.x = x
    self.y = y

  def get_shape(self):
    points = []

    x = self.x
    y = self.y
    w = self.w
    h = self.h

    points.append([x - (w / 2), y - (h / 2)])
    points.append([x + (w / 2), y - (h / 2)])
    points.append([x + (w / 2), y + (h / 2)])
    points.append([x - (w / 2), y + (h / 2)])

    return points

  def render(self, surface):
    pygame.draw.polygon(surface, self.color, self.get_shape(), 0)