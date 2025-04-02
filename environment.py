
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


def drop_old_cell(b_agent_list:list, t_agent_list:list):
    """Drop cells that expect their lifespan

    Args:
        - b_agent_list (list) : list of Bcell object
        - t_agent_list (list) : list of Tcell object

    Returns:
        - (list) : list of alive Bcell object
        - (list) : list of alive Tcell object
    
    """

    # params
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


def look_for_division(b_agent_list:list, t_agent_list:list):
    """Look for cells in conditions for a cell division (basically check empty space around)
    and activate division

    Args:
        - b_agent_list (list) : list of Bcell object
        - t_agent_list (list) : list of Tcell object

    Returns:
        - (list) : list of alive Bcell object
        - (list) : list of alive Tcell object
    
    """

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
