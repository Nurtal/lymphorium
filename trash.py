import numpy as np
import matplotlib.pyplot as plt

class LymphocyteB:
    """Un agent simple qui se déplace sur une grille."""

    def __init__(self, x, y, grid_size):
        self.x = x
        self.y = y
        self.grid_size = grid_size

    def move(self):
        """Déplacement aléatoire dans la grille."""
        dx, dy = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
        self.x = np.clip(self.x + dx, 0, self.grid_size - 1)
        self.y = np.clip(self.y + dy, 0, self.grid_size - 1)

# Initialisation de la simulation
grid_size = 20
n_agents = 10
agents = [LymphocyteB(np.random.randint(0, grid_size), np.random.randint(0, grid_size), grid_size) for _ in range(n_agents)]

# Simulation
for step in range(10):  # 10 étapes
    plt.figure(figsize=(5, 5))
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    for agent in agents:
        agent.move()
        plt.scatter(agent.x, agent.y, c="blue")
    plt.savefig(f"figures/step_{step}.png")
    plt.close()

