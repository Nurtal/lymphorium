import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

class LymphocyteB:
    """Un agent simple qui se déplace sur une grille."""

    def __init__(self, x, y, grid_size):
        self.x = x
        self.y = y
        self.grid_size = grid_size
        self.color = 'blue'

    def move(self):
        """Déplacement aléatoire dans la grille."""
        dx, dy = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
        self.x = np.clip(self.x + dx, 0, self.grid_size - 1)
        self.y = np.clip(self.y + dy, 0, self.grid_size - 1)

    def activate():
        self.color = 'red'
    

class LymphocyteT:
    """Un agent simple qui se déplace sur une grille."""

    def __init__(self, x, y, grid_size):
        self.x = x
        self.y = y
        self.grid_size = grid_size
        self.color = 'green'
        self.speed = 2

    def move(self):
        """Déplacement aléatoire dans la grille."""
        dx, dy = np.random.choice([-1, 0, 1]), np.random.choice([-self.speed, 0, self.speed])
        self.x = np.clip(self.x + dx, 0, self.grid_size - 1)
        self.y = np.clip(self.y + dy, 0, self.grid_size - 1)

def run_simulation(n_steps:int):
    """Run"""

    # Initialisation de la simulation
    grid_size = 20
    n_b_agents = 10
    b_agents = [LymphocyteB(np.random.randint(0, grid_size), np.random.randint(0, grid_size), grid_size) for _ in range(n_b_agents)]
    n_t_agents = 10
    t_agents = [LymphocyteT(np.random.randint(0, grid_size), np.random.randint(0, grid_size), grid_size) for _ in range(n_t_agents)]

    # Simulation
    for i in tqdm(range(n_steps), desc="Simulation en cours"):
        plt.figure(figsize=(5, 5))
        plt.xlim(0, grid_size)
        plt.ylim(0, grid_size)
        for b_agent in b_agents:
            b_agent.move()
            plt.scatter(b_agent.x, b_agent.y, c=b_agent.color)
        for t_agent in t_agents:
            t_agent.move()
            plt.scatter(t_agent.x, t_agent.y, c=t_agent.color)
        plt.savefig(f"figures/step_{i}.png")
        plt.close()

if __name__ == "__main__":

    run_simulation(100)
