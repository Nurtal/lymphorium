import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import math
import os
import random
import pandas as pd

class LymphocyteB:
    """Un agent simple qui se déplace sur une grille."""

    def __init__(self, x, y, grid_size):
        self.x = x
        self.y = y
        self.grid_size = grid_size
        self.color = 'blue'
        self.life_span = 10
        self.age = 0
        self.activated = False

    def move(self):
        """Déplacement aléatoire dans la grille."""
        dx, dy = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
        self.x = np.clip(self.x + dx, 0, self.grid_size - 1)
        self.y = np.clip(self.y + dy, 0, self.grid_size - 1)

    def activate(self):
        self.color = 'red'
        self.activated = True
    
    def get_older(self):
        self.age +=1

    def cell_division(self):
        new_cell = LymphocyteB(self.x+1, self.y, self.grid_size)
        new_cell.color = self.color
        new_cell.age = 0
        return new_cell

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

    def cell_division(self):
        new_cell = LymphocyteT(self.x+1, self.y, self.grid_size)
        new_cell.age = 0
        return new_cell


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



def look_for_division(b_agent_list, t_agent_list):
    """ """

    # params
    b_pop = []
    t_pop = []
    treshold = 2

    # deal with b
    for b_agent in b_agent_list:
        ready_for_division = True

        # check other b cell
        for other_b in b_agent_list:
            dist = math.sqrt((b_agent.x - other_b.x)**2 + (b_agent.y - other_b.y)**2)
            if b_agent != other_b and dist  <= treshold:
                ready_for_division = False
                break
            
        # check t cells
        for t_agent in t_agent_list:
            dist = math.sqrt((b_agent.x - t_agent.x)**2 + (b_agent.y - t_agent.y)**2)
            if b_agent != t_agent and dist  <= treshold:
                ready_for_division = False
                break

        # add b cell to pop
        b_pop.append(b_agent)
        
        # cell division
        if ready_for_division:
            new_b = b_agent.cell_division()
            b_pop.append(new_b)
            
    # deal with t
    for t_agent in t_agent_list:
        ready_for_division = True

        # check other t cell
        for other_t in t_agent_list:
            dist = math.sqrt((t_agent.x - other_t.x)**2 + (t_agent.y - other_t.y)**2)
            if t_agent != other_t and dist <= treshold:
                ready_for_division = False
                break
            
        # check b cells
        for b_agent in b_agent_list:
            dist = math.sqrt((t_agent.x - b_agent.x)**2 + (t_agent.y - b_agent.y)**2)
            if t_agent != b_agent and dist <= treshold:
                ready_for_division = False
                break

        # add b cell to pop
        t_pop.append(t_agent)
        
        # cell division
        if ready_for_division:
            new_t = t_agent.cell_division()
            t_pop.append(new_t)


    return b_pop, t_pop


    


def init_random_age(b_agents, t_agents):
    """assign a random age to cells, used at the begining of the simulation"""

    b_pop = []
    t_pop = []

    for b_agent in b_agents:
        b_agent.age = random.randint(0, b_agent.life_span)
        b_pop.append(b_agent)
    for t_agent in t_agents:
        t_agent.age = random.randint(0, t_agent.life_span)
        t_pop.append(t_agent)

    return b_pop, t_pop


def run_simulation(n_steps:int, output_folder:str):
    """Run"""

    # initialisation de l'environnement
    if not os.path.isdir(f"{output_folder}"):
        os.mkdir(f"{output_folder}") 
    if not os.path.isdir(f"{output_folder}/figures"):
        os.mkdir(f"{output_folder}/figures")
    if not os.path.isdir(f"{output_folder}/logs"):
        os.mkdir(f"{output_folder}/logs")

    # Initialisation de la simulation
    grid_size = 20
    n_b_agents = 10
    b_agents = [LymphocyteB(np.random.randint(0, grid_size), np.random.randint(0, grid_size), grid_size) for _ in range(n_b_agents)]
    n_t_agents = 10
    t_agents = [LymphocyteT(np.random.randint(0, grid_size), np.random.randint(0, grid_size), grid_size) for _ in range(n_t_agents)]

    # init metrics
    step_to_nb = [{"STEP":0, "VALUE":n_b_agents}]
    step_to_nt = [{"STEP":0, "VALUE":n_t_agents}]
    step_to_nab = [{"STEP":0, "VALUE":0}]
    step_to_n_total = [{"STEP":0,"VALUE":n_b_agents+n_t_agents}]
    step_to_density = [{"STEP":0, "VALUE":float(n_b_agents+n_t_agents) / (grid_size*grid_size)}]

    # init random age for cells
    b_agents, t_agents = init_random_age(b_agents, t_agents)

    # Simulation
    for i in tqdm(range(n_steps), desc="Simulation en cours"):

        # init cmpts
        n_activated_b = 0

        # detect b activation
        detect_interaction(b_agents, t_agents)

        # cell division
        b_agents, t_agents = look_for_division(b_agents, t_agents)

        # drop old cells
        b_agents, t_agents = drop_old_cell(b_agents, t_agents)
        
        plt.figure(figsize=(5, 5))
        plt.xlim(0, grid_size)
        plt.ylim(0, grid_size)
        for b_agent in b_agents:
            b_agent.move()
            b_agent.get_older()
            plt.scatter(b_agent.x, b_agent.y, c=b_agent.color)

            # compute nb of activared b cells
            if b_agent.activated:
                n_activated_b +=1
            
        for t_agent in t_agents:
            t_agent.move()
            t_agent.get_older()
            plt.scatter(t_agent.x, t_agent.y, c=t_agent.color)
        plt.savefig(f"{output_folder}/figures/step_{i}.png")
        plt.close()

        # update metrics
        step_to_nb.append({"STEP":i, "VALUE":len(b_agents)})
        step_to_nt.append({"STEP":i, "VALUE":len(t_agents)})
        step_to_nab.append({"STEP":i, "VALUE":n_activated_b})
        step_to_n_total.append({"STEP":i, "VALUE":len(b_agents)+len(t_agents)})
        step_to_density.append({"STEP":i, "VALUE":float(len(b_agents)+len(t_agents)) / (grid_size*grid_size)})


    # save metrics in logs
    df = pd.DataFrame(step_to_nb)
    df.to_csv(f"{output_folder}/logs/nb_bcell.csv", index=False)
    df = pd.DataFrame(step_to_nt)
    df.to_csv(f"{output_folder}/logs/nb_tcell.csv", index=False)
    df = pd.DataFrame(step_to_nab)
    df.to_csv(f"{output_folder}/logs/nb_activated_bcell.csv", index=False)
    df = pd.DataFrame(step_to_n_total)
    df.to_csv(f"{output_folder}/logs/nb_total.csv", index=False)
    df = pd.DataFrame(step_to_density)
    df.to_csv(f"{output_folder}/logs/density.csv", index=False)
    

if __name__ == "__main__":

    run_simulation(100, "/tmp/zog")
