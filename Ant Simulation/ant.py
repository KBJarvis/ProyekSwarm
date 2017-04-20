import pygame
import math
from random import randint

class Ant:

  def __init__(self, colony):
    self.colony = colony

    self.x = colony.x
    self.y = colony.y
    self.w = 5
    self.h = 10

    self.directions = ['NW', 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W']
    self.direction = self.directions[randint(0, len(self.directions) - 1)]
    self.direction_timer = 20

    self.has_food = False
    self.food_level = 0

    self.color = (255, 0, 0)

    self.energy = 1000

  def increment_energy(self, i):
    new = self.energy + i

    if new >= 0:
      self.energy = new
    else:
      self.colony.kill(self)

  def inc_direction_timer(self, i):
    new = self.direction_timer + i

    if new >= 0:
      self.direction_timer = new

  def update(self, dimens):
    self.update_pos(dimens)
    self.check_collisions()
    self.update_energy()
    self.leave_pheromones()
    self.update_direction()

  def update_pos(self, dimens):
    new_pos = self.get_new_pos()
    new_pos = self.bound_pos(new_pos, dimens)

    self.x = new_pos[0]
    self.y = new_pos[1]

  def get_new_pos(self):
    pos_diff = [0, 0]

    if 'N' in self.direction:
      pos_diff[1] = -2
    if 'S' in self.direction:
      pos_diff[1] = 2
    if 'E' in self.direction:
      pos_diff[0] = 2
    if 'W' in self.direction:
      pos_diff[0] = -2

    new_pos = (self.x + pos_diff[0], self.y + pos_diff[1])

    return new_pos

  def bound_pos(self, pos, dimens):
    new_pos = []

    for i, d in enumerate(pos):
      if d >= dimens[i]:
        new_pos.append(dimens[i]-1)
        self.reverse_direction()
      elif d <= 0:
        new_pos.append(0)
        self.reverse_direction()
      else:
        d = d % dimens[i]
        new_pos.append(d)

    return new_pos

  def check_collisions(self):
    if self.has_food:
      self.check_home_collisions()
    else:
      self.check_food_collisions()

  def check_home_collisions(self):
    horizontal = self.x < self.colony.x + self.colony.radius and self.x > self.colony.x - self.colony.radius

    vertical = self.y < self.colony.y + self.colony.radius and self.y > self.colony.y - self.colony.radius

    if horizontal and vertical:
      self.colony.food_level = self.colony.food_level + self.food_level
      self.food_level = 0
      self.has_food = False

      self.reverse_direction()

  def reverse_direction(self):
    current_index = self.directions.index(self.direction)
    opposite_index = (current_index + 4) % len(self.directions)
    self.direction = self.directions[opposite_index]

  def check_food_collisions(self):
    for food in self.colony.sim.food_items:
      if not self.has_food:
        radius = food.w / 2

        horizontal = self.x < food.x + radius and self.x > food.x - radius

        vertical = self.y < food.y + radius and self.y > food.y - radius

        if horizontal and vertical:
          self.energy = 1000
          self.food_level = self.food_level + 100
          food.food_level = food.food_level - 100
          self.has_food = True

  def update_energy(self):
    self.increment_energy(-1)

  def leave_pheromones(self):
    cell = self.colony.sim.get_cell_at((self.x, self.y))

    if self.has_food:
      amount = 255
    else:
      amount = (255 - cell.pheromone_level) / 10

    increment = amount
    cell.inc_pheromone_level(increment)

  def update_direction(self):
    if self.has_food:
      self.get_direction_home()
    else:
      if self.direction_timer == 0:
        self.get_direction_from_pheromones()
      else:
        self.inc_direction_timer(-1)

  def get_direction_home(self):
    home_pos = (self.colony.x, self.colony.y)

    d = ''

    if home_pos[1] > self.y + 5:
      d = d + 'S'
    elif home_pos[1] < self.y - 5:
      d = d + 'N'

    if home_pos[0] > self.x + 5:
      d = d + 'E'
    elif home_pos[0] < self.x - 5:
      d = d + 'W'

    self.direction = d

  def get_direction_from_random(self):
    diff = randint(-2, 2)
    choice = (self.directions.index(self.direction) + diff) % len(self.directions)
    self.direction = self.directions[choice]
    self.direction_timer = randint(15, 30)

  def get_direction_from_pheromones(self):
    neighbours = self.colony.sim.get_surrounding_cells((self.x, self.y))

    strongest = 0
    strongest_cell_indices = []
    choice = 0
    chosen = False

    for i, cell in enumerate(neighbours):
      if not self.opposite(i):
        if cell.pheromone_level == strongest:
          strongest_cell_indices.append(i)
        if cell.pheromone_level > strongest:
          strongest_cell_indices = []
          strongest_cell_indices.append(i)
          strongest = cell.pheromone_level
          choice = i
          chosen = True

    if chosen:
      index = randint(0, len(strongest_cell_indices) - 1)
      choice = strongest_cell_indices[index]
      self.direction = self.directions[choice]
      self.direction_timer = 5
    else:
      self.get_direction_from_random()

  def opposite(self, choice):
    current_index = self.directions.index(self.direction)

    opposite = False
    for i in range(current_index + 3, current_index + 6):
      if choice == i % (len(self.directions)):
        opposite = True

    return opposite

  def get_shape(self):
    d = self.direction
    points = []

    x = self.x
    y = self.y
    w = self.w
    h = self.h

    if len(d) == 1:
      if 'N' in d or 'S' in d:
        points.append([x - (w / 2), y - (h / 2)])
        points.append([x + (w / 2), y - (h / 2)])
        points.append([x + (w / 2), y + (h / 2)])
        points.append([x - (w / 2), y + (h / 2)])
      else:
        points.append([x - (h / 2), y - (w / 2)])
        points.append([x + (h / 2), y - (w / 2)])
        points.append([x + (h / 2), y + (w / 2)])
        points.append([x - (h / 2), y + (w / 2)])
    else:
      tmp_points = []
      tmp_points.append([x - (w / 2), y - (h / 2)])
      tmp_points.append([x + (w / 2), y - (h / 2)])
      tmp_points.append([x + (w / 2), y + (h / 2)])
      tmp_points.append([x - (w / 2), y + (h / 2)])

      if d == 'NW' or d == 'SE':
        theta = (math.pi / 8) * 7
      else:
        theta = math.pi / 8

      for point in tmp_points:
        temp_x = point[0] - x
        temp_y = point[1] - y

        rotated_x = (temp_x * math.cos(theta)) - (temp_y * math.sin(theta))
        rotated_y = (temp_x * math.sin(theta)) + (temp_y * math.cos(theta))

        points.append([rotated_x + x, rotated_y + y])

    return points

  def render(self, surface):
    pygame.draw.polygon(surface, self.color, self.get_shape(), 0)

    if self.has_food:
      pygame.draw.rect(surface, (0, 255, 0), [self.x, self.y, 2, 2], 0)