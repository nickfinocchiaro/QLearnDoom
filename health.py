#!/usr/bin/env python

#####################################################################
# This script presents how to use the most basic features of the environment.
# It configures the engine, and makes the agent perform random actions.
# It also gets current state and reward earned with the action.
# <episodes> number of episodes are played. 
# Random combination of buttons is chosen for every action.
# Game variables from state and last reward are printed.
#
# To see the scenario description go to "../../scenarios/README.md"
#####################################################################

from __future__ import print_function

from vizdoom import *

from random import choice
from time import sleep
from healthlearningAgent import *

import itertools as it
import math


# Create DoomGame instance. It will run the game and communicate with you.
game = DoomGame()
game.load_config("../../examples/config/health_gathering.cfg")
#game.set_mode(Mode.ASYNC_PLAYER)
#game.set_ticrate(35)

# Enables depth buffer.
game.set_depth_buffer_enabled(True)

# Enables labeling of in game objects labeling.
game.set_labels_buffer_enabled(True)

# Enables buffer with top down map of the current episode/level.
game.set_automap_buffer_enabled(True)


# Adds game variables that will be included in state.
game.add_available_game_variable(GameVariable.POSITION_X)
game.add_available_game_variable(GameVariable.POSITION_Y)
game.add_available_game_variable(GameVariable.POSITION_Z)


# Makes the window appear (turned on by default)
game.set_window_visible(True)

# Turns on the sound. (turned off by default)
game.set_sound_enabled(True)


# Sets ViZDoom mode (PLAYER, ASYNC_PLAYER, SPECTATOR, ASYNC_SPECTATOR, PLAYER mode is default)
#game.set_mode(Mode.PLAYER)

# Initialize the game. Further configuration won't take any effect from now on.
#game.set_console_enabled(True)
game.init()

# Define some actions. Each list entry corresponds to declared buttons:
# MOVE_LEFT, MOVE_RIGHT, ATTACK
# 5 more combinations are naturally possible but only 3 are included for transparency when watching.
#actions = [[True, False, False], [False, True, False], [False, False, True]]
n = game.get_available_buttons_size()
actions = [list(a) for a in it.product([0, 1], repeat=n)]


# Run this many episodes
episodes = 60

# Sets time that will pause the engine after each action (in seconds)
# Without this everything would go too fast for you to keep track of what's happening.
sleep_time = 1 / DEFAULT_TICRATE # = 0.028


agent      = ApproximateQAgent()
resolution = (game.get_screen_width(), game.get_screen_height())
skiprate   = 1

def distance(obj1, obj2):
    # Objects received in form [x, y, z] coordinates

    # Find the sum of the squares
    sumOfSquares = 0
    for i in range(0, 3):
        sumOfSquares += pow(obj1[i] - obj2[i], 2)

    # Return the square root of the sum of the squares.
    return math.sqrt(sumOfSquares)



def objectDistances(buffers):
    # Input:  game.get_state()
    # Output: a dictionary of distances of objects (excluding self) with
    #         game.get_state().labels.value as keys

    coordinates = {}
    for l in buffers.labels:
        coordinates[l.value] = [l.object_position_x,
                                l.object_position_y,
                                l.object_position_z]

        
    gv = buffers.game_variables
    #print(gv)
    if not gv == None:
        coordinates[255] = [gv[1], gv[2], gv[3]]
    distances = {}
    #print(coordinates.keys())
    for key in list(coordinates.keys()):
        distances[key] = distance(coordinates[key], coordinates[255])

    return distances

            
def extractObjects(buffers, resolution):
    distances = objectDistances(buffers)
    
    objects = {}
    
    labels_buf = buffers.labels_buffer

    keys = []
    for l in buffers.labels:
        keys.append(l.value)

    for key in keys:
        objects[key] = ('Medikit', distances[key])

    return objects


def getGameState(game):
    game_state = game.get_state()
    
    return (game_state,
            extractObjects(game_state, resolution),
            actions,
            resolution,
            game_state.game_variables,
            game.is_episode_finished())



for i in range(episodes):
    print("Episode #" + str(i + 1))
    if i == 31:
        agent.stopTraining()
        print("Ending training mode.")
        print("Entering testing mode.")
        
    # Starts a new episode. It is not needed right after init() but it doesn't cost much. At least the loop is nicer.
    game.new_episode()

    while not game.is_episode_finished():

        ##############################
        """ *** BEGIN OUR CODE *** """
        ##############################
        
        state = getGameState(game)
        
        action    = agent.getAction(state)

        reward    = game.make_action(action, skiprate)        

        nextState = getGameState(game)

        agent.update(state, action, nextState, reward)
                            
        ###############################
        """ *** END OF OUR CODE *** """
        ###############################


        if sleep_time > 0:
            sleep(sleep_time)

    # Check how the episode went.
    print("Episode finished.")
    print("Total reward:", game.get_total_reward())
    print("************************")

# It will be done automatically anyway but sometimes you need to do it in the middle of the program...
game.close()

