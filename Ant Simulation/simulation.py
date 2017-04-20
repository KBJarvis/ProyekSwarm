from __future__ import division 
from cell import Cell
from colony import Colony
from food import Food
import math

class Simulation:
  
  def __init__(self, surface, grid_size):
    self.is_running = True
    self.grid_size = grid_size
    self.cells = []
    self.food_items = []
    self.dimens = surface.get_size()

    self.init_cells()

    self.food_count = 3

    self.init_food()

    self.colony = Colony(self)

  def stop(self):
    self.is_running = False

  def init_cells(self):
    for i in range(0, self.grid_size):
      cell_row = []
      for j in range(0, self.grid_size):
        cell = Cell(i, j, self.dimens, self.grid_size)

        cell_row.append(cell)
      self.cells.append(cell_row)

  def init_food(self):
    for i in range(0, self.food_count):
      self.add_food()

  def update(self):
    for cell_row in self.cells:
      for cell in cell_row:
        cell.update()

    self.colony.update(self.dimens)

    for food in self.food_items:
      food.update()

  def add_food(self):
    food = Food(self)
    self.food_items.append(food)

  def kill_food(self, food):
    self.food_items.remove(food)

  def get_cell_at(self, pos):
    width = self.dimens[0]
    height = self.dimens[1]
    x = pos[0]
    y = pos[1]

    grid_x = int(((x / width) * self.grid_size))
    grid_y = int(((y / height) * self.grid_size))

    cell = self.cells[grid_x][grid_y]
    return cell

  def get_surrounding_cells(self, pos):
    cells = []

    cell = self.get_cell_at(pos)

    left_index = (cell.grid_i - 1) % self.grid_size
    right_index = (cell.grid_i + 1) % self.grid_size
    top_index = (cell.grid_j - 1) % self.grid_size
    bottom_index = (cell.grid_j + 1) % self.grid_size

    cells.append(self.cells[left_index][top_index])
    cells.append(self.cells[cell.grid_i][top_index])
    cells.append(self.cells[right_index][top_index])
    cells.append(self.cells[right_index][cell.grid_j])
    cells.append(self.cells[right_index][bottom_index])
    cells.append(self.cells[cell.grid_i][bottom_index])
    cells.append(self.cells[left_index][bottom_index])
    cells.append(self.cells[left_index][cell.grid_j])

    return cells

  def reset_cell(self, pos):
    cell = self.get_cell_at(pos)
    cell.set_pheromone_level(255)

  def render(self, surface):
    for cell_row in self.cells:
      for cell in cell_row:
        cell.render(surface)

    for food in self.food_items:
      food.render(surface)

    self.colony.render(surface)