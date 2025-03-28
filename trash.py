import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import math
import os

class LymphocyteB:
    """Un agent simple qui se déplace sur une grille."""

    def __init__(self, x, y, grid_size):
        self.x = x
        self.y = y
        self.grid_size = grid_size
        self.color = 'blue'
        self.life_span = 10
        self.age = 0

    def move(self):
        """Déplacement aléatoire dans la grille."""
        dx, dy = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
        self.x = np.clip(self.x + dx, 0, self.grid_size - 1)
        self.y = np.clip(self.y + dy, 0, self.grid_size - 1)

    def activate(self):
        self.color = 'red'
    
    def get_older(self):
        self.age +=1

class LymphocyteT:
    """Un agent simple qui se déplace sur une grille."""

    def __init__(self, x, y, grid_size):
        self.x = x
        self.y = y
        self.grid_size = grid_size
        self.color = 'green'
        self.speed = 2
        self.life_span = 10
        self.age = 0

    def move(self):
        """Déplacement aléatoire dans la grille."""
        dx, dy = np.random.choice([-1, 0, 1]), np.random.choice([-self.speed, 0, self.speed])
        self.x = np.clip(self.x + dx, 0, self.grid_size - 1)
        self.y = np.clip(self.y + dy, 0, self.grid_size - 1)

    def get_older(self):
        self.age +=1




def detect_interaction(b_agent_list, t_agent_list):
    """ """
    # params
    interaction_treshold = 2
    
    for b_agent in b_agent_list:
        for t_agent in t_agent_list:

            # compute distance
            dist = math.sqrt((b_agent.x - t_agent.x)**2 + (b_agent.y - t_agent.y)**2)

            # activate b cell
            if dist <= interaction_treshold:
                b_agent.activate()
    

def drop_old_cell(b_agent_list, t_agent_list):
    """ """

    b_pop = []
    t_pop = []

    # deal with b cells
    for b_agent in b_agent_list:
        if b_agent.age <= b_agent.life_span:
            b_pop.append(b_agent)

    # deal with t cells
    for t_agent in t_agent_list:
        if t_agent.age <= t_agent.life_span:
            t_pop.append(t_agent)

    return b_pop, t_pop




def run_simulation(n_steps:int):
    """Run"""

    # initialisation de l'environnement
    if not os.path.isdir("figures"):
        os.mkdir("figures")

    # Initialisation de la simulation
    grid_size = 20
    n_b_agents = 10
    b_agents = [LymphocyteB(np.random.randint(0, grid_size), np.random.randint(0, grid_size), grid_size) for _ in range(n_b_agents)]
    n_t_agents = 10
    t_agents = [LymphocyteT(np.random.randint(0, grid_size), np.random.randint(0, grid_size), grid_size) for _ in range(n_t_agents)]

    # Simulation
    for i in tqdm(range(n_steps), desc="Simulation en cours"):

        # detect b activation
        detect_interaction(b_agents, t_agents)

        # drop old cells
        b_agents, t_agents = drop_old_cell(b_agents, t_agents)
        
        plt.figure(figsize=(5, 5))
        plt.xlim(0, grid_size)
        plt.ylim(0, grid_size)
        for b_agent in b_agents:
            b_agent.move()
            b_agent.get_older()
            plt.scatter(b_agent.x, b_agent.y, c=b_agent.color)
        for t_agent in t_agents:
            t_agent.move()
            t_agent.get_older()
            plt.scatter(t_agent.x, t_agent.y, c=t_agent.color)
        plt.savefig(f"figures/step_{i}.png")
        plt.close()


if __name__ == "__main__":

    run_simulation(100)
