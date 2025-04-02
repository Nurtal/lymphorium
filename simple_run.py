# load usual dependencies
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import random
import pandas as pd

# load agents
from agents.b_cell import LymphocyteB
from agents.t_cell import LymphocyteT

# load modules
import displayer
import environment

def run_simulation(n_steps:int, output_folder:str) -> None:
    """Run Simulation

    Args:
        - n_steps (int) : number of steps for the simulation
        - output_folder (str) : path to the output folder
    
    """

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
    step_to_nnb = [{"STEP":0, "VALUE":0}]
    step_to_n_total = [{"STEP":0,"VALUE":n_b_agents+n_t_agents}]
    step_to_density = [{"STEP":0, "VALUE":float(n_b_agents+n_t_agents) / (grid_size*grid_size)}]

    # init random age for cells
    b_agents, t_agents = environment.init_random_age(b_agents, t_agents)

    # Simulation
    for i in tqdm(range(n_steps), desc="Simulation en cours"):

        # init cmpts
        n_activated_b = 0
        n_naive_b = 0

        # detect b activation
        environment.detect_interaction(b_agents, t_agents)

        # cell division
        b_agents, t_agents = environment.look_for_division(b_agents, t_agents)

        # drop old cells
        b_agents, t_agents = environment.drop_old_cell(b_agents, t_agents)
        
        plt.figure(figsize=(5, 5))
        plt.xlim(0, grid_size)
        plt.ylim(0, grid_size)
        for b_agent in b_agents:
            b_agent.move()
            b_agent.get_older()
            plt.scatter(b_agent.x, b_agent.y, c=b_agent.color)

            # compute nb of activated b cells
            if b_agent.activated:
                n_activated_b +=1
            else:
                n_naive_b += 1
            
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
        step_to_nnb.append({"STEP":i, "VALUE":n_naive_b})
        step_to_n_total.append({"STEP":i, "VALUE":len(b_agents)+len(t_agents)})
        step_to_density.append({"STEP":i, "VALUE":float(len(b_agents)+len(t_agents)) / (grid_size*grid_size)})

    # save metrics in logs
    df = pd.DataFrame(step_to_nb)
    df.to_csv(f"{output_folder}/logs/nb_bcell.csv", index=False)
    df = pd.DataFrame(step_to_nt)
    df.to_csv(f"{output_folder}/logs/nb_tcell.csv", index=False)
    df = pd.DataFrame(step_to_nab)
    df.to_csv(f"{output_folder}/logs/nb_activated_bcell.csv", index=False)
    df = pd.DataFrame(step_to_nnb)
    df.to_csv(f"{output_folder}/logs/nb_naive_bcell.csv", index=False)
    df = pd.DataFrame(step_to_n_total)
    df.to_csv(f"{output_folder}/logs/nb_total.csv", index=False)
    df = pd.DataFrame(step_to_density)
    df.to_csv(f"{output_folder}/logs/density.csv", index=False)
    

if __name__ == "__main__":

    run_simulation(100, "/tmp/zog")
    displayer.display_logs("/tmp/zog/logs", "/tmp/test.png")
    displayer.craft_simulation_animation("/tmp/zog/figures", "/tmp/test.gif")
