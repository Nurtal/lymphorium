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
from agents.pathogen import Pathogen
from agents.nk_cell import NaturalKiller
from agents.neutro_cell import Neutrophile
from agents.dendritic_cell import Dendritic

# load modules
import displayer
import environment


def parse_configuration(configuration_file:str)->dict:
    """Parse a configuration file, returns extracted parameters in a dict.
    dict contain a 'valid' key, set to False if configuration file is missing
    or one of the expected parmaters is missing from file.
    Expected parmaters are:
        - n_steps
        - output_folder
        - grid_size
        - n_b_agents
        - n_t_agents
        - n_pathogen_agents

    Args:
        - configuration_file (str) : path to configuration file, supposed to be a ces file with two columns : 'PARAMETER' and 'VALUE'

    Returns:
        - (dict) : key as parameters and value as values
        
    """

    # init configuration
    configuration = {"valid":False}
    mandatory_params = [
        "n_steps",
        "output_folder",
        "grid_size",
        "n_b_agents",
        "n_t_agents",
        "n_pathogen_agents",
        "n_nk_agents",
        "n_neutro_agents",
        "n_dendritic_agents"
    ]

    # check if config file exist
    if not os.path.isfile(configuration_file):
        print(f"[!] Can't find file {configuration_file}")
        return configuration

    # load parameters from configuration
    df = pd.read_csv(configuration_file)
    for index, row in df.iterrows():
        configuration[row['PARAMETER']] = row['VALUE']

    # look for mandatory parameters
    configuration['valid'] = True
    for mp in mandatory_params:
        if mp not in configuration:
            print(f"[!] Missing mandatory parameter {mp} from configuration file")
            configuration['valid'] = False

    # return configuration as a dict
    return configuration


def run_simulation(n_steps:int, output_folder:str, grid_size:int, n_b_agents:int, n_t_agents:int, n_pathogen_agents:int, n_nk_agents:int, n_neutro_agents:int, n_dendritic_agents:int) -> None:
    """Run Simulation

    Args:
        - n_steps (int) : number of steps for the simulation
        - output_folder (str) : path to the output folder
        - grid_size (int) : grid_size (assume grid is a square)
        - n_b_agents (int) : number of b cells at initial condition
        - n_t_agents (int) : number of t cells at initial condition
        - n_pathogen_agents (int) : number of pathogen cell at initial condition
        - n_nk_agents (int) : number of natural killer cell at initial condition
        - n_neutro_agents (int) : number of neutrophile cell at initial condition
        - n_dendritic_agents (int) : number of dendritic cell at initial condition
    
    """

    # initialisation de l'environnement
    if not os.path.isdir(f"{output_folder}"):
        os.mkdir(f"{output_folder}") 
    if not os.path.isdir(f"{output_folder}/figures"):
        os.mkdir(f"{output_folder}/figures")
    if not os.path.isdir(f"{output_folder}/images"):
        os.mkdir(f"{output_folder}/images")
    if not os.path.isdir(f"{output_folder}/logs"):
        os.mkdir(f"{output_folder}/logs")

    # Initialisation de la simulation
    b_agents = [LymphocyteB(np.random.randint(0, grid_size), np.random.randint(0, grid_size), grid_size) for _ in range(n_b_agents)]
    t_agents = [LymphocyteT(np.random.randint(0, grid_size), np.random.randint(0, grid_size), grid_size) for _ in range(n_t_agents)]
    pathogen_agents = [Pathogen(np.random.randint(0, grid_size), np.random.randint(0, grid_size), grid_size) for _ in range(n_pathogen_agents)]
    nk_agents = [NaturalKiller(np.random.randint(0, grid_size), np.random.randint(0, grid_size), grid_size) for _ in range(n_nk_agents)]
    neutro_agents = [Neutrophile(np.random.randint(0, grid_size), np.random.randint(0, grid_size), grid_size) for _ in range(n_neutro_agents)]
    dendritic_agents = [Dendritic(np.random.randint(0, grid_size), np.random.randint(0, grid_size), grid_size) for _ in range(n_dendritic_agents)]

    # init metrics
    step_to_nb = [{"STEP":0, "VALUE":n_b_agents}]
    step_to_nt = [{"STEP":0, "VALUE":n_t_agents}]
    step_to_nab = [{"STEP":0, "VALUE":0}]
    step_to_nnb = [{"STEP":0, "VALUE":0}]
    step_to_n_total = [{"STEP":0,"VALUE":n_b_agents+n_t_agents}]
    step_to_density = [{"STEP":0, "VALUE":float(n_b_agents+n_t_agents) / (grid_size*grid_size)}]

    # init random age for cells
    b_agents, t_agents, pathogen_agents, nk_agents, neutro_agents, dendritic_agents = environment.init_random_age([b_agents, t_agents, pathogen_agents, nk_agents, neutro_agents, dendritic_agents])

    # Simulation
    for i in tqdm(range(n_steps), desc="Simulation en cours"):

        # init cmpts
        n_activated_b = 0
        n_naive_b = 0

        # detect b activation
        environment.detect_interaction(b_agents, t_agents)

        # cell division
        b_agents, t_agents, pathogen_agents, nk_agents, neutro_agents, dendritic_agents = environment.look_for_division([b_agents, t_agents, pathogen_agents, nk_agents, neutro_agents, dendritic_agents])

        # drop old cells
        b_agents, t_agents, pathogen_agents, nk_agents, neutro_agents, dendritic_agents = environment.drop_old_cell([b_agents, t_agents, pathogen_agents, nk_agents, neutro_agents, dendritic_agents])
        
        plt.figure(figsize=(5, 5))
        plt.xlim(0, grid_size)
        plt.ylim(0, grid_size)

        # deal with b cells
        for b_agent in b_agents:
            b_agent.move()
            b_agent.get_older()
            plt.scatter(b_agent.x, b_agent.y, c=b_agent.color)

            # compute nb of activated b cells
            if b_agent.activated:
                n_activated_b +=1
            else:
                n_naive_b += 1
            
        # deal wth t cells
        for t_agent in t_agents:
            t_agent.move()
            t_agent.get_older()
            plt.scatter(t_agent.x, t_agent.y, c=t_agent.color)

        # deal with pathogen
        for pathogen_agent in pathogen_agents:
            pathogen_agent.move()
            pathogen_agent.get_older()
            plt.scatter(pathogen_agent.x, pathogen_agent.y, c=pathogen_agent.color)

        # deal with nk cells
        for nk_agent in nk_agents:
            nk_agent.move()
            nk_agent.get_older()
            plt.scatter(nk_agent.x, nk_agent.y, c=nk_agent.color)
            
        # deal with neutrophile cells
        for neutro_agent in neutro_agents:
            neutro_agent.move()
            neutro_agent.get_older()
            plt.scatter(neutro_agent.x, neutro_agent.y, c=neutro_agent.color)

        # deal with dendritic cells
        for dendritic_agent in dendritic_agents:
            dendritic_agent.move()
            dendritic_agent.get_older()
            plt.scatter(dendritic_agent.x, dendritic_agent.y, c=dendritic_agent.color)
        
        plt.savefig(f"{output_folder}/images/step_{i}.png")
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


def run(configuration_file:str):
    """Run the simulation and create associated graphical representations
    
    Args:
        configuration_file (str) : path to the configuration file
    
    """

    # parse configuration
    configuration = parse_configuration(configuration_file)

    # check config validity
    if configuration['valid']:

        # run
        run_simulation(
                       int(configuration['n_steps']),
                       str(configuration['output_folder']),
                       int(configuration['grid_size']),
                       int(configuration['n_b_agents']),
                       int(configuration['n_t_agents']),
                       int(configuration['n_pathogen_agents']),
                       int(configuration['n_nk_agents']),
                       int(configuration['n_neutro_agents']),
                       int(configuration['n_dendritic_agents'])
        )

        # create representations
        displayer.display_logs(f"{configuration['output_folder']}/logs", f"{configuration['output_folder']}/figures/logs.png")
        displayer.craft_simulation_animation(f"{configuration['output_folder']}/images", f"{configuration['output_folder']}/figures/simulation.gif")
    

if __name__ == "__main__":

    # run_simulation(100, "/tmp/zog")
    # displayer.display_logs("/tmp/zog/logs", "/tmp/test.png")
    # displayer.craft_simulation_animation("/tmp/zog/figures", "/tmp/test.gif")

    run("ressources/exemple.conf")
