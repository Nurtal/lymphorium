import numpy as np
import random

class Mastocyte:
    """Un agent simple qui se déplace sur une grille."""

    def __init__(self, x, y, grid_size):
        self.x = x
        self.y = y
        self.grid_size = grid_size
        self.color = 'purple'
        self.life_span = 10
        self.age = 0
        self.activated = False

    def move(self):
        """Déplacement aléatoire dans la grille."""
        dx, dy = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
        self.x = np.clip(self.x + dx, 0, self.grid_size - 1)
        self.y = np.clip(self.y + dy, 0, self.grid_size - 1)

    def get_older(self):
        self.age +=1

    def cell_division(self):
        new_cell = Mastocyte(self.x+1, self.y, self.grid_size)
        new_cell.color = self.color
        new_cell.age = 0
        return new_cell
