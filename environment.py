
# load usual dependencies
import numpy as np
import math
import os
import random
import pandas as pd
import glob

def detect_interaction(b_agent_list:list, t_agent_list:list) -> None:
    """Detect interaction between Bcells and Tcells, switch activation for Bcells
    if a Tcells is nearby.

    Args:
        b_agent_list (list) : list of Bcell object
        t_agent_list (list) : list of Tcell object
    
    """

    # params
    interaction_treshold = 2

    # loop over agent    
    for b_agent in b_agent_list:
        for t_agent in t_agent_list:

            # compute distance
            dist = math.sqrt((b_agent.x - t_agent.x)**2 + (b_agent.y - t_agent.y)**2)

            # activate b cell
            if dist <= interaction_treshold:
                b_agent.activate()


def drop_old_cell(agent_list_list:list):
    """Drop cells that exceed their lifespan

    Args:
        - agent_list_list (list) : list of list of agents, e.g [b_agents, t_agents]

    Returns:
        - (list) : updated list of agent list 
    
    """

    # params
    updated_list = []

    # look for old agents
    for agent_list in agent_list_list:
        agent_list_updated = []
        for agent in agent_list:
            if agent.age <= agent.life_span:
                agent_list_updated.append(agent)
        updated_list.append(agent_list_updated)

    return updated_list
            
def look_for_division(agent_list_list:list) -> list:
    """Look for cells in conditions for a cell division (basically check empty space around)
    and activate division

    Args:
        - agent_list_list (list) : list of list of agents, e.g [b_agents, t_agents]

    Returns:
        - (list) : updated list of agent list 

    """

    # params
    treshold = 2
    updated_list = []

    for agent_list in agent_list_list:
        agent_list_updated = []
        for agent in agent_list:
            ready_for_division = True

            # check other agent cell
            for agent_list_to_check in agent_list_list:
                for agent_to_check in agent_list_to_check:
                    dist = math.sqrt((agent.x - agent_to_check.x)**2 + (agent.y - agent_to_check.y)**2)
                    if agent != agent_to_check and dist  <= treshold:
                        ready_for_division = False
                        break

            # add agent cell to pop
            agent_list_updated.append(agent)
        
            # cell division
            if ready_for_division:
                new_agent = agent.cell_division()
                agent_list_updated.append(new_agent)

        # update list of list
        updated_list.append(agent_list_updated)
            
    return updated_list



def init_random_age(b_agents:list, t_agents:list):
    """assign a random age to cells, used at the begining of the simulation
    
    Args:
        - b_agents (list) : list of Bcell object
        - t_agents (list) : list of Tcell object

    Returns:
        - (list) : list of alive Bcell object
        - (list) : list of alive Tcell object
    
    """

    # params
    b_pop = []
    t_pop = []

    # deal with Bcells
    for b_agent in b_agents:
        b_agent.age = random.randint(0, b_agent.life_span)
        b_pop.append(b_agent)

    # deal with Tcells
    for t_agent in t_agents:
        t_agent.age = random.randint(0, t_agent.life_span)
        t_pop.append(t_agent)

    return b_pop, t_pop
